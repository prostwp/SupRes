from file_check import SupResAutomation
import os
from sup_res_keys import keys
import webbrowser
import subprocess
from pynput.keyboard import Controller, Key
import pyautogui
import platform
from datetime import datetime, timedelta

try:
    import pyautogui
except AssertionError:
    pass
import time

os_name = platform.system()
if os_name == "Windows":
    file_path = 'C:\\Users\\dkarnachev\\Downloads\\pasted_text.txt'
else:
    file_path = '/Users/dkarnachev/Downloads/pasted_text.txt'
keyboard = Controller()


def max_in_non_empty_list(lst):
    if lst:  # Проверяем, что список не пуст
        return max(lst)
    else:
        raise ValueError("Список не должен быть пустым")


def wrire_sup(sup_res_dict):
    count_of_sup = len(sup_res_dict['Support'])
    descending_order = sorted(sup_res_dict['Support'], reverse=True)
    key = keys['support'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("sup" + str(i), descending_order[i - 1])
    print(key)
    return key


def wrire_res(sup_res_dict):
    count_of_sup = len(sup_res_dict['Resistance'])
    ascending_order = sorted(sup_res_dict['Resistance'])
    key = keys['resistance'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("res" + str(i), ascending_order[i - 1])
    print("REPLACED RESISTANCE KEY " + str(key))
    return key


def write(text, interval=0.00001):
    for i in text:
        keyboard.press(i)
        keyboard.release(i)
        time.sleep(interval)
    pyautogui.press("enter")
    print(f"Write {text}")


# def toggle_bold():
#     keyboard.press(Key.ctrl if os_name == "Windows" else Key.cmd)
#     keyboard.press('b')
#     keyboard.release('b')
#     keyboard.release(Key.ctrl if os_name == "Windows" else Key.cmd)
#     time.sleep(0.2)
def write_bold(text):
    def toggle_bold():
        modifier_key = Key.ctrl if os_name == "Windows" else Key.cmd
        keyboard.press(modifier_key)
        keyboard.press('b')
        keyboard.release('b')
        keyboard.release(modifier_key)
        time.sleep(0.2)

    toggle_bold()  # Включаем жирный
    time.sleep(0.1)
    write(text)  # Пишем текст
    time.sleep(0.1)
    toggle_bold()  # Выключаем жирный
    toggle_bold()  # Выключаем жирный


# chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222"

while True:
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:

        gen = keys["general_outlook"][0]
        print(gen)
        key = keys
        levels = SupResAutomation()
        decoded_json = levels.decoding(file_path)
        drawing_data = decoded_json['panels'][0]['drawings']
        for drawing in drawing_data:
            levels.sup_res_dict_generator(drawing)
        if decoded_json:
            url = 'https://cp.octafeed.com/panel/overview-posts/create'

            webbrowser.open(url)

            # handler = VKeyHandler()
            # handler.wait_for_v_key()
            time.sleep(5)

            # toggle_bold()

            pyautogui.press('enter')
            #

            # toggle_bold()
            # write(key["general_outlook"][0])
            write_bold(key["general_outlook"][0])
            # time.sleep(0.2)
            # toggle_bold()
            # time.sleep(0.2)
            print(levels.data_state)
            if levels.data_state != "BTCUSD" and levels.data_state != "XAUUSD" and levels.data_state != "USDCAD" and levels.data_state != "GBPJPY":
                price_change = levels.get_price_change_percentage(levels.data_state, "SP5UT4AK12FE7ZEQ")
                if float(price_change) > 0.1:
                    write(key['trend'][0])
                elif float(price_change) < -0.1:
                    write(key['trend'][1])
                else:
                    write(key['trend'][2])
            else:
                write(key['trend'][0])
            # write(key['trend'][0])
            if levels.direction == "buy":
                write(wrire_sup(levels.dict_sup_res)) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1)
                write(key["if_pair_rebound"][0])
                write(wrire_res(levels.dict_sup_res)) if len(levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)

            elif levels.direction == "sell":
                write(wrire_sup(levels.dict_sup_res)) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1)
                write(wrire_res(levels.dict_sup_res)) if len(levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)
                write(key["if_pair_rebound"][1])

            with open("news.txt", "r") as content:
                try:
                    with open(file_path, 'r') as file:
                        content = file.readlines()
                    if content and len(content) == 2:
                        file_time = datetime.strptime(content[1], '%H:%M').time()
                        current_time = datetime.now()
                        threshold_time = datetime.combine(current_time.date(), file_time)
                        time_difference = threshold_time - current_time
                        write_bold(key["fundamental_factors"][0])
                        # write(key["fundamental_factors"][0])
                        # toggle_bold()
                        if time_difference > timedelta(hours=1):
                            write(content[0])
                        elif timedelta(0) <= time_difference <= timedelta(hours=1):
                            write(content[0].replace("hour", "minute"))
                        else:
                            with open(file_path, 'w') as file:
                                pass
                    else:
                        write(key["no_news"][0])
                except FileNotFoundError:
                    print("File not found.")
            today = datetime.today()
            if today.weekday() == 4:
                write(keys["friday"][0])
            time.sleep(2)
            print(f"{levels.direction}" == 'sell')
            with open("range.txt", "w") as file:
                file.write(
                    max(levels.dict_sup_res["Support"]) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1))
                file.write("\n")
                file.write(min(levels.dict_sup_res["Resistance"]) if len(
                    levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1))
            with open("variety.txt", "w") as file:
                if type(levels.broke_flag is list()):
                    if levels.broke_flag[0] == "resistance":
                        file.write(keys["broke"][1].replace("1999", levels.broke_flag[1]))
                    elif levels.broke_flag[0] == "support":
                        file.write(keys["broke"][0].replace("1999", levels.broke_flag[1]))
                if levels.direction == "sell":
                    print(1)
                    file.write(keys["bearish_title"][0].replace("1999", min(levels.dict_sup_res["Resistance"])) + "\n")
                    file.write(keys["bearish_title"][1].replace("1999", min(levels.dict_sup_res["Resistance"])))
                elif levels.direction == "buy":
                    print(2)
                    file.write(keys["bullish_title"][0].replace("1999",
                                                                max(levels.dict_sup_res["Support"]) + "\n" if len(
                                                                    levels.dict_sup_res["Support"]) > 0 else time.sleep(
                                                                    0.1)))
                    file.write(keys["bullish_title"][1].replace("1999", max(levels.dict_sup_res["Support"])) if len(
                        levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1))
            print(3)
            subprocess.run(["node", "puppeteer_script.js", f"{levels.direction}"])
            print(4)
        os.remove(file_path)
