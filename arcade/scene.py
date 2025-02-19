"""
This module provides a Scene Manager class.

This class let's you add Sprites/SpriteLists to a scene and give them
a name, as well as control the draw order. In addition it provides a
helper function to create a Scene directly from a TileMap object.
"""

from typing import Dict, List, Optional

from arcade import Sprite, SpriteList
from arcade.tilemap import TileMap


class Scene:
    """
    Class that represents a `scene` object. Most games will use Scenes to render their Sprites.
    For examples on how to use this class, see:
    https://arcade.academy/examples/index.html#scenes

    Attributes:
        :sprite_lists: A list of `SpriteList` objects. The order of this list is the
                       order in which they will be drawn.
        :name_mapping: A dictionary of `SpriteList` objects. This contains the same lists
                       as the `sprite_lists` attribute, but is a mapping of them by name. This is
                       not necessarily in the same order as the `sprite_lists` attribute.
    """

    def __init__(self) -> None:
        """
        Create a new Scene.
        """
        self.sprite_lists: List[SpriteList] = []
        self.name_mapping: Dict[str, SpriteList] = {}

    @classmethod
    def from_tilemap(cls, tilemap: TileMap) -> "Scene":
        """
        Create a new Scene from a `TileMap` object.

        This will look at all the SpriteLists in a TileMap object and create
        a Scene with them. This will automatically keep SpriteLists in the same
        order as they are defined in the TileMap class, which is the order that
        they are defined within Tiled.

        :param TileMap tilemap: The `TileMap` object to create the scene from.
        """
        scene = cls()
        for name, sprite_list in tilemap.sprite_lists.items():
            scene.add_sprite_list(name=name, sprite_list=sprite_list)
        return scene

    def get_sprite_list(self, name: str) -> SpriteList:
        """
        Helper function to retrieve a `SpriteList` by name.

        The name mapping can be accessed directly, this is just here for ease of use.

        :param str name: The name of the `SpriteList` to retrieve.
        """
        return self.name_mapping[name]

    def add_sprite(self, name: str, sprite: Sprite) -> None:
        """
        Add a Sprite to a SpriteList in the Scene with the specified name.

        If the desired SpriteList does not exist, it will automatically be created
        and added to the Scene. This will default the SpriteList to be added to the end
        of the draw order, and created with no extra options like using spatial hashing.

        If you need more control over where the SpriteList goes or need it to use Spatial Hash,
        then the SpriteList should be added separately and then have the Sprites added.

        :param str name: The name of the `SpriteList` to add to or create.
        :param Sprite sprite: The `Sprite` to add.
        """
        if name in self.name_mapping:
            self.name_mapping[name].append(sprite)
        else:
            new_list = SpriteList()
            new_list.append(sprite)
            self.add_sprite_list(name=name, sprite_list=new_list)

    def add_sprite_list(
        self,
        name: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name.

        This will add a new SpriteList to the scene at the end of the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if not sprite_list:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        self.sprite_lists.append(sprite_list)

    def add_sprite_list_before(
        self,
        name: str,
        before: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name before a specific SpriteList.

        This will add a new SpriteList to the scene before the specified SpriteList in the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param str before: The name of the SpriteList to place this one before.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if not sprite_list:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        before_list = self.name_mapping[before]
        index = self.sprite_lists.index(before_list) - 1
        self.sprite_lists.insert(index, sprite_list)

    def add_sprite_list_after(
        self,
        name: str,
        after: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name after a specific SpriteList.

        This will add a new SpriteList to the scene after the specified SpriteList in the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param str after: The name of the SpriteList to place this one after.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if not sprite_list:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        after_list = self.name_mapping[after]
        index = self.sprite_lists.index(after_list)
        self.sprite_lists.insert(index, sprite_list)

    def remove_sprite_list_by_name(
        self,
        name: str,
    ) -> None:
        """
        Remove a SpriteList by it's name.

        This function serves to completely remove the SpriteList from the Scene.

        :param str name: The name of the SpriteList to remove.
        """
        sprite_list = self.name_mapping[name]
        self.sprite_lists.remove(sprite_list)
        del self.name_mapping[name]

    def remove_sprite_list_by_object(self, sprite_list: SpriteList) -> None:
        self.sprite_lists.remove(sprite_list)
        self.name_mapping = {
            key: val for key, val in self.name_mapping.items() if val != sprite_list
        }

    def update(self, names: Optional[List[str]] = None) -> None:
        """
        Used to update SpriteLists contained in the scene.

        If `names` parameter is provided then only the specified spritelists
        will be updated. If `names` is not provided, then every SpriteList
        in the scene will be updated.

        :param Optional[List[str]] names: A list of names of SpriteLists to update.
        """
        if names:
            for name in names:
                self.name_mapping[name].update()
            return

        for sprite_list in self.sprite_lists:
            sprite_list.update()

    def update_animation(
        self, delta_time: float, names: Optional[List[str]] = None
    ) -> None:
        """
        Used to update the animation of SpriteLists contained in the scene.

        If `names` parameter is provided then only the specified spritelists
        will be updated. If `names` is not provided, then every SpriteList
        in the scene will be updated.

        :param float delta_time: The delta time for the update.
        :param Optional[List[str]] names: A list of names of SpriteLists to update.
        """
        if names:
            for name in names:
                self.name_mapping[name].update_animation(delta_time)
            return

        for sprite_list in self.sprite_lists:
            sprite_list.update_animation(delta_time)

    def draw(self, names: Optional[List[str]] = None, **kwargs) -> None:
        """
        Draw the Scene.

        If `names` parameter is provided then only the specified SpriteLists
        will be drawn. They will be drawn in the order that the names in the
        list were arranged. If `names` is not provided, then every SpriteList
        in the scene will be drawn according the order of the main sprite_lists
        attribute of the Scene.

        :param Optional[List[str]] names: A list of names of SpriteLists to draw.
        :param filter: Optional parameter to set OpenGL filter, such as
                       `gl.GL_NEAREST` to avoid smoothing.
        :param blend_function: Optional parameter to set the OpenGL blend function
            used for drawing the sprite list, such as `arcade.Window.ctx.BLEND_ADDITIVE`
            or `arcade.Window.ctx.BLEND_DEFAULT`
        """

        if names:
            for name in names:
                self.name_mapping[name].draw(**kwargs)
            return

        for sprite_list in self.sprite_lists:
            sprite_list.draw(**kwargs)
