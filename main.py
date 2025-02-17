import os
import time
import tkinter as tk

import asyncio
import psutil
import win32gui
import win32process
from PIL import ImageGrab

import trigger_chat


def get_open_windows():
    """Возвращает словарь с дескрипторами окон и их заголовками."""
    windows = {}

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):  # Проверяем, видимо ли окно
            title = win32gui.GetWindowText(hwnd)  # Получаем заголовок окна
            if title:  # Если есть заголовок, добавляем в словарь
                pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                windows[hwnd] = (title, pid)

    win32gui.EnumWindows(callback, None)
    return windows
def get_process_name(pid):
    """Возвращает имя процесса по его PID."""
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None


def take_screenshot():
    # await asyncio.sleep(0.125)
    # time.sleep(0.125)
    """Создает скриншот экрана и сохраняет его в папку screenshots."""
    timestamp = time.strftime("%d.%m.%Y_%H-%M-%S")
    screenshot_dir = './recorder/screenshots'
    os.makedirs(screenshot_dir, exist_ok=True)  # Создаем папку, если она не существует

    # Генерируем имя файла с учетом существующих скриншотов
    base_screenshot_path = os.path.join(screenshot_dir, f'SCREENSHOT_{timestamp}')
    screenshot_path = base_screenshot_path + '.png'
    counter = 1

    while os.path.exists(screenshot_path):
        screenshot_path = f"{base_screenshot_path}_{counter}.png"
        counter += 1

    # Делаем скриншот
    screenshot = ImageGrab.grab()
    # screenshot.save(screenshot_path)
    # print(f"[Скриншот] Сохранен: {screenshot_path}")
    return screenshot
class App:
    prev_windows = get_open_windows()
    def __init__(self, root):
        self.root = root
        self.root.title("Ботяра")

        # Переменные
        self.do_auto_disable = tk.BooleanVar(value=False)
        self.enabled = tk.BooleanVar(value=False)

        # Виджеты
        tk.Label(root, text="Сработал - приостановить бота").pack()
        self.auto_disable_button = tk.Button(root, text="Откл.", command=self.toggle_auto_disable)
        self.auto_disable_button.pack()

        self.status_label = tk.Label(root, text="Выключено", fg="green")
        self.status_label.pack()
        self.toggle_button = tk.Button(root, text="Включить", bg="green", command=self.toggle_enabled)
        self.toggle_button.pack()


        self.update_ui()
        # self.loop = asyncio.new_event_loop()
        # self.task = self.loop.create_task(self.scanner_thread())
        # self.task.
        # self.task = asyncio.create_task(self.scanner_thread())
        # self.task.



    def toggle_auto_disable(self):
        self.do_auto_disable.set(not self.do_auto_disable.get())
        self.auto_disable_button.config(text="Вкл." if self.do_auto_disable.get() else "Откл.")

    def toggle_enabled(self):
        self.enabled.set(not self.enabled.get())
        self.update_ui()

    def update_ui(self):
        if self.enabled.get():
            self.status_label.config(text="Включено", fg="green")
            self.toggle_button.config(text="Выключить", bg="red")
        else:
            self.status_label.config(text="Выключено", fg="red")
            self.toggle_button.config(text="Включить", bg="green")

    def scanner_thread(self):
        # print("tick")

        # while True:
        # await asyncio.sleep(0.25)  # Интервал проверки
        if not self.enabled.get():
            self.prev_windows = get_open_windows()

            self.root.after(200, self.scanner_thread)

            return
        current_windows = get_open_windows()
        needScreenshot = False
        screenshot_path = None
        records = []
        # Определяем открытые новые окна
        opened_windows = {hwnd: info for hwnd, info in current_windows.items() if hwnd not in self.prev_windows}
        for hwnd, (title, pid) in opened_windows.items():
            print(f"[Открыто] Заголовок: '{title}', PID: {pid}, Процесс: {get_process_name(pid)}")
            needScreenshot = True
            records.append((1, title, pid, get_process_name(pid), None))
        # Определяем закрытые окна
        closed_windows = {hwnd: info for hwnd, info in self.prev_windows.items() if hwnd not in current_windows}
        for hwnd, (title, pid) in closed_windows.items():
            print(f"[Закрыто] Заголовок: '{title}', PID: {pid}, Процесс: {get_process_name(pid)}")
            records.append((2, title, pid, get_process_name(pid), None))
        # Обновляем предыдущий список окон
        prev_windows = current_windows
        if needScreenshot:
            # print("[Уведомление] Создание скриншота...")
            # Вызов функции для создания скриншота
            screenshot = take_screenshot()
            screen_width, screen_height = screenshot.size

            # Координаты пикселя (80, 120) от правого нижнего угла
            x = screen_width - 80
            y = screen_height - 120
            # Целевой цвет в RGB
            target_color = (33, 143, 97)  # #218f61
            pixel_color = screenshot.getpixel((x, y))

            # Проверяем цвет и вызываем функцию
            if pixel_color == target_color:
                if app.do_auto_disable.get():
                    app.enabled.set(False)
                trigger_chat.main()
        # if screenshot_path:
            # records.append((-1, None, None, None, screenshot_path))
        # for record in records:
            # create_record(*record)
            # print(record)
        self.prev_windows = get_open_windows()

        self.root.after(200, self.scanner_thread)




# Запуск
root = tk.Tk()
app = App(root)
root.after(200, app.scanner_thread)
root.mainloop()
