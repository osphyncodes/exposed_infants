@echo off
:: Set base paths
set BASE_DIR=C:\Users\Ngomba_Joseph\Documents\Programming\exposed_infants
set ENV_DIR=%BASE_DIR%\env
set PROJECT_DIR=%BASE_DIR%\backend

:: Compose the full command
set CMD=call "%ENV_DIR%\Scripts\activate.bat" ^&^& timeout /t 3 /nobreak ^&^& cd /d "%PROJECT_DIR%" ^&^& python manage.py runserver 0.0.0.0:8000

:: Run the command silently using PowerShell
powershell -WindowStyle Hidden -Command "%CMD%"
