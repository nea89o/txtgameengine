import numpy as np

from .app import TxtGameApp
from OpenGL.GL import *


class TestApp(TxtGameApp):
    def __init__(self):
        super().__init__((640, 480), "OpenGL window")

    def init(self):
        self.render.setup_vertex_arrays()
        #self.platform.check_debug()
        self.default_shaders = self.shaders.load_shaders(
            'base_shaders/vertex.glsl', 'base_shaders/fragment.glsl')
        self.tri_buffer = self.render.setup_triangle(np.array([
            -1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            0.0,  1.0, 0.0,
        ], np.float32))

    def update(self, delta: float):
        super().update(delta)
        with self.default_shaders:
            self.render.triangle(self.tri_buffer)
        


if __name__ == '__main__':
    a = TestApp()
    a.start()
