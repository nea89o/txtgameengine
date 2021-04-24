import os
import typing
from PIL import Image
import numpy as np
from ..app import builtin_resource_path

TEXTURE_FOLDER = builtin_resource_path / 'textures'

if typing.TYPE_CHECKING:
    from ..app import TxtGameApp


class Texture:
    def __init__(self, app: 'TxtGameApp', load: typing.Union[os.PathLike, Image.Image]):
        self.app = app
        self.load = load
        self._bind_to_gl()

    def _bind_to_gl(self):
        if isinstance(self.load, Image.Image):
            image = self.load
        else:
            image = Image.open(str(self.load))
        self.width, self.height = image.size
        image = image.convert('RGBA')
        imagedata = np.array(list(image.getdata()), np.uint8)
        self.gl_texid = self.app.render.setup_texture(self.width, self.height, imagedata)
        image.close()

    @property
    def size(self):
        return self.width, self.height

    def uvs_from_pixels(self, x: int, y: int) -> typing.Tuple[float, float]:
        return self.app.coords.from_pixels_to_uvs(self.size, x, y)

    def free(self):
        self.app.render.free_texture(self.gl_texid)
