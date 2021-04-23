import os
from abc import ABC
from dataclasses import dataclass
from typing import Optional
import typing
import xml.dom.minidom as minidom

if typing.TYPE_CHECKING:
    from .twod import Texture
    from .app import TxtGameApp


class Font(ABC):
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
    def __init__(self, texture: Texture, xml_path: str):
        self.texture = texture
        dom = minidom.parse(xml_path)
        for char in dom.getElementsByTagName('Char'):
            code = char.attributes['code'].value
            width = char.attributes['width'].value
            x_render_offset, y_render_offset = char.attributes['offset'].value.split(' ')
            x_texture_offset, y_texture_offset, x_texture_width, y_texture_width = char.attributes['rect'].split(' ')
            self.glyphs[code] = \
                Glyph(self, int(x_texture_offset), int(y_texture_offset), int(x_texture_width), int(y_texture_width),
                      int(x_render_offset), int(y_render_offset), int(width))

    @classmethod
    def load(cls, app: 'TxtGameApp', image_path: os.PathLike, xml_path: os.PathLike):
        from .twod import Texture
        return cls(Texture(app, image_path), xml_path)


class TextRenderer:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    def use_font(self, font: Font):
        self.font = font
