from pynput import keyboard
import threading

class VKeyHandler:
    def __init__(self):
        self.v_key_pressed = threading.Event()
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            if key.char == 'v':
                self.v_key_pressed.set()
        except AttributeError:
            pass

    def wait_for_v_key(self):
        self.v_key_pressed.clear()
        self.listener.start()
        self.v_key_pressed.wait()
        self.listener.stop()

