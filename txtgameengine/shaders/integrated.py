from .shader import Shader
from ..app import base_path

shader_base_path = base_path / 'builtin_shaders'


class BasicShader(Shader):
    UNIFORMS = dict()
    VERTEX_PATH = shader_base_path / 'basic/vertex.glsl'
    FRAGMENT_PATH = shader_base_path / 'basic/fragment.glsl'


class TextureShader(Shader):
    UNIFORMS = dict(textureSampler="textureSampler")
    VERTEX_PATH = shader_base_path / 'texture/vertex.glsl'
    FRAGMENT_PATH = shader_base_path / 'texture/fragment.glsl'
