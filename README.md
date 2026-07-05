# 🐆 چیتا نت - فروشگاه VPN

فروشگاه آنلاین VPN با ادغام تلگرام، دیزاین حرفه‌ای و سیستم پرداخت یکپارچه.

## ✨ ویژگی‌های اصلی

- 🎨 **دیزاین مدرن و شیک** - Gradient، Animation، Responsive
- 📱 **ریسپانسیو** - کار کامل بر روی موبایل، تبلت و دسکتاپ
- 🤖 **ادغام تلگرام بات** - ورود خودکار و ایجاد پروفایل
- 👤 **پروفایل خودکار** - اطلاعات کاربر از تلگرام
- 💳 **سیستم سفارش** - 5 پلن VPN مختلف
- 📊 **داشبورد کاربر** - مشاهده سفارشات و وضعیت
- 🔐 **امنیت بالا** - Environment Variables، Password Hashing
- 💾 **دیتابیس SQLite** - ذخیره سازی ایمن اطلاعات
- ⚡ **API RESTful** - دسترسی برنامه‌ای به داده‌ها
- 📧 **اعلان تلگرام** - اطلاع‌رسانی خودکار

## 📦 پلن‌های موجود

| پلن | حجم | قیمت | سرعت | مدت | سرور |
|-----|------|-------|-------|------|------|
| عادی | 500 MB | 380,000 تومان | 10 Mbps | 30 روز | 🇩🇪 آلمان |
| پربازدید | 1 GB | 350,000 تومان | 20 Mbps | 30 روز | 🇩🇪 آلمان |
| اقتصادی | 2 GB | 650,000 تومان | 50 Mbps | 90 روز | 🇳🇱 هلند |
| ویژه | 5 GB | 1,100,000 تومان | 100 Mbps | 180 روز | 🇺🇸 آمریکا |
| سالانه | 10 GB | 1,800,000 تومان | 200 Mbps | 365 روز | 🇺🇸 آمریکا |

## 🚀 نصب و اجرا (Local)

### پیش‌نیازها
- Python 3.8+
- pip
- Git

### مراحل نصب

```bash
# 1. Repository کلون کن
git clone https://github.com/shahinmardani118/ChitaNet-VPN.git
cd ChitaNet-VPN

# 2. محیط مجازی ایجاد کن
python -m venv venv

# 3. محیط مجازی را فعال کن
# روی Windows:
venv\Scripts\activate
# روی macOS/Linux:
source venv/bin/activate

# 4. وابستگی‌ها را نصب کن
pip install -r requirements.txt

# 5. فایل .env ایجاد کن
cp .env.example .env

# 6. فایل .env را ویرایش کن (توکن تلگرام و اطلاعات بانکی را وارد کن)
nano .env

# 7. اپلیکیشن را اجرا کن
python app.py
```

**آدرس دسترسی:** `http://localhost:5000`

---

## 🐳 اجرا با Docker

### پیش‌نیازها
- Docker
- Docker Compose

### مراحل

```bash
# 1. فایل .env را ویرایش کن
nano .env

# 2. Docker Compose را اجرا کن
docker-compose up --build

# 3. سایت قابل دسترسی است
http://localhost:5000
```

**متوقف کردن:**
```bash
docker-compose down
```

---

## ☁️ Deploy بر Render (رایگان)

### Step 1: Repository GitHub ایجاد کن
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/ChitaNet-VPN.git
git push -u origin main
```

### Step 2: Deploy بر Render
1. برو: https://render.com
2. کلیک کن: **New → Web Service**
3. GitHub repo رو کانکت کن
4. تنظیمات:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. **Environment Variables** را اضافه کن:
   - `TELEGRAM_TOKEN`
   - `ADMIN_CHAT_ID`
   - `ADMIN_PASSWORD`
   - `BANK_CARD`
   - `BANK_OWNER`
6. **Deploy** را کلیک کن ✅

---

## 🌐 Deploy بر Railway (رایگان)

```bash
# 1. Railway CLI نصب کن
npm i -g @railway/cli

# 2. وارد Railway شو
railway login

# 3. Repository رو Initialize کن
railway init

# 4. Environment Variables را تنظیم کن
railway variables set TELEGRAM_TOKEN=your_token
railway variables set ADMIN_CHAT_ID=your_chat_id
# ... و سایر متغیرها

# 5. Deploy کن
railway up
```

---

## ⚙️ متغیرهای محیطی

فایل `.env` را ایجاد کن:

```env
# Telegram Configuration
TELEGRAM_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=your_admin_chat_id

# Admin
ADMIN_PASSWORD=your_secure_password

# Bank Information
BANK_CARD=6219861881136252
BANK_OWNER=نام صاحب حساب

# Flask
PORT=5000
FLASK_ENV=production
```

### کیفیت توکن تلگرام
1. برو: https://t.me/BotFather
2. دستور بزن: `/newbot`
3. توکن را کپی کن

---

## 📂 ساختار پروژه

```
ChitaNet-VPN/
├── app.py                 # اصلی‌ترین فایل اپلیکیشن
├── requirements.txt       # وابستگی‌های Python
├── Dockerfile            # تنظیمات Docker
├── docker-compose.yml    # تنظیمات Docker Compose
├── .env.example          # نمونه متغیرهای محیطی
├── .gitignore           # فایل‌های عدم نیاز
├── README.md            # این فایل
└── database.db          # دیتابیس SQLite (خودکار ساخته می‌شود)
```

---

## 📊 دیتابیس

سیستم از **SQLite** استفاده می‌کند و خودکار جداول را ایجاد می‌کند.

### جداول
- **users** - اطلاعات کاربران
- **orders** - سفارشات و تراکنش‌ها
- **support_tickets** - تیکت‌های پشتیبانی

---

## 🔌 API Endpoints

### دریافت اطلاعات کاربر
```
GET /api/user/info
```

### دریافت لیست پلن‌ها
```
GET /api/plans
```

---

## 🎯 صفحات اصلی

- `/` - صفحه اصلی و لیست پلن‌ها
- `/login` - صفحه ورود
- `/profile` - پروفایل کاربر
- `/orders` - لیست سفارشات
- `/buy/<plan_key>` - صفحه پرداخت
- `/logout` - خروج

---

## 🔐 امنیت

- ✅ Environment Variables برای حفاظت از اسرار
- ✅ Password Hashing با SHA256
- ✅ CSRF Protection
- ✅ Session Management
- ✅ Input Validation

---

## 🤖 ادغام تلگرام بات

### کار کردن

1. **بات را استارت کن**: `/start`
2. **اطلاعات کاربر ذخیره می‌شود**:
   - Telegram ID
   - Username
   - First Name
   - Language
3. **کاربر به سایت رفته و ورود می‌کند**
4. **پروفایل خودکار ایجاد می‌شود**

---

## 📝 لاگ‌ها

```bash
# مشاهده لاگ‌های Docker
docker-compose logs -f

# مشاهده لاگ‌های ریل‌تایم
tail -f app.log
```

---

## 🐛 حل مشکلات

### مشکل: خطای "Module not found"
```bash
pip install -r requirements.txt
```

### مشکل: دیتابیس خالی است
```bash
rm database.db
python app.py
```

### مشکل: توکن تلگرام کار نمی‌کند
- توکن را بررسی کن
- BotFather قطع کن و دوباره شروع کن

---

## 📞 پشتیبانی

- 💬 **تلگرام**: https://t.me/chitaseee
- 🤖 **بات**: https://t.me/ChitaSeee_bot

---

## 👨‍💻 سازنده

**Shahin Mardani**

GitHub: https://github.com/shahinmardani118

---

## 📄 لایسنس

MIT License - آزاد برای استفاده تجاری و شخصی

---

## 🌟 اگر کمک کرد، یک ستاره بدهید!

```bash
git star shahinmardani118/ChitaNet-VPN
```

---

## 📚 منابع مفید

- 🔗 [Flask Documentation](https://flask.palletsprojects.com/)
- 🔗 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🔗 [Docker Documentation](https://docs.docker.com/)
- 🔗 [Render Deployment](https://render.com/docs)
- 🔗 [Railway Deployment](https://docs.railway.app/)

---

## 🎉 شروع کنید!

```bash
python app.py
# یا
docker-compose up
```

**سایت شما اکنون آنلاین است!** 🚀
