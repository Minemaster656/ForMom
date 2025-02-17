import pygetwindow as gw
import pyautogui
import time

# Название окна (например, "Блокнот" или "Chrome")
window_title = "JivoSite_notify"

def main():
    # Поиск окна по названию
    windows = gw.getWindowsWithTitle(window_title)

    if len(windows) > 0:
        # Переключение на первое найденное окно
        window = windows[0]
        window.activate()  # Активируем окно
        time.sleep(0.2)  # Даем время для переключения

        # Симуляция нажатия LCtrl + Ё
        pyautogui.keyDown('ctrl')
        pyautogui.press('`')  # Клавиша ` (на ней обычно находится Ё)
        pyautogui.keyUp('ctrl')
    else:
        print(f"Окно с названием '{window_title}' не найдено.")
