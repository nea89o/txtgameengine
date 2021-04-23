import typing

if typing.TYPE_CHECKING:
    from ..app import TxtGameApp


class Shader:
    """Wrapper class for a GL program"""

    UNIFORMS: typing.Dict[str, str] = dict()
    VERTEX_PATH: str
    FRAGMENT_PATH: str

    def __init__(self, app: 'TxtGameApp'):
        self.app = app
        self._prog_id = self.app.shaders.load_shaders(self.VERTEX_PATH, self.FRAGMENT_PATH)
        self._is_bound = 0
        self.uniform_locations = {}
        self._fill_uniforms()

    def _fill_uniforms(self):
        with self:
            for prop_name, shader_name in self.UNIFORMS.items():
                self.uniform_locations[prop_name] = \
                    self.app.shaders.get_uniform_location(self._prog_id, shader_name)

    def __getattr__(self, item):
        if item in self.uniform_locations:
            return self.uniform_locations[item]
        raise AttributeError("Shader '%s' has no attribute or uniform named %s" % (type(self).__name__, item))

    def _require_bound(self, required=False):
        assert self._is_bound > 0 or not required
        return self

    def get_uniform_location(self, name: str):
        return self.uniform_locations[name]

    def __enter__(self):
        self._is_bound += 1
        if self._is_bound == 1:
            self.app.shaders.bind_shader(self._prog_id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_bound -= 1
        if self._is_bound == 0:
            self.app.shaders.bind_shader(0)

    def __repr__(self):
        return '<Shader prog_id=%d uniforms=%r>' % (self._prog_id, self.uniform_locations)
