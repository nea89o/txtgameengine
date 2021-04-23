import numpy as np

from .scenes import SceneTxtGameApp, Scene
from OpenGL.GL import *
from pathlib import Path

shader_path = Path(__file__).parent / 'base_shaders'


class TriangleScene(Scene):
    TRIANGLE_DATA = [
        -1.0, -1.0, 0.0,
        1.0, -1.0, 0.0,
        0.0, 1.0, 0.0,
    ]

    def on_enter(self):
        self.default_shaders = self.app.shaders.load_shaders(
            str(shader_path / 'vertex.glsl'), str(shader_path / 'fragment.glsl'))

        self.tri_buffer = self.app.render.setup_triangle(
            np.array(self.TRIANGLE_DATA, np.float32))
        self.t = 0

    def update(self, delta):
        self.t += delta
        if self.t > 10:
            self.push_scene(EvilTriangleScene)
            self.t = 0
        with self.default_shaders:
            self.app.render.triangle(self.tri_buffer)


class EvilTriangleScene(TriangleScene):
    TRIANGLE_DATA = [
        -1.0, 1.0, 0.0,
        1.0, 1.0, 0.0,
        0.0, -1.0, 0.0,
    ]


class TestApp(SceneTxtGameApp):
    MAIN_SCENE_T = TriangleScene

    def init(self):
        super().init()
        self.render.setup_vertex_arrays()
        # self.platform.check_debug()


if __name__ == '__main__':
    a = TestApp((640, 480), "OpenGL window")
    a.start()
