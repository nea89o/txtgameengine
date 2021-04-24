import numpy as np

from .fonts import TextRenderer, BitmapFont
from .scenes import SceneTxtGameApp, Scene
from pathlib import Path
from .shaders import TextureShader
from .twod.textures import Texture, TEXTURE_FOLDER
from.input.keyboard import ModKey, KeyboardEvent

shader_path = Path(__file__).parent / 'shaders'


class TriangleScene(Scene):
    TRIANGLE_DATA = [
        -1.0, -1.0,
        1.0, -1.0,
        0.0, 1.0,
    ]

    def on_enter(self):
        self.default_shaders = self.app.shaders.load_shaders(
            str(shader_path / 'basic/vertex.glsl'), str(shader_path / 'basic/fragment.glsl'))

        self.tri_buffer = self.app.render.setup_buffer(
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
        -1.0, 1.0,
        1.0, 1.0,
        0.0, -1.0,
    ]

    def update(self, delta):
        super().update(delta)
        self.t = 0


class TextureScene(Scene):
    def on_enter(self):
        self.texture_shaders = TextureShader(self.app)
        self.texture = Texture(self.app, TEXTURE_FOLDER / 'test_image.png')
        self.triangle = self.app.render.setup_buffer(
            np.array([
                -1.0, 1.0,
                1.0, 1.0,
                -1.0, -1.0,
                1.0, -1.0,
            ], np.float32))
        self.uvs = self.app.render.setup_buffer(
            np.array([
                0, 0,
                1, 0,
                0, 1,
                1, 1,
            ], np.float32))
        self.text_renderer = TextRenderer(self.app)
        self.text_renderer.use_font(BitmapFont.fira_mono(self.app))

    def update(self, delta: float):
        with self.texture_shaders:
            self.app.render.bind_texture(self.texture_shaders.textureSampler, self.texture)
            self.app.render.textured_triangle(self.triangle, self.uvs, 4)
        self.text_renderer.render_text(0, 0, "HEE")


class TestApp(SceneTxtGameApp):
    MAIN_SCENE_T = TextureScene

    def init(self):
        super().init()
        self.render.setup_vertex_arrays()
        self.handler.register_keyboard_callback(self.handler.keyboard_callback()
                                                .with_mod_key(ModKey.CONTROL)
                                                .build(lambda key_event: print(key_event.keycode)))
        # self.platform.check_debug()



if __name__ == '__main__':
    a = TestApp((640, 480), "OpenGL window")
    a.start()
