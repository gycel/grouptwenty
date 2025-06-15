@echo off
echo Starting Admin Dashboard Report Generation...
echo.

REM Check if Django server is running
echo Checking if Django server is accessible...
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Django server is not running on http://localhost:8000
    echo Please start your Django server first with: python manage.py runserver
    pause
    exit /b 1
)

echo Django server is accessible. Starting Robot Framework...
echo.

REM Run the Robot Framework script
robot simple_admin_report.robot

echo.
echo Report generation completed!
echo Check the generated files in the current directory.
pause 