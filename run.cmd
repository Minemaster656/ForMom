@echo off
REM Выполняем git pull
echo Проверка обновлений...
git pull
echo Готово.
REM Проверяем, существует ли папка venv
if not exist "venv" (
    echo Создание виртуального окружения...
    py -m venv venv
    echo Готово.
) else (
    echo Виртуальное окружение уже существует.
)

REM Активируем виртуальное окружение
call .\venv\Scripts\activate
echo Окружение активировано.
echo Установка зависимостей...
REM Устанавливаем зависимости из req.txt
pip install -r req.txt
echo Зависимости установлены.
echo ЗАПУСК!
REM Запускаем main.py
python main.py

REM Деактивируем виртуальное окружение (опционально)
deactivate