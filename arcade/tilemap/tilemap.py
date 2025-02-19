"""
This module provides functionality to load in JSON map files from
the Tiled Map Editor. This is achieved using the pytiled-parser 
library.

For more info on Tiled see: https://www.mapeditor.org/
For more info on pytiled-parser see: https://github.com/Beefy-Swain/pytiled_parser
"""

import copy
import math
import os
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, OrderedDict, Tuple, Union, cast

import pytiled_parser
import pytiled_parser.tiled_object
from arcade import (
    AnimatedTimeBasedSprite,
    AnimationKeyframe,
    Sprite,
    SpriteList,
    load_texture,
)
from arcade.arcade_types import Point, TiledObject
from arcade.resources import resolve_resource_path

_FLIPPED_HORIZONTALLY_FLAG = 0x80000000
_FLIPPED_VERTICALLY_FLAG = 0x40000000
_FLIPPED_DIAGONALLY_FLAG = 0x20000000


def _get_image_info_from_tileset(tile: pytiled_parser.Tile):
    image_x = 0
    image_y = 0
    if tile.tileset.image is not None:
        margin = tile.tileset.margin or 0
        spacing = tile.tileset.spacing or 0
        row = tile.id // tile.tileset.columns
        image_y = margin + row * (tile.tileset.tile_height + spacing)
        col = tile.id % tile.tileset.columns
        image_x = margin + col * (tile.tileset.tile_width + spacing)

    if tile.tileset.image:
        width = tile.tileset.tile_width
        height = tile.tileset.tile_height
    else:
        width = tile.image_width
        height = tile.image_height

    return image_x, image_y, width, height


def _get_image_source(
    tile: pytiled_parser.Tile,
    map_directory: Optional[str],
) -> Optional[Path]:
    image_file = None
    if tile.image:
        image_file = tile.image
    elif tile.tileset.image:
        image_file = tile.tileset.image

    if not image_file:
        print(
            f"Warning for tile {tile.id}, no image source listed either for individual tile, or as a tileset."
        )
        return None

    if os.path.exists(image_file):
        return image_file

    if map_directory:
        try2 = Path(map_directory, image_file)
        if os.path.exists(try2):
            return try2

    print(f"Warning, can't find image {image_file} for tile {tile.id}")
    return None


class TileMap:
    """
    Class that represents a fully parsed and loaded map from Tiled.
    For examples on how to use this class, see:
    https://arcade.academy/examples/index.html#using-tiled-map-editor-to-create-maps

    Attributes:
        :tiled_map: The pytiled-parser map object. This can be useful for implementing features
                    that aren't supported by this class by accessing the raw map data directly.
        :width: The width of the map in tiles. This is the number of tiles, not pixels.
        :height: The height of the map in tiles. This is the number of tiles, not pixels.
        :tile_width: The width in pixels of each tile.
        :tile_height: The height in pixels of each tile.
        :background_color: The background color of the map.
        :scaling: A global scaling value to be applied to all Sprites in the map.
        :sprite_lists: A dictionary mapping SpriteLists to their layer names. This is used
                       for all tile layers of the map.
        :object_lists: A dictionary mapping TiledObjects to their layer names. This is used
                       for all object layers of the map.
    """

    def __init__(
        self,
        map_file: Union[str, Path],
        scaling: float = 1.0,
        layer_options: Optional[Dict[str, Dict[str, Any]]] = None,
        use_spatial_hash: Optional[bool] = None,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
    ) -> None:
        """
        Given a .json file, this will read in a Tiled map file, and
        initialize a new TileMap object.

        The `layer_options` parameter can be used to specify per layer arguments.
        The available options for this are:

            use_spatial_hash - A boolean to enable spatial hashing on this layer's SpriteList.
            scaling - A float providing layer specific Sprite scaling.
            hit_box_algorithm - A string for the hit box algorithm to use for the Sprite's in this layer.
            hit_box_detail - A float specifying the level of detail for each Sprite's hitbox

            For example:

            code-block::

                layer_options = {
                    "Platforms": {
                        "use_spatial_hash": True,
                        "scaling": 2.5,
                    },
                }

        The keys and their values in each layer are passed to the layer processing functions
        using the `**` operator on the dictionary.

        :param Union[str, Path] map_file: The JSON map file.
        :param float scaling: Global scaling to apply to all Sprites.
        :param Dict[str, Dict[str, Any]] layer_options: Extra parameters for each layer.
        :param Optional[bool] use_spatial_hash: If set to True, this will make moving a sprite
               in the SpriteList slower, but it will speed up collision detection
               with items in the SpriteList. Great for doing collision detection
               with static walls/platforms.
        :param str hit_box_algorithm: One of 'None', 'Simple' or 'Detailed'.
        :param float hit_box_detail: Float, defaults to 4.5. Used with 'Detailed' to hit box.
        """

        # If we should pull from local resources, replace with proper path
        map_file = resolve_resource_path(map_file)

        # This attribute stores the pytiled-parser map object
        self.tiled_map = pytiled_parser.parse_map(map_file)

        # Set Map Attributes
        self.width = self.tiled_map.map_size.width
        self.height = self.tiled_map.map_size.height
        self.tile_width = self.tiled_map.tile_size.width
        self.tile_height = self.tiled_map.tile_size.height
        self.background_color = self.tiled_map.background_color

        # Global Layer Defaults
        self.scaling = scaling
        self.use_spatial_hash = use_spatial_hash
        self.hit_box_algorithm = hit_box_algorithm
        self.hit_box_detail = hit_box_detail

        # Dictionaries to store the SpriteLists for processed layers
        self.sprite_lists: OrderedDict[str, SpriteList] = OrderedDict[str, SpriteList]()
        self.object_lists: OrderedDict[str, List[TiledObject]] = OrderedDict[
            str, SpriteList
        ]()
        self.properties = self.tiled_map.properties

        global_options = {
            "scaling": self.scaling,
            "use_spatial_hash": self.use_spatial_hash,
            "hit_box_algorithm": self.hit_box_algorithm,
            "hit_box_detail": self.hit_box_detail,
        }

        for layer in self.tiled_map.layers:
            if (layer.name in self.sprite_lists) or (layer.name in self.object_lists):
                raise AttributeError(
                    f"You have a duplicate layer name '{layer.name}' in your Tiled map. "
                    "Please use unique names for all layers and tilesets in your map."
                )
            self._process_layer(layer, global_options, layer_options)

    def _process_layer(
        self,
        layer: pytiled_parser.Layer,
        global_options: Dict[str, Any],
        layer_options: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> None:

        processed: Union[
            SpriteList, Tuple[Optional[SpriteList], Optional[List[TiledObject]]]
        ]

        options = global_options

        if layer_options:
            if layer.name in layer_options:
                new_options = {
                    key: layer_options[layer.name].get(key, global_options[key])
                    for key in global_options
                }
                options = new_options

        if isinstance(layer, pytiled_parser.TileLayer):
            processed = self._process_tile_layer(layer, **options)
            self.sprite_lists[layer.name] = processed
        elif isinstance(layer, pytiled_parser.ObjectLayer):
            processed = self._process_object_layer(layer, **options)
            if processed[0]:
                sprite_list = processed[0]
                if sprite_list:
                    self.sprite_lists[layer.name] = sprite_list
            if processed[1]:
                object_list = processed[1]
                if object_list:
                    self.object_lists[layer.name] = object_list
        elif isinstance(layer, pytiled_parser.ImageLayer):
            processed = self._process_image_layer(layer, **options)
            self.sprite_lists[layer.name] = processed
        elif isinstance(layer, pytiled_parser.LayerGroup):
            for sub_layer in layer.layers:
                self._process_layer(sub_layer, global_options, layer_options)

    def get_cartesian(
        self,
        x: float,
        y: float,
    ) -> Tuple[float, float]:
        """
        Given a set of coordinates in pixel units, this returns the cartesian coordinates.

        This assumes the supplied coordinates are pixel coordinates, and bases the cartesian
        grid off of the Map's tile size.

        If you have a map with 128x128 pixel Tiles, and you supply coordinates 500, 250 to
        this function you'll receive back 3, 2

        :param float x: The X Coordinate to convert
        :param float y: The Y Coordinate to convert
        """
        x = math.floor(x / (self.tile_width * self.scaling))
        y = math.floor(y / (self.tile_height * self.scaling))

        return x, y

    def get_tilemap_layer(self, layer_path: str) -> Optional[pytiled_parser.Layer]:
        assert isinstance(layer_path, str)

        def _get_tilemap_layer(my_path, layers):
            layer_name = my_path.pop(0)
            for my_layer in layers:
                if my_layer.name == layer_name:
                    if isinstance(my_layer, pytiled_parser.LayerGroup):
                        if len(my_path) != 0:
                            return _get_tilemap_layer(my_path, my_layer.layers)
                    else:
                        return my_layer
            return None

        path = layer_path.strip("/").split("/")
        layer = _get_tilemap_layer(path, self.tiled_map.layers)
        return layer

    def _get_tile_by_gid(self, tile_gid: int) -> Optional[pytiled_parser.Tile]:
        flipped_diagonally = False
        flipped_horizontally = False
        flipped_vertically = False

        if tile_gid & _FLIPPED_HORIZONTALLY_FLAG:
            flipped_horizontally = True
            tile_gid -= _FLIPPED_HORIZONTALLY_FLAG

        if tile_gid & _FLIPPED_DIAGONALLY_FLAG:
            flipped_diagonally = True
            tile_gid -= _FLIPPED_DIAGONALLY_FLAG

        if tile_gid & _FLIPPED_VERTICALLY_FLAG:
            flipped_vertically = True
            tile_gid -= _FLIPPED_VERTICALLY_FLAG

        for tileset_key, tileset in self.tiled_map.tilesets.items():
            if tile_gid < tileset_key:
                continue

            # No specific tile info, but there is a tile sheet
            # print(f"data {tileset_key} {tileset.tiles} {tileset.image} {tileset_key} {tile_gid} {tileset.tile_count}")
            if (
                tileset.image is not None
                and tileset_key <= tile_gid < tileset_key + tileset.tile_count
            ):
                # No specific tile info, but there is a tile sheet
                tile_ref = pytiled_parser.Tile(
                    id=(tile_gid - tileset_key), image=tileset.image
                )
            elif tileset.tiles is None and tileset.image is not None:
                # Not in this tileset, move to the next
                continue
            else:
                if tileset.tiles is None:
                    return None
                tile_ref = tileset.tiles.get(tile_gid - tileset_key)

            if tile_ref:
                my_tile = copy.copy(tile_ref)
                my_tile.tileset = tileset
                my_tile.flipped_vertically = flipped_vertically
                my_tile.flipped_diagonally = flipped_diagonally
                my_tile.flipped_horizontally = flipped_horizontally
                return my_tile

        print(f"Returning NO tile for {tile_gid}.")
        return None

    def _get_tile_by_id(
        self, tileset: pytiled_parser.Tileset, tile_id: int
    ) -> Optional[pytiled_parser.Tile]:
        for tileset_key, cur_tileset in self.tiled_map.tilesets.items():
            if cur_tileset is tileset:
                for tile_key, tile in cur_tileset.tiles.items():
                    if tile_id == tile.id:
                        return tile

        return None

    def _create_sprite_from_tile(
        self,
        tile: pytiled_parser.Tile,
        scaling: float = 1.0,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
    ) -> Sprite:
        """Given a tile from the parser, try and create a Sprite from it."""

        # --- Step 1, Find a reference to an image this is going to be based off of
        map_source = self.tiled_map.map_file
        map_directory = os.path.dirname(map_source)
        image_file = _get_image_source(tile, map_directory)

        if tile.animation:
            my_sprite: Sprite = AnimatedTimeBasedSprite(image_file, scaling)
        else:
            image_x, image_y, width, height = _get_image_info_from_tileset(tile)
            my_sprite = Sprite(
                image_file,
                scaling,
                image_x,
                image_y,
                width,
                height,
                flipped_horizontally=tile.flipped_horizontally,
                flipped_vertically=tile.flipped_vertically,
                flipped_diagonally=tile.flipped_diagonally,
                hit_box_algorithm=hit_box_algorithm,
                hit_box_detail=hit_box_detail,
            )

        if tile.properties is not None and len(tile.properties) > 0:
            for key, value in tile.properties.items():
                my_sprite.properties[key] = value

        if tile.type:
            my_sprite.properties["type"] = tile.type

        if tile.objects is not None:
            if not isinstance(tile.objects, pytiled_parser.ObjectLayer):
                print("Warning, tile.objects is not an ObjectLayer as expected.")
                return my_sprite

            if len(tile.objects.tiled_objects) > 1:
                if tile.image:
                    print(
                        f"Warning, only one hit box supported for tile with image {tile.image}."
                    )
                else:
                    print(f"Warning, only one hit box supported for tile.")

            for hitbox in tile.objects.tiled_objects:
                points: List[Point] = []
                if isinstance(hitbox, pytiled_parser.tiled_object.Rectangle):
                    if hitbox.size is None:
                        print(
                            f"Warning: Rectangle hitbox created for without a "
                            f"height or width Ignoring."
                        )
                        continue

                    sx = hitbox.coordinates.x - (my_sprite.width / (scaling * 2))
                    sy = -(hitbox.coordinates.y - (my_sprite.height / (scaling * 2)))
                    ex = (hitbox.coordinates.x + hitbox.size.width) - (
                        my_sprite.width / (scaling * 2)
                    )
                    ey = -(hitbox.coordinates.y + hitbox.size.height) - (
                        my_sprite.height / (scaling * 2)
                    )

                    points = [[sx, sy], [ex, sy], [ex, ey], [sx, ey]]
                elif isinstance(
                    hitbox, pytiled_parser.tiled_object.Polygon
                ) or isinstance(hitbox, pytiled_parser.tiled_object.Polyline):
                    for point in hitbox.points:
                        adj_x = (
                            point.x
                            + hitbox.coordinates.x
                            - my_sprite.width / (scaling * 2)
                        )
                        adj_y = -(
                            point.y
                            + hitbox.coordinates.y
                            - my_sprite.height / (scaling * 2)
                        )
                        adj_point = [adj_x, adj_y]
                        points.append(adj_point)

                    if points[0][0] == points[-1][0] and points[0][1] == points[-1][1]:
                        points.pop()
                elif isinstance(hitbox, pytiled_parser.tiled_object.Ellipse):
                    if not hitbox.size:
                        print(
                            f"Warning: Ellipse hitbox created without a height "
                            f" or width for {tile.image}. Ignoring."
                        )
                        continue

                    hw = hitbox.size.width / 2
                    hh = hitbox.size.height / 2
                    cx = hitbox.coordinates.x + hw
                    cy = hitbox.coordinates.y + hh

                    acx = cx - (my_sprite.width / (scaling * 2))
                    acy = cy - (my_sprite.height / (scaling * 2))

                    total_steps = 8
                    angles = [
                        step / total_steps * 2 * math.pi for step in range(total_steps)
                    ]
                    for angle in angles:
                        x = hw * math.cos(angle) + acx
                        y = -(hh * math.sin(angle) + acy)
                        points.append([x, y])
                else:
                    print(f"Warning: Hitbox type {type(hitbox)} not supported.")

                my_sprite.hit_box = points

        if tile.animation:
            key_frame_list = []
            for frame in tile.animation:
                frame_tile = self._get_tile_by_id(tile.tileset, frame.tile_id)
                if frame_tile:
                    image_file = _get_image_source(frame_tile, map_directory)

                    if frame_tile.image and image_file:
                        texture = load_texture(image_file)
                    elif not frame_tile.image and image_file:
                        # No image for tile, pull from tilesheet
                        (
                            image_x,
                            image_y,
                            width,
                            height,
                        ) = _get_image_info_from_tileset(frame_tile)

                        texture = load_texture(
                            image_file, image_x, image_y, width, height
                        )
                    else:
                        print(
                            f"Warning: failed to load image for animation frame for tile {frame_tile.id}"
                        )
                        texture = None

                    key_frame = AnimationKeyframe(
                        frame.tile_id, frame.duration, texture
                    )
                    key_frame_list.append(key_frame)

                    if len(key_frame_list) == 1:
                        my_sprite.texture = key_frame.texture

            cast(AnimatedTimeBasedSprite, my_sprite).frames = key_frame_list

        return my_sprite

    def _process_image_layer(
        self,
        layer: pytiled_parser.ImageLayer,
        scaling: float = 1.0,
        use_spatial_hash: Optional[bool] = None,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
    ) -> SpriteList:

        sprite_list: SpriteList = SpriteList(use_spatial_hash=use_spatial_hash)

        map_source = self.tiled_map.map_file
        map_directory = os.path.dirname(map_source)
        image_file = layer.image

        if not os.path.exists(image_file) and (map_directory):
            try2 = Path(map_directory, image_file)
            if not os.path.exists(try2):
                print(
                    f"Warning, can't find image {image_file} for Image Layer {layer.name}"
                )
            image_file = try2

        my_texture = load_texture(
            image_file,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
        )

        if layer.transparent_color:
            data = my_texture.image.getdata()

            target = layer.transparent_color
            new_data = []
            for item in data:
                if (
                    item[0] == target[0]
                    and item[1] == target[1]
                    and item[2] == target[2]
                ):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            my_texture.image.putdata(new_data)

        my_sprite = Sprite(
            image_file,
            scaling,
            texture=my_texture,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
        )

        if layer.properties:
            for key, value in layer.properties.items():
                my_sprite.properties[key] = value

        if layer.tint_color:
            my_sprite.color = layer.tint_color

        if layer.opacity:
            my_sprite.alpha = int(layer.opacity * 255)

        my_sprite.center_x = (layer.offset[0] * scaling) + my_sprite.width / 2
        my_sprite.center_y = layer.offset[1]

        sprite_list.append(my_sprite)
        return sprite_list

    def _process_tile_layer(
        self,
        layer: pytiled_parser.TileLayer,
        scaling: float = 1.0,
        use_spatial_hash: Optional[bool] = None,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
    ) -> SpriteList:

        sprite_list: SpriteList = SpriteList(use_spatial_hash=use_spatial_hash)
        map_array = layer.data

        # Loop through the layer and add in the list
        for row_index, row in enumerate(map_array):
            for column_index, item in enumerate(row):
                # Check for an empty tile
                if item == 0:
                    continue

                tile = self._get_tile_by_gid(item)
                if tile is None:
                    raise ValueError(
                        (
                            f"Couldn't find tile for item {item} in layer "
                            f"'{layer.name}' in file '{self.tiled_map.map_file}'"
                            f"at ({column_index}, {row_index})."
                        )
                    )

                my_sprite = self._create_sprite_from_tile(
                    tile,
                    scaling=scaling,
                    hit_box_algorithm=hit_box_algorithm,
                    hit_box_detail=hit_box_detail,
                )

                if my_sprite is None:
                    print(
                        f"Warning: Could not create sprite number {item} in layer '{layer.name}' {tile.image}"
                    )
                else:
                    my_sprite.center_x = (
                        column_index * (self.tiled_map.tile_size[0] * scaling)
                        + my_sprite.width / 2
                    )
                    my_sprite.center_y = (
                        self.tiled_map.map_size.height - row_index - 1
                    ) * (self.tiled_map.tile_size[1] * scaling) + my_sprite.height / 2

                    # Tint
                    if layer.tint_color:
                        my_sprite.color = layer.tint_color

                    # Opacity
                    opacity = layer.opacity
                    if opacity:
                        my_sprite.alpha = int(opacity * 255)

                    sprite_list.append(my_sprite)

        return sprite_list

    def _process_object_layer(
        self,
        layer: pytiled_parser.ObjectLayer,
        scaling: float = 1.0,
        use_spatial_hash: Optional[bool] = None,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
    ) -> Tuple[Optional[SpriteList], Optional[List[TiledObject]]]:

        if not scaling:
            scaling = self.scaling

        sprite_list: Optional[SpriteList] = None
        objects_list: Optional[List[TiledObject]] = []

        for cur_object in layer.tiled_objects:
            # shape: Optional[Union[Point, PointList, Rect]] = None
            if isinstance(cur_object, pytiled_parser.tiled_object.Tile):
                if not sprite_list:
                    sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)

                tile = self._get_tile_by_gid(cur_object.gid)
                my_sprite = self._create_sprite_from_tile(
                    tile,
                    scaling=scaling,
                    hit_box_algorithm=hit_box_algorithm,
                    hit_box_detail=hit_box_detail,
                )

                x = cur_object.coordinates.x * scaling
                y = (
                    self.tiled_map.map_size.height * self.tiled_map.tile_size[1]
                    - cur_object.coordinates.y
                ) * scaling

                my_sprite.width = width = cur_object.size[0] * scaling
                my_sprite.height = height = cur_object.size[1] * scaling
                center_x = width / 2
                center_y = height / 2
                if cur_object.rotation:
                    rotation = -math.radians(cur_object.rotation)
                else:
                    rotation = 0

                cos_rotation = math.cos(rotation)
                sin_rotation = math.sin(rotation)
                rotated_center_x = center_x * cos_rotation - center_y * sin_rotation
                rotated_center_y = center_y * sin_rotation + center_y * cos_rotation

                my_sprite.position = (x + rotated_center_x, y + rotated_center_y)
                my_sprite.angle = math.degrees(rotation)

                if layer.tint_color:
                    my_sprite.color = layer.tint_color

                opacity = layer.opacity
                if opacity:
                    my_sprite.alpha = int(opacity * 255)

                if cur_object.properties and "change_x" in cur_object.properties:
                    my_sprite.change_x = float(cur_object.properties["change_x"])

                if cur_object.properties and "change_y" in cur_object.properties:
                    my_sprite.change_y = float(cur_object.properties["change_y"])

                if cur_object.properties and "boundary_bottom" in cur_object.properties:
                    my_sprite.boundary_bottom = float(
                        cur_object.properties["boundary_bottom"]
                    )

                if cur_object.properties and "boundary_top" in cur_object.properties:
                    my_sprite.boundary_top = float(
                        cur_object.properties["boundary_top"]
                    )

                if cur_object.properties and "boundary_left" in cur_object.properties:
                    my_sprite.boundary_left = float(
                        cur_object.properties["boundary_left"]
                    )

                if cur_object.properties and "boundary_right" in cur_object.properties:
                    my_sprite.boundary_right = float(
                        cur_object.properties["boundary_right"]
                    )

                if cur_object.properties:
                    my_sprite.properties.update(cur_object.properties)

                if cur_object.type:
                    my_sprite.properties["type"] = cur_object.type

                if cur_object.name:
                    my_sprite.properties["name"] = cur_object.name

                sprite_list.append(my_sprite)
                continue
            elif isinstance(cur_object, pytiled_parser.tiled_object.Point):
                x = cur_object.coordinates.x * scaling
                y = (
                    self.tiled_map.map_size.height * self.tiled_map.tile_size[1]
                    - cur_object.coordinates.y
                ) * scaling

                shape = [x, y]
            elif isinstance(cur_object, pytiled_parser.tiled_object.Rectangle):
                sx = cur_object.coordinates.x
                sy = -cur_object.coordinates.y
                ex = cur_object.coordinates.x + cur_object.size.width
                ey = -(cur_object.coordinates.y + cur_object.size.height)

                p1 = [sx, sy]
                p2 = [ex, sy]
                p3 = [ex, ey]
                p4 = [sx, ey]

                shape = [p1, p2, p3, p4]
            elif isinstance(
                cur_object, pytiled_parser.tiled_object.Polygon
            ) or isinstance(cur_object, pytiled_parser.tiled_object.Polyline):
                shape = []
                for point in cur_object.points:
                    x = point.x + cur_object.coordinates.x
                    y = (self.height * self.tile_height) - (
                        point.y + cur_object.coordinates.y
                    )
                    point = (x, y)
                    shape.append(point)

                # If shape is a polyline, and it is closed, we need to remove the duplicate end point
                if shape[0][0] == shape[-1][0] and shape[0][1] == shape[-1][1]:
                    shape.pop()
            elif isinstance(cur_object, pytiled_parser.tiled_object.Ellipse):
                hw = cur_object.size.width / 2
                hh = cur_object.size.height / 2
                cx = cur_object.coordinates.x + hw
                cy = cur_object.coordinates.y + hh

                total_steps = 8
                angles = [
                    step / total_steps * 2 * math.pi for step in range(total_steps)
                ]
                shape = []
                for angle in angles:
                    x = hw * math.cos(angle) + cx
                    y = -(hh * math.sin(angle) + cy)
                    point = [x, y]
                    shape.append(point)
            else:
                continue

            if shape:
                tiled_object = TiledObject(
                    shape, cur_object.properties, cur_object.name, cur_object.type
                )

                if not objects_list:
                    objects_list = []

                objects_list.append(tiled_object)

        return sprite_list or None, objects_list or None


def load_tilemap(
    map_file: Union[str, Path],
    scaling: float = 1.0,
    layer_options: Optional[Dict[str, Dict[str, Any]]] = None,
    use_spatial_hash: Optional[bool] = None,
    hit_box_algorithm: str = "Simple",
    hit_box_detail: float = 4.5,
) -> TileMap:
    """
    Given a .json map file, loads in and returns a `TileMap` object.

    A TileMap can be created directly using the classes `__init__` function.
    This function exists for ease of use.

    For more clarification on the layer_options key, see the `__init__` function
    of the `TileMap` class

    :param Union[str, Path] map_file: The JSON map file.
    :param float scaling: The global scaling to apply to all Sprite's within the map.
    :param Optional[bool] use_spatial_hash: If set to True, this will make moving a sprite
               in the SpriteList slower, but it will speed up collision detection
               with items in the SpriteList. Great for doing collision detection
               with static walls/platforms.
    :param str hit_box_algorithm: One of 'None', 'Simple' or 'Detailed'.
    :param float hit_box_detail: Float, defaults to 4.5. Used with 'Detailed' to hit box.
    :param Dict[str, Dict[str, Any]] layer_options: Layer specific options for the map.
    """
    return TileMap(
        map_file,
        scaling,
        layer_options,
        use_spatial_hash,
        hit_box_algorithm,
        hit_box_detail,
    )


def read_tmx(map_file: Union[str, Path]) -> pytiled_parser.TiledMap:
    """
    Deprecated function to raise a warning that it has been removed.

    Exists to provide info for outdated code bases.
    """
    raise DeprecationWarning(
        "The read_tmx function has been replaced by the new TileMap class."
    )
