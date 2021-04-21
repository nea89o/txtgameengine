import glfw
from vulkan import *
import time


class PlatformError(Exception):
    pass


class QueueFamilies:
    graphics_i: int
    graphics: object


class PlatformComponent:
    def __init__(self, app: 'TxtGameApp'):
        self.app = app

    def init(self):
        glfw.init()
        self.init_vulkan()
        self.init_window()

    def init_vulkan(self):
        self.create_instance()
        self.pick_physical_device()
        self.create_logical_device()

    def is_device_suitable(self, device):
        return 1

    def pick_physical_device(self):
        devices = [(d, self.is_device_suitable(d))
                   for d in vkEnumeratePhysicalDevices(self.instance)]
        if len(devices) == 0:
            raise PlatformError("No vulkan devices available.")
        device, rating = sorted(devices, key=lambda x: x[1])[-1]
        if rating < 0:
            raise PlatformError("No suitable devices available.")
        self.physical_device = device
        self.find_queue_families()

    def find_queue_families(self):
        self.queues = QueueFamilies()
        for i, queue_family in enumerate(vkGetPhysicalDeviceQueueFamilyProperties(self.physical_device)):
            if queue_family.queueFlags & VK_QUEUE_GRAPHICS_BIT:
                self.queues.graphics_i = i

    def create_logical_device(self):
        queue_create_info = [VkDeviceQueueCreateInfo(
            queueFamilyIndex=self.queues.graphics_i,
            queueCount=1,
            pQueuePriorities=[1],
            flags=0,
        )]
        device_create = VkDeviceCreateInfo(
            pQueueCreateInfos=queue_create_info,
            pEnabledFeatures=vkGetPhysicalDeviceFeatures(self.physical_device),
            flags=0,
            ppEnabledLayerNames=self.layers,
            ppEnabledExtensionNames=[],
        )
        self.logical_device = vkCreateDevice(
            self.physical_device, device_create, None)
        self.queues.graphic = vkGetDeviceQueue(
            device=self.logical_device,
            queueFamilyIndex=self.queues.graphics_i,
            queueIndex=0,
        )

    def create_instance(self):
        app_info = VkApplicationInfo(
            pApplicationName=self.app.name,
            applicationVersion=VK_MAKE_VERSION(1, 0, 0),
            pEngineName="TxtGameEngine",
            engineVersion=VK_MAKE_VERSION(1, 0, 0),
            apiVersion=VK_API_VERSION_1_0,
        )
        extensions = glfw.get_required_instance_extensions()
        present_layers = vkEnumerateInstanceLayerProperties()
        missing_layers = set(self.app.requested_validation_layers) - \
            set(l.layerName for l in present_layers)
        if missing_layers:
            raise PlatformError(
                "Missing validation layers: "+str(missing_layers))
        self.layers = self.app.requested_validation_layers
        createInfo = VkInstanceCreateInfo(
            pApplicationInfo=app_info,
            flags=0,
            enabledExtensionCount=len(extensions),
            ppEnabledExtensionNames=extensions,
            enabledLayerCount=len(self.layers),
            ppEnabledLayerNames=self.layers,
        )
        self.instance = vkCreateInstance(createInfo, None)

    def init_window(self):
        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
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

    def poll_events(self):
        glfw.poll_events()

    def cleanup(self):
        vkDestroyDevice(self.logical_device)
        vkDestroyInstance(self.instance)
        glfw.destroy_window(window)
        glfw.terminate()


class TxtGameApp:
    PLATFORM_CLASS = PlatformComponent

    def __init__(self, size: (int, int), name: str):
        self.size = size
        self.name = name
        self.platform: self.PLATFORM_CLASS = self.PLATFORM_CLASS(self)
        self.requested_validation_layers = []

    def start(self):
        self.platform.init()
        last_update_time = time.monotonic()
        while not self.platform.should_close:
            update_time = time.monotonic()
            self.platform.poll_events()
            self.update(update_time - last_update_time)
            last_update_time = update_time

    def update(self, delta: float):
        raise NotImplementedError
