#!/bin/bash

# 🐆 ChitaNet VPN - اسکریپت اجرا

echo "═════════════════════════════════════════"
echo "  🐆 ChitaNet VPN - فروشگاه VPN"
echo "═════════════════════════════════════════"
echo ""

# بررسی Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 نصب نیست!"
    exit 1
fi

echo "✅ Python3 پیدا شد"

# ایجاد محیط مجازی اگر نباشد
if [ ! -d "venv" ]; then
    echo "📦 ایجاد محیط مجازی..."
    python3 -m venv venv
fi

# فعال کردن محیط مجازی
echo "🔧 فعال‌سازی محیط مجازی..."
source venv/bin/activate || . venv/Scripts/activate

# نصب وابستگی‌ها
echo "📥 نصب وابستگی‌ها..."
pip install --upgrade pip
pip install -r requirements.txt

# ایجاد پوشه uploads
mkdir -p static/uploads

# اجرای اپلیکیشن
echo ""
echo "═════════════════════════════════════════"
echo "  ✨ اپلیکیشن شروع می‌شود..."
echo "═════════════════════════════════════════"
echo ""
echo "🌐 آدرس دسترسی: http://localhost:5000"
echo "📊 پنل ادمین: http://localhost:5000/admin"
echo "👤 رمز ادمین: vpnadmin1404"
echo ""
echo "برای خروج: Ctrl+C را فشار دهید"
echo ""

python app.py