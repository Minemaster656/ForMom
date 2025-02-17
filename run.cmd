@echo off
chcp 1251
REM Выполняем git pull
echo Проверка обновлений
git pull
echo Подготовка среды...
REM Проверяем, существует ли папка venv
if not exist "venv" (
    echo Создание виртуального окружения...
    py -m venv venv
) else (
    echo Виртуальное окружение уже существует.
)
echo Запуск среды...
REM Активируем виртуальное окружение
call .\venv\Scripts\activate
echo Установка зависимостей
REM Устанавливаем зависимости из req.txt
REM yes | py -m pip install -r req.txt -q -q -q --exists-action i
py -m pip install -r req.txt -q -q -q --exists-action i
echo ЗАПУСК!
REM Запускаем main.py и ждем завершения
python "main.py"
REM Ожидаем завершения main.py
if errorlevel 1 (
    echo Произошла ошибка при выполнении main.py.
) else (
    echo main.py завершен успешно.
)
REM pause
REM timeout /s 10