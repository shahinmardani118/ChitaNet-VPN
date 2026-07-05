# 🚀 شروع سریع ChitaNet VPN

## ⚡ اجرای فوری (بدون دردسر!)

### 🖥️ **برای Windows:**

1. **فایل `run.bat` را دابل‌کلیک کنید**
2. **صبر کنید تا نصب شود (۲-۳ دقیقه)**
3. **مرورگر را باز کنید و برو به:** `http://localhost:5000`

### 🍎 **برای macOS/Linux:**

```bash
chmod +x run.sh
./run.sh
```

سپس برو به: `http://localhost:5000`

---

## 📋 اطلاعات ورود

### 👤 **کاربر عادی:**
- به صفحه اصلی برو و یک پلن انتخاب کن
- یوزرنیم تلگرام خود را وارد کن
- کد تأیید را دریافت کن

### 🔐 **پنل ادمین:**
- برو به: `http://localhost:5000/admin`
- **رمز عبور:** `vpnadmin1404`

---

## 🎯 کار کردن

### 1️⃣ **سفارش جدید**
- صفحه اصلی → یک پلن انتخاب کن → نام خود را وارد کن
- کد سفارش دریافت کن

### 2️⃣ **پرداخت**
- شماره کارت: `6219861881136252`
- صاحب حساب: `ورمزیار`
- رسید را آپ‌لود کن

### 3️⃣ **تأیید (ادمین)**
- پنل ادمین رو باز کن
- سفارش‌های در انتظار رو ببین
- کانفیگ را وارد کن و تایید کن

### 4️⃣ **دریافت کانفیگ (کاربر)**
- پروفایل خود را باز کن
- کانفیگ را کپی کن

---

## 📱 اطلاعات تلگرام

- **بات:** https://t.me/ChitaSeee_bot
- **پشتیبانی:** https://t.me/chitaseee
- **توکن:** `8606482568:AAGnvoTHaH0D-qk7STb6T1NF9goKX-3FA30`
- **آیدی ادمین:** `7597912378`

---

## 🗄️ دیتابیس

- **نوع:** SQLite
- **فایل:** `database.db` (خودکار ساخته می‌شود)
- **مکان:** پوشه اصلی پروژه

---

## 🐳 اجرا با Docker

```bash
# نصب Docker: https://www.docker.com/

# اجرا
docker-compose up --build

# متوقف کردن
docker-compose down
```

---

## 🚨 مشکلات معمول

### ❌ "Python not found"
→ Python را نصب کن: https://www.python.org/downloads/

### ❌ "Port 5000 already in use"
→ این دستور را اجرا کن:
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

### ❌ "Module not found"
→ دستور را اجرا کن:
```bash
pip install -r requirements.txt
```

### ❌ "Telegram Token Invalid"
→ توکن را بررسی کن یا توکن جدیدی بگیر: https://t.me/BotFather

---

## 💾 تغییر تنظیمات

### فایل `.env`

```env
# توکن تلگرام
TELEGRAM_TOKEN=your_token_here

# آیدی چت ادمین
ADMIN_CHAT_ID=your_chat_id

# رمز ادمین
ADMIN_PASSWORD=your_password

# شماره کارت
BANK_CARD=your_card_number

# صاحب حساب
BANK_OWNER=صاحب حساب

# پورت
PORT=5000
```

---

## 📊 ساختار پروژه

```
ChitaNet-VPN/
├── app.py                # برنامه اصلی ✅
├── requirements.txt       # وابستگی‌ها ✅
├── .env                   # تنظیمات ✅
├── run.sh                # اسکریپت اجرا (Linux/Mac) ✅
├── run.bat               # اسکریپت اجرا (Windows) ✅
├── docker-compose.yml     # Docker ✅
├── Dockerfile            # Docker ✅
├── database.db           # دیتابیس (خودکار)
└── static/uploads/       # آپ‌لودهای کاربران
```

---

## 🎉 تماس

- 💬 **تلگرام:** https://t.me/chitaseee
- 📧 **ایمیل:** contact@chitanet.com

**ایجاد شده با ❤️ توسط Shahin Mardani**

---

**حالا آماده هستی! 🚀 رو شروع کن!**