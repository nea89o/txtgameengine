import typing

from .app import TxtGameApp


class SceneTxtGameApp(TxtGameApp):
    MAIN_SCENE_T: typing.Type['Scene'] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_stack = []

    def push_scene(self, scene_t: typing.Type['Scene']):
        if self.scene_stack:
            self.scene_stack[-1].on_pause()
        self.scene_stack += [scene_t(self)]
        self.scene_stack[-1].on_enter()
    
    def pop_scene(self):
        self.scene_stack[-1].on_exit()
        del self.scene_stack[-1]
        if not self.scene_stack:
            self.exit()
            return
        self.scene_stack[-2].on_resume()

    def update(self, delta):
        if not self.scene_stack: # TODO: better lifecycles in TxtGameApp so we dont have to hack this
            self.push_scene(self.MAIN_SCENE_T)
        super().update(delta)
        print("Scene Stack:", ' > '.join(type(x).__name__ for x in self.scene_stack))
        self.scene_stack[-1].update(delta)

class Scene:
    def __init__(self, app: 'SceneTxtGameApp'):
        self.app = app

    def pop_scene(self):
        """Exits this scene and returns control to the parent scene"""
        self.app.pop_scene()

    def push_scene(self, scene_t: typing.Type['Scene']):
        """Pushes a scene type onto the scene stack"""
        self.app.push_scene(scene_t)

    def on_exit(self):
        """Called when the scene is removed from the scene tree"""

    def on_enter(self):
        """Called when the scene is first entered in the scene tree"""
        pass

    def on_pause(self):
        """Called when another scene takes update priority over this scene without unloading this scene"""
        pass

    def on_resume(self):
        """Called when this scene takes over update priority after previously using it to another scene"""
        pass

    def update(self, delta: float):
        """Render the current scene"""
        pass
