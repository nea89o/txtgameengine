import glfw
from vulkan import *
from glfw.GLFW import *

from txtgameengine.app import TxtGameApp


def main():
    glfw.init()
    glfw.window_hint(GLFW_CLIENT_API, GLFW_NO_API)
    window = glfw.create_window(640, 480, "Vulkan window", None, None)
    if not window:
        glfw.terminate()
        return
    extensions = vkEnumerateInstanceExtensionProperties(None)
    print([e.name for e in extensions])
    while not glfw.window_should_close(window):
        glfw.poll_events()
    glfw.destroy_window(window)
    glfw.terminate()


class TestApp(TxtGameApp):
    def __init__(self):
        super().__init__((640, 480), "Vulkan window")
        self.requested_validation_layers += ["VK_LAYER_KHRONOS_validation"]

    def update(self, delta: float):
        pass


if __name__ == '__main__':
    # main()
    a = TestApp()
    a.start()
