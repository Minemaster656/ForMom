@echo off
chcp 1251
REM ��������� git pull
echo �������� ����������
git pull
echo ���������� �����...
REM ���������, ���������� �� ����� venv
if not exist "venv" (
    echo �������� ������������ ���������...
    py -m venv venv
) else (
    echo ����������� ��������� ��� ����������.
)
echo ������ �����...
REM ���������� ����������� ���������
call .\venv\Scripts\activate
echo ��������� ������������
REM ������������� ����������� �� req.txt
REM yes | py -m pip install -r req.txt -q -q -q --exists-action i
py -m pip install -r req.txt -q -q -q --exists-action i
echo ������!
REM ��������� main.py � ���� ����������
python "main.py"
REM ������� ���������� main.py
if errorlevel 1 (
    echo ��������� ������ ��� ���������� main.py.
) else (
    echo main.py �������� �������.
)
REM pause
REM timeout /s 10