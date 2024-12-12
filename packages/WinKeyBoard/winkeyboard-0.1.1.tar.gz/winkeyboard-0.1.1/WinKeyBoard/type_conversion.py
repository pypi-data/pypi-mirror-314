import ctypes

class VK_:
    def __init__(self, VK_CODE, VK_NAME, CHAR):
        self.CHAR = CHAR
        self.VK_CODE = VK_CODE
        self.VK_NAME = VK_NAME
    
    def get_CHAR(self):
        return self.CHAR
    
    def get_VK_CODE(self):
        return self.VK_CODE
    
    def get_VK_NAME(self):
        return self.VK_NAME
    
    def get_SCAN_CODE(self):
        return VK_CODE_to_SCAN_CODE(self.VK_CODE)
    
    def to_pynput_key(self):
        import pynput
        keydict = {
            0x08 : pynput.keyboard.Key.backspace,
            0x09 : pynput.keyboard.Key.tab,
            0x0D : pynput.keyboard.Key.enter,
            0x10 : pynput.keyboard.Key.shift,
            0x11 : pynput.keyboard.Key.ctrl,
            0x12 : pynput.keyboard.Key.alt,
            0x13 : pynput.keyboard.Key.pause,
            0x14 : pynput.keyboard.Key.caps_lock,
            0x1B : pynput.keyboard.Key.esc,
            0x20 : pynput.keyboard.Key.space,
            0x21 : pynput.keyboard.Key.page_up,
            0x22 : pynput.keyboard.Key.page_down,
            0x23 : pynput.keyboard.Key.end,
            0x24 : pynput.keyboard.Key.home,
            0x25 : pynput.keyboard.Key.left,
            0x26 : pynput.keyboard.Key.up,
            0x27 : pynput.keyboard.Key.right,
            0x28 : pynput.keyboard.Key.down,
            0x2C : pynput.keyboard.Key.print_screen,
            0x2D : pynput.keyboard.Key.insert,
            0x2E : pynput.keyboard.Key.delete,
            0x5B : pynput.keyboard.Key.cmd_l,
            0x5C : pynput.keyboard.Key.cmd_r,
            0x5D : pynput.keyboard.Key.menu,
            0x70 : pynput.keyboard.Key.f1,
            0x71 : pynput.keyboard.Key.f2,
            0x72 : pynput.keyboard.Key.f3,
            0x73 : pynput.keyboard.Key.f4,
            0x74 : pynput.keyboard.Key.f5,
            0x75 : pynput.keyboard.Key.f6,
            0x76 : pynput.keyboard.Key.f7,
            0x77 : pynput.keyboard.Key.f8,
            0x78 : pynput.keyboard.Key.f9,
            0x79 : pynput.keyboard.Key.f10,
            0x7A : pynput.keyboard.Key.f11,
            0x7B : pynput.keyboard.Key.f12,
            0x7C : pynput.keyboard.Key.f13,
            0x7D : pynput.keyboard.Key.f14,
            0x7E : pynput.keyboard.Key.f15,
            0x7F : pynput.keyboard.Key.f16,
            0x80 : pynput.keyboard.Key.f17,
            0x81 : pynput.keyboard.Key.f18,
            0x82 : pynput.keyboard.Key.f19,
            0x83 : pynput.keyboard.Key.f20,
            0x84 : pynput.keyboard.Key.f21,
            0x85 : pynput.keyboard.Key.f22,
            0x86 : pynput.keyboard.Key.f23,
            0x87 : pynput.keyboard.Key.f24,
            0x90 : pynput.keyboard.Key.num_lock,
            0x91 : pynput.keyboard.Key.scroll_lock,
            0x90 : pynput.keyboard.Key.num_lock,
            0x97 : pynput.keyboard.Key.media_previous,
            0x98 : pynput.keyboard.Key.media_next,
            0x99 : pynput.keyboard.Key.media_play_pause,
            0x9B : pynput.keyboard.Key.media_volume_mute,
            0x9C : pynput.keyboard.Key.media_volume_down,
            0x9D : pynput.keyboard.Key.media_volume_up,
            0xA0 : pynput.keyboard.Key.shift_l,
            0xA1 : pynput.keyboard.Key.shift_r,
            0xA2 : pynput.keyboard.Key.ctrl_l,
            0xA3 : pynput.keyboard.Key.ctrl_r,
            0xA4 : pynput.keyboard.Key.alt_l,
            0xA5 : pynput.keyboard.Key.alt_r,
            0xAD : pynput.keyboard.Key.media_volume_mute,
            0xAE : pynput.keyboard.Key.media_volume_down,
            0xAF : pynput.keyboard.Key.media_volume_up,
            0xB0 : pynput.keyboard.Key.media_next,
            0xB1 : pynput.keyboard.Key.media_previous,
            0xB3 : pynput.keyboard.Key.media_play_pause
        }
        if self.VK_CODE in keydict:
            return keydict[self.VK_CODE]
        return pynput.keyboard.KeyCode.from_vk(self.VK_CODE)
        
def VK_CODE_to_SCAN_CODE(vk_code : int) -> int:
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    scan_code = user32.MapVirtualKeyW(vk_code, 0)
    return scan_code

def fromVK_CODE(VK_CODE) -> VK_:
    """
    将虚拟键码转换为VK_对象。
    """
    from . import VK as VK_List
    for var_name in dir(VK_List):
        if not var_name.startswith('_') and not var_name.endswith('_') :
            var_value = getattr(VK_List, var_name)
            if var_value.get_VK_CODE() == VK_CODE:
                return var_value
    return None

def fromCHAR(CHAR) -> VK_:
    """
    将字符转换为VK_对象。
    """
    from . import VK as VK_List
    for var_name in dir(VK_List):
        if not var_name.startswith('_') and not var_name.endswith('_') :
            var_value = getattr(VK_List, var_name)
            if var_value.get_CHAR() == CHAR:
                return var_value
    return None

def fromSCAN_CODE(SCAN_CODE) -> VK_:
    """
    将扫描码转换为VK_对象。
    """
    from . import VK as VK_List
    for var_name in dir(VK_List):
        if not var_name.startswith('_') and not var_name.endswith('_') :
            var_value = getattr(VK_List, var_name)
            if SCAN_CODE == var_value.get_SCAN_CODE():
                return var_value
    return None