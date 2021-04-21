import glfw
from glfw.GLFW import *

from .app import TxtGameApp


def main():
    glfw.init()
    glfw.window_hint(GLFW_CLIENT_API, GLFW_NO_API)
    window = glfw.create_window(640, 480, "Vulkan window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.destroy_window(window)
    glfw.terminate()


class TestApp(TxtGameApp):
    def __init__(self):
        super().__init__((640, 480), "Vulkan window")
        self.requested_validation_layers += ["VK_LAYER_KHRONOS_validation"]

    def update(self, delta: float):
        super().update(delta)


if __name__ == '__main__':
    # main()
    a = TestApp()
    a.start()
