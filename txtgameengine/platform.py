import glfw
import typing

from OpenGL import GL

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

    @staticmethod
    def monotonic_time():
        return glfw.get_time()

    @staticmethod
    def enable_vsync():
        glfw.swap_interval(1)

    def init_window(self):
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
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
        GL.glClearColor(r, g, b, a)

    @staticmethod
    def clear_background(depth_buffer=False):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | (depth_buffer and GL.GL_DEPTH_BUFFER_BIT or 0))
