import win32gui
import win32process
import time
import psutil
import os
import time
from PIL import ImageGrab
import sqlite3

def initialize_database():
    """Проверяет наличие базы данных и создает таблицу, если она не существует."""
    db_path = './recorder/records.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            timestamp TEXT,
            action INTEGER,
            window_title TEXT,
            pid INTEGER,
            process_name TEXT,
            screenshot_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_record(action, window_title, pid, process_name, screenshot_name=None):
    """Создает запись в базе данных."""
    db_path = './recorder/records.db'
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO records (timestamp, action, window_title, pid, process_name, screenshot_name)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, action, window_title, pid, process_name, screenshot_name))
    
    conn.commit()
    conn.close()

initialize_database()  # Инициализация базы данных при запуске


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
    time.sleep(0.125)
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
    screenshot.save(screenshot_path)
    print(f"[Скриншот] Сохранен: {screenshot_path}")
    return screenshot_path

def monitor_windows():
    """Отслеживает открытие и закрытие окон."""
    prev_windows = get_open_windows()

    while True:
        time.sleep(0.25)  # Интервал проверки
        current_windows = get_open_windows()
        needScreenshot = False
        screenshot_path = None
        records = []
        # Определяем открытые новые окна
        opened_windows = {hwnd: info for hwnd, info in current_windows.items() if hwnd not in prev_windows}
        for hwnd, (title, pid) in opened_windows.items():
            print(f"[Открыто] Заголовок: '{title}', PID: {pid}, Процесс: {get_process_name(pid)}")
            needScreenshot = True
            records.append((1, title, pid, get_process_name(pid), None))
        # Определяем закрытые окна
        closed_windows = {hwnd: info for hwnd, info in prev_windows.items() if hwnd not in current_windows}
        for hwnd, (title, pid) in closed_windows.items():
            print(f"[Закрыто] Заголовок: '{title}', PID: {pid}, Процесс: {get_process_name(pid)}")
            records.append((2, title, pid, get_process_name(pid), None))
        # Обновляем предыдущий список окон
        prev_windows = current_windows
        if needScreenshot:
            print("[Уведомление] Создание скриншота...")
            # Вызов функции для создания скриншота
            screenshot_path = take_screenshot()
        if screenshot_path:
            records.append((-1, None, None, None, screenshot_path))
        for record in records:
            create_record(*record)





if __name__ == "__main__":
    monitor_windows()
