@echo off
REM 🐆 ChitaNet VPN - اسکریپت اجرا برای Windows

echo =====================================
echo   🐆 ChitaNet VPN - فروشگاه VPN
echo =====================================
echo.

REM بررسی Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python نصب نیست!
    echo برای نصب Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python پیدا شد

REM ایجاد محیط مجازی اگر نباشد
if not exist "venv" (
    echo 📦 ایجاد محیط مجازی...
    python -m venv venv
)

REM فعال کردن محیط مجازی
echo 🔧 فعال‌سازی محیط مجازی...
call venv\Scripts\activate.bat

REM نصب وابستگی‌ها
echo 📥 نصب وابستگی‌ها...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM ایجاد پوشه uploads
if not exist "static\uploads" mkdir static\uploads

REM اجرای اپلیکیشن
echo.
echo =====================================
echo   ✨ اپلیکیشن شروع می‌شود...
echo =====================================
echo.
echo 🌐 آدرس دسترسی: http://localhost:5000
echo 📊 پنل ادمین: http://localhost:5000/admin
echo 👤 رمز ادمین: vpnadmin1404
echo.
echo برای خروج: Ctrl+C را فشار دهید
echo.

python app.py