import ctypes
import time

# Códigos virtuais das teclas multimídia
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002


def press_key(vk_code):
    """Simula pressionar e soltar uma tecla multimídia."""
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


def play_pause():
    """Play/Pause"""
    press_key(VK_MEDIA_PLAY_PAUSE)


def next_track():
    """Próxima música"""
    press_key(VK_MEDIA_NEXT_TRACK)


def previous_track():
    """Música anterior"""
    press_key(VK_MEDIA_PREV_TRACK)


# --- Exemplo de uso ---
if __name__ == "__main__":
    print("Play/Pause...")
    play_pause()
    time.sleep(2)

    print("Próxima música...")
    next_track()
    time.sleep(2)

    print("Anterior...")
    previous_track()
