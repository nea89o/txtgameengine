import typing

if typing.TYPE_CHECKING:
    from ..app import TxtGameApp


class Texture:
    def __init__(self, app: 'TxtGameApp', gl_texid: int):
        self.app = app
        self.gl_texid = gl_texid

