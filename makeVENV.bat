
@echo off
set VENV_DIR=venv

if not exist "%VENV_DIR%" (
    echo Создание виртуального окружения...
    python -m venv %VENV_DIR%
    echo Виртуальное окружение создано.
) else (
    echo Виртуальное окружение уже существует.
)

