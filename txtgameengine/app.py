import time

from .platform import PlatformComponent

EPSILON = 1.e-10


class TxtGameApp:
    PLATFORM_CLASS = PlatformComponent

    def __init__(self, size: (int, int), name: str):
        self.size = size
        self.name = name
        self.platform = self.PLATFORM_CLASS(self)
        self.requested_validation_layers = []

    def start(self):
        self.platform.init()
        self.platform.set_clear_color(1, 0, 0.75, 1)
        last_update_time = self.platform.monotonic_time()
        while not self.platform.should_close:
            update_time = self.platform.monotonic_time()
            self.platform.poll_events()
            self.update(update_time - last_update_time)
            self.platform.swap_buffers()
            last_update_time = update_time
        self.platform.cleanup()

    def update(self, delta: float):
        print("Running: delta = %.4fs, approx. fps = %ds" % (delta, 1. / (delta or EPSILON)))
        self.platform.clear_background()
