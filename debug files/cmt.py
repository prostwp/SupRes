# from pynput import keyboard
# import threading
#
# class VKeyHandler:
#     def __init__(self):
#         self.v_key_pressed = threading.Event()
#         self.listener = keyboard.Listener(on_press=self.on_press)
#
#     def on_press(self, key):
#         try:
#             if key.char == 'v':
#                 self.v_key_pressed.set()
#         except AttributeError:
#             pass
#     class VKeyHandler:
#         def __init__(self):
#             self.v_key_pressed = threading.Event()
#             self.listener = keyboard.Listener(on_press=self.on_press)
#
#         def on_press(self, key):
#             try:
#                 if key.char == 'v':
#                     self.v_key_pressed.set()
#             except AttributeError:
#                 pass
#
#         def wait_for_v_key(self):
#             self.v_key_pressed.clear()
#             self.listener.start()
#             self.v_key_pressed.wait()
#             self.listener.stop()
#
#     handler = VKeyHandler()
#     print("Ожидание нажатия клавиши V...")
#     handler.wait_for_v_key()
#     print("Клавиша V нажата!")
#
#     def wait_for_v_key(self):
#         self.v_key_pressed.clear()
#         self.listener.start()
#         self.v_key_pressed.wait()
#         self.listener.stop()
#
# handler = VKeyHandler()
# print("Ожидание нажатия клавиши V...")
# handler.wait_for_v_key()
# print("Клавиша V нажата!")
# for i in range(1,9):
#     print(i)
import time
from pynput.keyboard import Controller, Key

keyboard = Controller()
os_name = "Windows"  # Или "Mac" в зависимости от ОС

def write_bold(text):
    def toggle_bold():
        modifier_key = Key.ctrl if os_name == "Windows" else Key.cmd
        keyboard.press(modifier_key)
        keyboard.press('b')
        keyboard.release('b')
        keyboard.release(modifier_key)
        time.sleep(0.2)

    toggle_bold()  # Включаем жирный
    write(text)  # Пишем текст
    toggle_bold()  # Выключаем жирный


def write(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.05)  # Задержка между нажатиями клавиш


# Пример использования
write_bold("Hello, World!")
