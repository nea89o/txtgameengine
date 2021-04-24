from pathlib import Path
from .input.callbacks import CallbackHandler

EPSILON = 1.e-10
builtin_resource_path = Path(__file__).parent / 'builtin_res'

from .platform import PlatformComponent, RenderComponent, ShaderComponent, CoordinateComponent


class TxtGameApp:
    PLATFORM_CLASS = PlatformComponent
    RENDER_CLASS = RenderComponent
    SHADER_CLASS = ShaderComponent
    COORDINATE_CLASS = CoordinateComponent

    def __init__(self, size: (int, int), name: str):
        self.size = size
        self.name = name
        self.window = None
        self.platform = self.PLATFORM_CLASS(self)
        self.render = self.RENDER_CLASS(self)
        self.shaders = self.SHADER_CLASS(self)
        self.coords = self.COORDINATE_CLASS(self)
        self.should_exit = False
        self.handler = CallbackHandler(self)

    def init(self):
        self.platform.init_callbacks(self.window, self.handler)

    def start(self):
        self.platform.init()
        self.init()
        self.platform.set_clear_color(1, 0, 0.75, 1)
        last_update_time = self.platform.monotonic_time()
        while not (self.platform.should_close or self.should_exit):
            update_time = self.platform.monotonic_time()
            self.platform.poll_events()
            self.update(update_time - last_update_time)
            self.platform.swap_buffers()
            last_update_time = update_time
        self.platform.cleanup()

    def update(self, delta: float):
        print("Running: delta = %.4fs, approx. fps = %ds" % (delta, 1. / (delta or EPSILON)))
        self.platform.clear_background()

    def exit(self):
        self.should_exit = True
