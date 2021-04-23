import typing
from PIL import Image
import numpy as np

TEXTURE_FOLDER = 'txtgameengine/res/textures/'

if typing.TYPE_CHECKING:
    from ..app import TxtGameApp


class Texture:
    def __init__(self, app: 'TxtGameApp', path: str):
        self.app = app
        self.path = path
        self._load_from_disk()
        self._bind_to_gl()

    def _load_from_disk(self):
        self.image = Image.open(TEXTURE_FOLDER + self.path)
        self.width, self.height = self.image.size

    def _bind_to_gl(self):
        imagedata = np.array(list(self.image.getdata()), np.uint8)
        self.gl_texid = self.app.render.setup_texture(self.width, self.height, imagedata)

    def free(self):
        self.app.render.free_texture(self.gl_texid)