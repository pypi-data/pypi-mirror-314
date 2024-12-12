name = "WindowsKeyBoard"
from . import VK, key_controller, type_conversion

def wait(ms: float):
    import time
    time.sleep(ms/1000)