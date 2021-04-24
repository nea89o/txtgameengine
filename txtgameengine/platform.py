import glfw
import typing

import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
from .twod import Texture
from .input.callbacks import CallbackHandler

if typing.TYPE_CHECKING:
    from .app import TxtGameApp


class PlatformError(Exception):
    pass


class PlatformComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    def init(self):
        glfw.init()
        self.init_window()
        glfw.make_context_current(self.app.window)
        glViewport(0, 0, *self.app.size)

    @staticmethod
    def monotonic_time():
        return glfw.get_time()

    @staticmethod
    def enable_vsync():
        glfw.swap_interval(1)

    def init_window(self):
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, glfw.TRUE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        self.app.window = glfw.create_window(
            *self.app.size, self.app.name, None, None)
        if not self.app.window:
            raise PlatformError("Failed to initialize glfw window")

    @property
    def should_close(self) -> bool:
        return glfw.window_should_close(self.app.window)

    @should_close.setter
    def should_close(self, val: bool):
        glfw.set_window_should_close(val, self.app.window)

    @staticmethod
    def poll_events():
        glfw.poll_events()

    @staticmethod
    def init_callbacks(window, handler: CallbackHandler):
        glfw.set_key_callback(window, handler.get_keyboard_input_callback)
        #glfw.set_mouse_button_callback(window, handler.get_mouse_click_callback())
        #glfw.set_cursor_pos_callback(window, handler.get_mouse_move_callback())

    def cleanup(self):
        glfw.destroy_window(self.app.window)
        glfw.terminate()

    def swap_buffers(self):
        glfw.swap_buffers(self.app.window)

    @staticmethod
    def set_clear_color(r, g, b, a):
        glClearColor(r, g, b, a)

    @staticmethod
    def print_debug_message(source, msg_type, msg_id, severity, length, raw, user):
        print('OPENGL ERROR', source, msg_type, msg_id, severity)

    def check_debug(self):
        assert (glGetIntegerv(GL_CONTEXT_FLAGS)
                & GL_CONTEXT_FLAG_DEBUG_BIT) != 0
        glDebugMessageCallback(GLDEBUGPROC(self.print_debug_message), None)

    @staticmethod
    def clear_background(depth_buffer=False):
        glClear(GL_COLOR_BUFFER_BIT | (
                depth_buffer and GL_DEPTH_BUFFER_BIT or 0))


class CoordinateComponent:

    def __init__(self, app: 'TxtGameApp'):
        self.screen_x = [-1, 1]
        self.screen_y = [1, -1]
        self.app = app

    @property
    def pixel_x(self):
        return [0, self.app.size[0]]

    @property
    def pixel_y(self):
        return [0, self.app.size[1]]

    def from_screen_to_pixels(self, x: float, y: float) -> typing.Tuple[int, int]:
        return int(np.interp(x, self.screen_x, self.pixel_x)), \
               int(np.interp(y, self.screen_y, self.pixel_y))

    def from_pixels_to_screen(self, x: int, y: int) -> typing.Tuple[float, float]:
        return np.interp(x, self.pixel_x, self.screen_x), \
               np.interp(y, self.pixel_y, self.screen_y)


class ShaderComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    @staticmethod
    def load_shaders(vertex_file: str, fragment_file: str):
        with open(vertex_file) as fp:
            vertex_source = fp.read()
        with open(fragment_file) as fp:
            fragment_source = fp.read()
        vertex_shader = shaders.compileShader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(
            fragment_source, GL_FRAGMENT_SHADER)
        return shaders.compileProgram(vertex_shader, fragment_shader)

    @staticmethod
    def bind_shader(prog_id: int):
        glUseProgram(prog_id)

    @staticmethod
    def get_uniform_location(prog_id: int, name: str):
        return glGetUniformLocation(prog_id, name)


class RenderComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    @staticmethod
    def setup_vertex_arrays():
        arr = glGenVertexArrays(1)
        glBindVertexArray(arr)

    @staticmethod
    def setup_buffer(arr, mode=GL_STATIC_DRAW):
        buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glBufferData(GL_ARRAY_BUFFER, arr.itemsize *
                     arr.size, arr, mode)
        return buf

    @staticmethod
    def triangle(buf):
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableVertexAttribArray(0)

    def textured_triangle(self, shader_location, texture, triangle, uvs):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture.gl_texid)
        glUniform1i(shader_location, 0)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, uvs)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        self.triangle(triangle)
        glDisableVertexAttribArray(1)

    def setup_texture(self, width: int, height: int, data: np.ndarray):
        tex_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        return tex_id

    def free_texture(self, gl_texid: int):
        glBindTexture(gl_texid, 0)  # unbind the texture
        glDeleteTextures(1, gl_texid)  # actually delete it
