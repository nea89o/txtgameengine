import glfw
import typing

from OpenGL.GL import *
import OpenGL.GL.shaders as shaders

if typing.TYPE_CHECKING:
    from .app import TxtGameApp


class PlatformError(Exception):
    pass


class PlatformComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app
        self.window = None

    def init(self):
        glfw.init()
        self.init_window()
        glfw.make_context_current(self.window)
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
        self.window = glfw.create_window(
            *self.app.size, self.app.name, None, None)
        if not self.window:
            raise PlatformError("Failed to initialize glfw window")

    @property
    def should_close(self) -> bool:
        return glfw.window_should_close(self.window)

    @should_close.setter
    def should_close(self, val: bool):
        glfw.set_window_should_close(val)

    @staticmethod
    def poll_events():
        glfw.poll_events()

    def cleanup(self):
        glfw.destroy_window(self.window)
        glfw.terminate()

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

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


class ShaderComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    @staticmethod
    def load_shaders(vertex_file, fragment_file):
        with open(vertex_file) as fp:
            vertex_source = fp.read()
        with open(fragment_file) as fp:
            fragment_source = fp.read()
        vertex_shader = shaders.compileShader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(
            fragment_source, GL_FRAGMENT_SHADER)
        return shaders.compileProgram(vertex_shader, fragment_shader)


class RenderComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    @staticmethod
    def setup_vertex_arrays():
        arr = glGenVertexArrays(1)
        glBindVertexArray(arr)

    @staticmethod
    def setup_triangle(arr):
        buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glBufferData(GL_ARRAY_BUFFER, arr.itemsize *
                     arr.size, arr, GL_STATIC_DRAW)
        return buf

    @staticmethod
    def triangle(buf):
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableVertexAttribArray(0)
