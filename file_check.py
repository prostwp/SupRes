import base64
import json
import os
import webbrowser
import subprocess
import time
# import pyautogui
import re
import requests


class SupResAutomation:
    def __init__(self):
        self.dict_sup_res = {'Support': [], 'Resistance': []}
        self.direction = ''
        self.data_state = ''
        self.timeframe = ''
        self.broke_flag = [1]

    def get_price_change_percentage(self, symbol, api_key):
        # Получаем данные о валютной паре за текущий день
        url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        # Получаем текущую дату
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Получаем данные за текущий и предыдущий день
        try:
            today_data = data['Time Series FX (Daily)'][current_date]
            today_open = float(today_data['1. open'])
            today_close = float(today_data['4. close'])

            # Рассчитываем изменение в процентах
            change_percentage = ((today_close - today_open) / today_open) * 100
            return change_percentage
        except KeyError:
            return "Данные за текущий день еще недоступны."
    def sup_res_dict_generator(self, draw_element):
        self._error_handler(draw_element, dict)
        if draw_element['toolType'] == 'text':
            splited_draw_el = draw_element['settings']['text'].split()
            if splited_draw_el[0] == "Weekly":
                splited_draw_el.remove("Weekly")

            if splited_draw_el[0] == "Broken":

                splited_draw_el.remove("Broken")

                if splited_draw_el[0] == "Support":
                    self.broke_flag = ["support", splited_draw_el[-1]]
                    splited_draw_el[0] = "Resistance"

                elif splited_draw_el[0] == "Resistance":
                    self.broke_flag = ["resistance", splited_draw_el[-1]]
                    splited_draw_el[0] = "Support"

            if splited_draw_el[0] == "Resistance":
                self.dict_sup_res["Resistance"].append(splited_draw_el[-1])
            elif splited_draw_el[0] == "Support":
                self.dict_sup_res["Support"].append(splited_draw_el[-1])
            else:
                raise Exception("It is not support or resistance")
            return {splited_draw_el[0]: splited_draw_el[1]}

        if draw_element['toolType'] == 'arrow_line':
            if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
                self.direction = "sell"
            elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
                self.direction = "buy"
            else:
                raise Exception("Direction did not found")

    def find_direction(self, draw_element):
        if draw_element['toolType'] == 'arrow_line':
            if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
                self.direction = "sell"
            elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
                self.direction = "buy"
            else:
                raise Exception("Direction did not found")

    def decoding(self, file_path):
        try:
            # Открываем исходный файл для чтения
            with open(file_path, 'r') as file:
                content = file.read()
            data_state_match = re.search(r'data-symbol="([A-Z]{6})"', content)
            if data_state_match:
                currency_pair = data_state_match.group(1)
                self.data_state = currency_pair
            else:
                raise ValueError("Валютная пара не найдена в файле")
            with open('currency_pair.txt', 'w') as file:
                file.write(currency_pair)
            # Извлекаем Base64 строку изображения
            base64_str_index = content.find("base64,") + len("base64,")
            base64_str_end_index = content.find('"', base64_str_index)
            base64_image_str = content[base64_str_index:base64_str_end_index]

            # Декодируем Base64 строку изображения в бинарные данные
            image_data = base64.b64decode(base64_image_str)

            # Сохраняем бинарные данные в файл
            # self.png_wtirer(image_data)

            # Извлекаем и декодируем строку состояния
            data_state_index = content.find('data-state="') + len('data-state="')
            data_state_end_index = content.find('"', data_state_index)
            data_state_str = content[data_state_index:data_state_end_index]

            # Декодируем строку состояния из Base64
            data_state = base64.b64decode(data_state_str).decode('utf-8')
            json_data_state = json.loads(data_state)

            # Сохраняем декодированные данные состояния в файл
            # with open('decoded_state.json', 'w') as state_file:
            #     state_file.write(data_state)

            print("Файлы успешно декодированы и сохранены.")
            return json_data_state
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")


    def png_wtirer(self, data):
        with open('decoded_image.png', 'wb') as image_file:
            image_file.write(data)

    def _error_handler(self, data, expected_type):
        if not isinstance(data, expected_type) or not data:
            raise TypeError(f"Provided data: {data} is not of type {expected_type.__name__} or is empty")


# import pyautogui
def process_file(file_path):
    dict_sup_res = {'Support': [], 'Resistance': []}
    try:
        # Открываем исходный файл для чтения
        with open(file_path, 'r') as file:
            content = file.read()

        # Извлекаем Base64 строку изображения
        base64_str_index = content.find("base64,") + len("base64,")
        base64_str_end_index = content.find('"', base64_str_index)
        base64_image_str = content[base64_str_index:base64_str_end_index]

        # Декодируем Base64 строку изображения в бинарные данные
        image_data = base64.b64decode(base64_image_str)

        # Сохраняем бинарные данные в файл
        with open('decoded_image.png', 'wb') as image_file:
            image_file.write(image_data)

        # Извлекаем и декодируем строку состояния
        data_state_index = content.find('data-state="') + len('data-state="')
        data_state_end_index = content.find('"', data_state_index)
        data_state_str = content[data_state_index:data_state_end_index]

        # Декодируем строку состояния из Base64
        data_state = base64.b64decode(data_state_str).decode('utf-8')
        json_data_state = json.loads(data_state)

        drawing_data = json_data_state['panels'][0]['drawings']
        for draw_element in drawing_data:
            if draw_element['toolType'] == 'text':
                splited_draw_el = draw_element['settings']['text'].split()
                if splited_draw_el[0] == "Weekly":
                    splited_draw_el.remove("Weekly")

                if splited_draw_el[0] == "Broken":
                    splited_draw_el.remove("Broken")

                    if splited_draw_el[0] == "Support":
                        splited_draw_el[0] = "Resistance"

                    elif splited_draw_el[0] == "Resistance":
                        splited_draw_el[0] = "Support"

                if splited_draw_el[0] == "Resistance":
                    dict_sup_res["Resistance"].append(splited_draw_el[-1])
                elif splited_draw_el[0] == "Support":
                    dict_sup_res["Support"].append(splited_draw_el[-1])
                else:
                    raise Exception("It is not support or resistance")

            if draw_element['toolType'] == 'arrow_line':
                if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
                    direction = "Sell"
                elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
                    direction = "Buy"
                else:
                    raise Exception("Direction did not found")

        # Сохраняем декодированные данные состояния в файл
        with open('decoded_state.json', 'w') as state_file:
            state_file.write(data_state)

        print("Файлы успешно декодированы и сохранены.")
        return direction
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False


def check_for_file():
    file_path = '/Users/dkarnachev/Downloads/pasted_text.txt'
    while True:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            if process_file(file_path):
                url = 'https://cp.octafeed.com/panel/overview-posts/create'
                webbrowser.open(url)
                # x, y = 358, 960  # Замените на точные координаты
                # pyautogui.moveTo(x, y)
                time.sleep(2)
                # time.sleep(0.5)
                # pyautogui.press('enter')

                # subprocess.run(["node", "puppeteer_script.js"])
            # os.remove(file_path)  # Удаляем файл после обработки
    # time.sleep(1)


if __name__ == "__main__":
    check_for_file()
