import os
from abc import ABC
from dataclasses import dataclass
from typing import Optional
import typing
import xml.dom.minidom as minidom

from .shaders import FontShader

if typing.TYPE_CHECKING:
    from .twod import Texture
    from .app import TxtGameApp


class Font(ABC):
    texture: 'Texture'

    def __init__(self):
        self.glyphs = dict()

    def get_glyph(self, char: str) -> Optional['Glyph']:
        return self.glyphs.get(char)


@dataclass
class Glyph:
    font: 'Font'
    x_texture_offset: int
    y_texture_offset: int
    x_texture_width: int
    y_texture_width: int
    x_render_offset: int
    y_render_offset: int
    x_advance: int


class BitmapFont(Font):
    def __init__(self, texture: 'Texture', xml_path: str):
        super().__init__()
        self.texture = texture
        dom = minidom.parse(str(xml_path))
        for char in dom.getElementsByTagName('Char'):
            code = char.attributes['code'].value
            width = char.attributes['width'].value
            x_render_offset, y_render_offset = char.attributes['offset'].value.split(' ')
            x_texture_offset, y_texture_offset, x_texture_width, y_texture_width = char.attributes['rect'].value.split(' ')
            self.glyphs[code] = \
                Glyph(self, int(x_texture_offset), int(y_texture_offset), int(x_texture_width), int(y_texture_width),
                      int(x_render_offset), int(y_render_offset), int(width))

    @classmethod
    def load(cls, app: 'TxtGameApp', image_path: os.PathLike, xml_path: os.PathLike):
        from .twod import Texture
        return cls(Texture(app, image_path), xml_path)

    @classmethod
    def fira_mono(cls, app: 'TxtGameApp'):
        from .app import builtin_resource_path
        return cls.load(app, builtin_resource_path / 'fonts/fira_code/regular.png',
                        builtin_resource_path / 'fonts/fira_code/regular.xml')


class TextRenderer:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app
        self.font: Font = None
        self.shader = FontShader(app)

    def use_font(self, font: Font):
        self.font = font

    def render_text(self, x: int, y: int, text: str) -> typing.Tuple[int, int]:
        """No support for newlines"""
        if self.font is None:
            raise ValueError("No font set")
        glyphs = list(map(self.font.get_glyph, text))
        missing = [t for t, g in zip(text, glyphs) if g is None]
        if missing:
            raise ValueError("No glyph found for character '%s'" % missing[0])
        with self.shader:
            self.app.render.bind_texture(self.shader.textureSampler, self.font.texture)
            for glyph in glyphs:
                x, y = self._render_glyph(glyph, x, y)
        return x, y

    def _render_glyph(self, glyph: Glyph, x: int, y: int) -> typing.Tuple[int, int]:
        low_x = x + glyph.x_render_offset
        high_x = low_x + glyph.x_texture_width
        low_y = y + glyph.y_render_offset
        high_y = low_y + glyph.y_texture_width
        low_x, low_y = self.app.coords.from_pixels_to_screen(low_x, low_y)
        high_x, high_y = self.app.coords.from_pixels_to_screen(high_x, high_y)
        tex_low_x = glyph.x_texture_offset
        tex_high_x = tex_low_x + glyph.x_texture_width
        tex_low_y = glyph.y_texture_offset
        tex_high_y = tex_low_y + glyph.y_texture_width
        tex_low_x, tex_low_y = self.app.coords.from_pixels_to_screen(tex_low_x, tex_low_y)
        tex_high_x, tex_high_y = self.app.coords.from_pixels_to_screen(tex_high_x, tex_high_y)
        render = self.app.render.setup_buffer([
            low_x, low_y,
            high_x, low_y,
            low_x, high_y,
            high_x, high_y,
        ])
        uvs = self.app.render.setup_buffer([
            tex_low_x, tex_low_y,
            tex_high_x, tex_low_y,
            tex_low_x, tex_high_y,
            tex_high_x, tex_high_y,
        ])
        self.app.render.textured_triangle(render, uvs, 4)
        return x + glyph.x_advance, y
