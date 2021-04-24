import typing
from .keyboard import ModKey, KeyboardCallback, KeyboardEvent, KeyboardCallbackBuilder

if typing.TYPE_CHECKING:
    from ..app import TxtGameApp


class CallbackHandler:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app
        self.keyboard_callbacks: typing.List[KeyboardCallback] = []

    def register_keyboard_callback(self, callback: KeyboardCallback):
        self.keyboard_callbacks.append(callback)

    def get_keyboard_input_callback(self, window: typing.Any, keycode: int, scancode: int, action: int, mod_keys: int):
        event = KeyboardEvent(window, keycode, scancode, action, ModKey(mod_keys))
        for callback in self.keyboard_callbacks:
            if event.mod_keys == callback.required_mod_keys:
                continue

            callback.callback(event)

    def get_mouse_move_callback(self, window: typing.Any, pos_x: float, pos_y: float):
        pass

    def get_mouse_click_callback(self, window: typing.Any, button: int, action: int, mod_keys: int):
        pass

    def keyboard_callback(self) -> KeyboardCallbackBuilder:
        return KeyboardCallbackBuilder(self.app)
