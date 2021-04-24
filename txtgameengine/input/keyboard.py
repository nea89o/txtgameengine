from enum import IntFlag
import glfw
import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from ..scenes import Scene

    SceneLike = typing.TypeAlias('SceneLike', typing.Union[Scene, typing.Type[Scene]])


class ModKey(IntFlag):
    SHIFT = glfw.MOD_SHIFT
    CONTROL = glfw.MOD_CONTROL
    ALT = glfw.MOD_ALT
    SUPER = glfw.MOD_SUPER


@dataclass
class KeyboardEvent:
    window: typing.Any
    keycode: int
    scancode: int
    action: int
    mod_keys: int

    def has_modkey(self, modkey: ModKey):
        return bool(self.mod_keys & modkey)


class KeyboardCallbackBuilder:
    def __init__(self, app):
        self.app = app
        self.scene = None
        self.required_mod_keys = ModKey(0)

    def build(self, callback: typing.Callable[[KeyboardEvent], None]):
        KeyboardCallback(self.required_mod_keys, callback)

    def only_in_scene(self, scene: 'SceneLike'):
        self.scene = scene
        return self

    def with_mod_key(self, mod_key: ModKey):
        self.required_mod_keys |= mod_key
        return self


class KeyboardCallback:
    def __init__(self, required_mod_keys, callback: typing.Callable[[KeyboardEvent], None]):
        self.required_mod_keys = required_mod_keys
        self.callback = callback
