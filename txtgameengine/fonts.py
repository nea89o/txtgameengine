from abc import ABC
from dataclasses import dataclass
from typing import Optional


class Font(ABC):
    def get_glyph(self, char: str) -> Optional['Glyph']:
        raise NotImplementedError()

    @property
    def font(self):
        raise NotImplementedError()


@dataclass
class Glyph:
    font: 'Font'
    x_texture_offset: int
    y_texture_offset: int
    x_width: int
    y_width: int


class MonospacedFont(Font):
    def get_glyph(self, char: str):
        pass
