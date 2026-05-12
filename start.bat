@echo off
title Yumi UserBot Launcher
cd /d "%~dp0"

echo Сброс зависших процессов Python...
taskkill /f /im python.exe >nul 2>&1

echo Запуск бота...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Произошла ошибка при запуске.
    pause
)