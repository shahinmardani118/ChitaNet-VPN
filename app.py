from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
import sqlite3
import requests
import os
import hashlib
import random
import time
import threading
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "ramz_khili_mohkami_123456"

TELEGRAM_TOKEN = "8606482568:AAGnvoTHaH0D-qk7STb6T1NF9goKX-3FA30"
ADMIN_CHAT_ID = "7597912378"

BOT_USERNAME = ""
try:
    _r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe", timeout=5)
    if _r.ok:
        BOT_USERNAME = _r.json()['result']['username']
except:
    pass

pending_otp = {}      # {code: {'username': str, 'ts': float}}
verified_codes = {}   # {code: {'chat_id': str, 'username': str}}
_last_update_id = 0

def _poll_bot():
    global _last_update_id
    while True:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
                params={'offset': _last_update_id + 1, 'timeout': 25},
                timeout=30
            )
            if r.ok:
                for upd in r.json().get('result', []):
                    _last_update_id = upd['update_id']
                    msg = upd.get('message', {})
                    text = (msg.get('text') or '').strip()
                    chat = msg.get('chat', {})
                    chat_id = str(chat.get('id', ''))
                    uname = chat.get('username', '')
                    if text.isdigit() and len(text) == 6 and text in pending_otp:
                        entry = pending_otp[text]
                        if time.time() - entry['ts'] <= 300:
                            verified_codes[text] = {'chat_id': chat_id, 'username': uname}
                            send_telegram_message(chat_id, "✅ کد تأیید شد! به سایت برگردید و دکمه «تأیید کردم» را بزنید.")
        except Exception:
            pass
        time.sleep(2)

threading.Thread(target=_poll_bot, daemon=True).start()

PLANS = {
    "1_month_500": {"name": "یک ماهه 500 مگابایت", "price": 380000, "server": "🇩🇪 آلمان", "category": "عادی"},
    "1_month_1gb": {"name": "یک ماهه 1 گیگابایت", "price": 350000, "server": "🇩🇪 آلمان", "category": "پربازدید"},
    "3_month_2gb": {"name": "سه ماهه 2 گیگابایت", "price": 650000, "server": "🇳🇱 هلند", "category": "اقتصادی"},
    "6_month_5gb": {"name": "شش ماهه 5 گیگابایت", "price": 1100000, "server": "🇺🇸 آمریکا", "category": "ویژه"},
}
BANK_CARD = "6219861881136252"
BANK_OWNER = "ورمزیار"
ADMIN_PASSWORD = "vpnadmin1404"

# ─── BASE TEMPLATES ───────────────────────────────────────────────────────────

BASE_START = '''<!DOCTYPE html>
<html>
<head>
    <title>🐆 چیتا نت | فروشگاه VPN</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="فروشگاه اینترنتی چیتا نت — خرید VPN با کیفیت بالا، پرداخت کارت به کارت و تحویل سریع کانفیگ">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Vazirmatn', 'Tahoma', sans-serif;
            background: #080b14;
            color: #e8eaf6;
            min-height: 100vh;
            direction: rtl;
            overflow-x: hidden;
        }

        /* ── Animated Background ── */
        body::before {
            content: '';
            position: fixed; inset: 0; z-index: -1;
            background:
                radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,120,255,0.12) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(120,0,255,0.10) 0%, transparent 60%),
                radial-gradient(ellipse 50% 60% at 50% 50%, rgba(0,60,120,0.08) 0%, transparent 70%),
                linear-gradient(160deg, #080b14 0%, #0d1220 50%, #0a0e1a 100%);
            animation: bgPulse 8s ease-in-out infinite alternate;
        }
        @keyframes bgPulse {
            0%   { opacity: 1; }
            100% { opacity: 0.85; filter: hue-rotate(15deg); }
        }

        .container { max-width: 660px; margin: 0 auto; padding: 20px; padding-bottom: 100px; }

        /* ── Topbar ── */
        .topbar {
            display: flex; align-items: center; justify-content: space-between;
            padding: 20px 0 12px 0;
        }
        .logo {
            flex: 1; text-align: center;
            font-size: 28px; font-weight: 900;
            background: linear-gradient(90deg, #00c6ff, #7b2ff7, #00c6ff);
            background-size: 200%;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmerText 4s linear infinite;
            letter-spacing: 1px;
        }
        @keyframes shimmerText { 0%{background-position:0%} 100%{background-position:200%} }

        .cart-btn {
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            color: #fff; border: none; border-radius: 14px;
            padding: 10px 18px; font-size: 14px; font-weight: 700;
            cursor: pointer; text-decoration: none;
            display: flex; align-items: center; gap: 6px;
            white-space: nowrap; transition: all 0.25s;
            box-shadow: 0 4px 15px rgba(99,102,241,0.35);
            font-family: inherit;
        }
        .cart-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 22px rgba(99,102,241,0.5); }

        /* ── Cards ── */
        .card {
            background: rgba(15,18,30,0.85);
            backdrop-filter: blur(18px);
            border-radius: 24px; padding: 24px;
            margin-bottom: 22px;
            border: 1px solid rgba(99,102,241,0.18);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
            animation: fadeUp 0.4s ease both;
        }
        @keyframes fadeUp {
            from { opacity:0; transform:translateY(18px); }
            to   { opacity:1; transform:translateY(0); }
        }

        /* ── Plan Cards ── */
        .plan {
            background: rgba(20,24,40,0.7);
            margin: 12px 0; padding: 18px 16px;
            border-radius: 18px; cursor: pointer;
            transition: all 0.3s cubic-bezier(.4,0,.2,1);
            border: 2px solid rgba(99,102,241,0.1);
            position: relative; overflow: hidden;
        }
        .plan::before {
            content: ''; position: absolute; inset: 0;
            background: linear-gradient(135deg, rgba(0,198,255,0.06), rgba(123,47,247,0.06));
            opacity: 0; transition: opacity 0.3s;
        }
        .plan:hover { transform: translateY(-4px); border-color: #6366f1; box-shadow: 0 8px 30px rgba(99,102,241,0.2); }
        .plan:hover::before { opacity: 1; }
        .plan.selected {
            border-color: #0ea5e9;
            background: rgba(14,165,233,0.08);
            box-shadow: 0 0 0 1px #0ea5e9, 0 8px 30px rgba(14,165,233,0.25);
        }
        .plan.selected::after {
            content: '✓'; position: absolute; top: 12px; left: 14px;
            background: #0ea5e9; color: #fff; border-radius: 50%;
            width: 22px; height: 22px; font-size: 13px; font-weight: bold;
            display: flex; align-items: center; justify-content: center;
        }
        .plan-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .plan-name { font-size: 16px; font-weight: 700; color: #e0e7ff; }
        .plan-price { font-size: 20px; font-weight: 900; color: #fbbf24; }
        .plan-price span { font-size: 12px; font-weight: 400; color: #aaa; }
        .plan-meta { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
        .plan-server { font-size: 12px; color: #94a3b8; }
        .plan-badge {
            display: inline-block;
            background: linear-gradient(90deg, rgba(99,102,241,0.2), rgba(14,165,233,0.2));
            color: #a5b4fc; border-radius: 20px;
            padding: 3px 10px; font-size: 11px; font-weight: 600;
            border: 1px solid rgba(99,102,241,0.2);
        }

        /* ── Inputs ── */
        input, textarea, select {
            width: 100%; padding: 13px 16px; margin: 10px 0;
            border-radius: 12px;
            border: 1.5px solid rgba(99,102,241,0.2);
            background: rgba(10,13,25,0.8);
            color: #e8eaf6; font-size: 15px;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
        }
        input::placeholder { color: #475569; }

        /* ── Buttons ── */
        button, .btn {
            width: 100%; padding: 15px;
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            color: white; border: none; border-radius: 14px;
            font-size: 16px; font-weight: 700; cursor: pointer;
            transition: all 0.3s; text-align: center;
            display: block; text-decoration: none;
            box-sizing: border-box; font-family: inherit;
            position: relative; overflow: hidden;
            box-shadow: 0 4px 20px rgba(99,102,241,0.3);
        }
        button::after, .btn::after {
            content: ''; position: absolute; top: -50%; left: -60%;
            width: 40%; height: 200%;
            background: rgba(255,255,255,0.15);
            transform: skewX(-20deg);
            transition: left 0.4s;
        }
        button:hover::after, .btn:hover::after { left: 120%; }
        button:hover, .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(99,102,241,0.45); }
        button:active, .btn:active { transform: translateY(0); }

        .btn-green { background: linear-gradient(135deg, #22c55e, #16a34a); box-shadow: 0 4px 20px rgba(34,197,94,0.3); }
        .btn-green:hover { box-shadow: 0 8px 28px rgba(34,197,94,0.45); }
        .btn-outline {
            background: transparent;
            border: 2px solid rgba(99,102,241,0.4);
            color: #a5b4fc; margin-top: 10px;
            box-shadow: none;
        }
        .btn-outline:hover { background: rgba(99,102,241,0.1); border-color: #6366f1; box-shadow: none; }
        .btn-outline::after { display: none; }
        .btn-red { background: linear-gradient(135deg, #ef4444, #dc2626); box-shadow: 0 4px 20px rgba(239,68,68,0.3); }

        /* ── Badges ── */
        .badge { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .badge-pending { background: linear-gradient(135deg,#f59e0b,#d97706); color:#fff; }
        .badge-approved { background: linear-gradient(135deg,#22c55e,#16a34a); color:#fff; }
        .badge-rejected { background: linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }

        /* ── Admin ── */
        .admin-panel { background: rgba(10,13,25,0.9); padding: 22px; border-radius: 20px; margin: 10px 0; border: 1px solid rgba(99,102,241,0.15); }
        .order-item { border-bottom: 1px solid rgba(99,102,241,0.1); padding: 18px 8px; margin: 8px 0; }
        textarea { font-family: monospace; }
        hr { border: none; border-top: 1px solid rgba(99,102,241,0.12); margin: 16px 0; }

        /* ── Config Box ── */
        .config-box {
            background: rgba(0,255,170,0.04);
            border: 1px solid rgba(0,255,170,0.2);
            border-radius: 14px; padding: 14px;
            margin: 12px 0; word-break: break-all;
            font-size: 13px; font-family: monospace;
            direction: ltr; color: #00ffaa;
            position: relative;
        }
        .copy-btn {
            display: block; width: 100%; margin-top: 10px; padding: 9px;
            background: rgba(0,255,170,0.1); border: 1px solid rgba(0,255,170,0.25);
            color: #00ffaa; border-radius: 10px; font-size: 13px;
            font-weight: 600; cursor: pointer; transition: all 0.2s;
            font-family: inherit; text-align: center;
        }
        .copy-btn:hover { background: rgba(0,255,170,0.2); transform: none; box-shadow: none; }
        .copy-btn::after { display: none; }

        /* ── Invoice ── */
        .invoice {
            background: rgba(5,8,16,0.9); border-radius: 16px; padding: 20px;
            font-family: monospace; font-size: 14px;
            direction: ltr; text-align: left; line-height: 2;
            border: 1px solid rgba(99,102,241,0.15);
            color: #94a3b8;
        }
        .invoice b { color: #e0e7ff; }

        .two-btn { display: flex; gap: 10px; margin-top: 14px; }
        .two-btn button, .two-btn .btn { flex: 1; }
        .section-title { font-size: 14px; color: #64748b; margin-bottom: 10px; font-weight: 500; }
        .success-icon { font-size: 56px; text-align: center; margin: 10px 0; animation: bounceIn 0.6s ease; }
        @keyframes bounceIn { 0%{transform:scale(0.5);opacity:0} 70%{transform:scale(1.15)} 100%{transform:scale(1);opacity:1} }
        .cart-search { display: flex; gap: 10px; }
        .cart-search input { flex: 1; margin: 0; }
        .cart-search button { width: auto; padding: 13px 20px; }

        /* ── Modal ── */
        .modal-overlay {
            position: fixed; inset: 0;
            background: rgba(0,0,0,0.82);
            backdrop-filter: blur(6px);
            z-index: 1000; display: flex;
            align-items: center; justify-content: center; padding: 20px;
        }
        .modal-overlay.hidden { display: none; }
        .modal-box {
            background: rgba(12,15,28,0.97);
            border: 1px solid rgba(99,102,241,0.35);
            border-radius: 22px; padding: 30px 26px;
            width: 100%; max-width: 370px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,255,255,0.04);
            animation: modalPop 0.3s cubic-bezier(.34,1.56,.64,1);
        }
        @keyframes modalPop { from{opacity:0;transform:scale(0.88) translateY(20px)} to{opacity:1;transform:scale(1) translateY(0)} }
        .modal-title { font-size: 18px; font-weight: 800; color: #e0e7ff; margin-bottom: 6px; }
        .modal-sub { font-size: 13px; color: #64748b; margin-bottom: 18px; line-height: 1.7; }
        .modal-input {
            width: 100%; padding: 14px; border-radius: 12px;
            border: 1.5px solid rgba(99,102,241,0.25);
            background: rgba(5,8,16,0.9); color: #fff;
            font-size: 18px; font-family: inherit;
            direction: ltr; text-align: center;
            letter-spacing: 5px; margin-bottom: 14px;
        }
        .modal-input:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.2); }
        .modal-btn {
            width: 100%; padding: 14px;
            background: linear-gradient(135deg,#0ea5e9,#6366f1);
            color: #fff; border: none; border-radius: 12px;
            font-size: 15px; font-weight: 700; cursor: pointer;
            font-family: inherit; transition: all 0.2s;
            box-shadow: 0 4px 18px rgba(99,102,241,0.35);
        }
        .modal-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(99,102,241,0.5); }
        .modal-err { color: #f87171; font-size: 13px; margin-bottom: 10px; min-height: 18px; }

        /* ── Code Display ── */
        .otp-display {
            font-size: 36px; font-weight: 900; color: #0ea5e9;
            text-align: center; letter-spacing: 10px;
            padding: 18px 10px; background: rgba(14,165,233,0.06);
            border-radius: 16px; margin: 14px 0;
            border: 1px solid rgba(14,165,233,0.2);
            font-family: monospace;
        }

        /* ── FAB ── */
        .fab-support {
            position: fixed; bottom: 26px; right: 20px;
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            color: #fff; border-radius: 50px; padding: 11px 20px;
            font-size: 13px; font-weight: 700; text-decoration: none;
            box-shadow: 0 4px 22px rgba(99,102,241,0.5);
            display: flex; align-items: center; gap: 7px;
            z-index: 999; transition: all 0.25s; font-family: inherit;
        }
        .fab-support:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(99,102,241,0.65); }
        .fab-menu-btn {
            position: fixed; bottom: 26px; left: 20px;
            background: rgba(15,18,30,0.95); color: #a5b4fc;
            border-radius: 50%; width: 50px; height: 50px; font-size: 24px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 22px rgba(0,0,0,0.6); cursor: pointer;
            z-index: 999; border: 1px solid rgba(99,102,241,0.3); transition: all 0.2s;
        }
        .fab-menu-btn:hover { background: rgba(99,102,241,0.2); }
        .fab-dropdown {
            position: fixed; bottom: 86px; left: 16px;
            background: rgba(12,15,28,0.97); border: 1px solid rgba(99,102,241,0.25);
            border-radius: 18px; padding: 12px;
            min-width: 190px; z-index: 998;
            box-shadow: 0 12px 40px rgba(0,0,0,0.7); display: none;
        }
        .fab-dropdown.open { display: block; animation: modalPop 0.2s ease; }
        .fab-dropdown a {
            display: flex; align-items: center; gap: 10px;
            padding: 11px 14px; color: #e0e7ff;
            text-decoration: none; border-radius: 12px;
            font-size: 14px; transition: 0.15s;
        }
        .fab-dropdown a:hover { background: rgba(99,102,241,0.12); }

        /* ── Profile ── */
        .profile-hero {
            background: linear-gradient(135deg, rgba(14,165,233,0.12), rgba(99,102,241,0.12));
            border-radius: 20px; padding: 22px;
            display: flex; align-items: center; gap: 18px;
            margin-bottom: 22px;
            border: 1px solid rgba(99,102,241,0.2);
        }
        .profile-avatar {
            width: 64px; height: 64px; border-radius: 50%;
            background: linear-gradient(135deg, #0ea5e9, #7b2ff7);
            display: flex; align-items: center; justify-content: center;
            font-size: 26px; font-weight: 900; color: #fff; flex-shrink: 0;
            box-shadow: 0 4px 20px rgba(99,102,241,0.5);
        }
        .profile-info h2 { font-size: 18px; font-weight: 800; color: #e0e7ff; }
        .profile-info p { font-size: 13px; color: #64748b; margin-top: 4px; }
        .profile-info .tg-tag { color: #0ea5e9; font-weight: 600; }
        .profile-stats {
            display: grid; grid-template-columns: 1fr 1fr 1fr;
            gap: 12px; margin-bottom: 22px;
        }
        .stat-card {
            background: rgba(20,24,40,0.7);
            border-radius: 16px; padding: 16px 12px; text-align: center;
            border: 1px solid rgba(99,102,241,0.12);
        }
        .stat-num { font-size: 22px; font-weight: 900; color: #e0e7ff; }
        .stat-label { font-size: 11px; color: #475569; margin-top: 4px; }
        .profile-order {
            background: rgba(15,18,30,0.8);
            border-radius: 18px; padding: 18px;
            margin-bottom: 14px;
            border: 1px solid rgba(99,102,241,0.12);
            transition: border-color 0.2s;
        }
        .profile-order:hover { border-color: rgba(99,102,241,0.3); }
        .profile-order.approved { border-right: 3px solid #22c55e; }
        .profile-order.pending  { border-right: 3px solid #f59e0b; }
        .profile-order.rejected { border-right: 3px solid #ef4444; }
        .profile-order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .order-plan-name { font-size: 15px; font-weight: 700; color: #c7d2fe; }
        .order-meta { font-size: 12px; color: #475569; margin-top: 6px; display: flex; gap: 14px; flex-wrap: wrap; }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <span class="logo">🐆 چیتا نت</span>
            {% if user_tg %}
            <a href="/profile" class="cart-btn">👤 پروفایل من</a>
            {% else %}
            <a href="/cart" class="cart-btn">🛒 سبد خرید</a>
            {% endif %}
        </div>
'''

BASE_END = '''
    </div>

    <a href="https://t.me/chitaseee" target="_blank" class="fab-support">💬 پشتیبانی</a>
    <div class="fab-menu-btn" onclick="toggleFab()" id="fabBtn">&#8943;</div>
    <div class="fab-dropdown" id="fabDropdown">
        <a href="https://t.me/chitaseee" target="_blank"><span style="font-size:20px;">✈️</span> کانال چیتا نت</a>
    </div>

    <script>
    function toggleFab() {
        document.getElementById('fabDropdown').classList.toggle('open');
    }
    document.addEventListener('click', function(e) {
        var btn = document.getElementById('fabBtn');
        var dd = document.getElementById('fabDropdown');
        if (btn && dd && !btn.contains(e.target) && !dd.contains(e.target)) dd.classList.remove('open');
    });
    </script>
</body>
</html>'''

# ─── HTML PAGES ───────────────────────────────────────────────────────────────

HTML_HOME = BASE_START + '''
<div class="card">
    <p class="section-title" style="margin-bottom:14px; font-size:13px;">✨ پلن مورد نظر را انتخاب کنید</p>
    <form id="orderForm" onsubmit="handleOrder(event)">
        <input type="text" name="name" id="nameInput" placeholder="نام و نام خانوادگی" required>
        <div id="plans-list" style="margin-top:4px;">
            {% for key, plan in plans.items() %}
            <div class="plan" onclick="selectPlan('{{ key }}')" id="plan-{{ key }}">
                <div class="plan-row">
                    <div class="plan-name">{{ plan.name }}</div>
                    <div class="plan-price">{{ "{:,.0f}".format(plan.price) }}<span> تومان</span></div>
                </div>
                <div class="plan-meta">
                    <span class="plan-server">{{ plan.server }}</span>
                    <span class="plan-badge">{{ plan.category }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        <input type="hidden" name="plan_key" id="selected_plan" required>
        <button type="submit" style="margin-top:18px;">🛒 ادامه و پرداخت</button>
    </form>
</div>

<!-- مرحله ۱: دریافت یوزرنیم -->
<div class="modal-overlay hidden" id="modalStep1">
    <div class="modal-box">
        <div class="modal-title">📲 ورود با تلگرام</div>
        <div class="modal-sub">یوزرنیم تلگرام خود را وارد کنید تا کد تأیید دریافت کنید.</div>
        <p class="modal-err" id="err1"></p>
        <input class="modal-input" type="text" id="tgUsernameInput" placeholder="@username" style="letter-spacing:1px; direction:ltr; text-align:center;">
        <button class="modal-btn" onclick="sendOtp()">📨 دریافت کد</button>
    </div>
</div>

<!-- مرحله ۲: نمایش کد و ارسال به ربات -->
<div class="modal-overlay hidden" id="modalStep2">
    <div class="modal-box">
        <div class="modal-title">🤖 کد را به ربات بفرستید</div>
        <div class="modal-sub">این کد را برای ربات <span id="botLinkSpan" style="color:#00aaff; font-weight:bold;"></span> بفرستید:</div>
        <div id="displayCode" class="otp-display"></div>
        <p style="font-size:12px; color:#aaa; text-align:center; margin-bottom:14px;">بعد از فرستادن کد، دکمه زیر را بزنید</p>
        <p class="modal-err" id="err2"></p>
        <button class="modal-btn" onclick="verifyOtp()">✅ کد را فرستادم — تأیید کن</button>
        <button onclick="document.getElementById('modalStep2').classList.add('hidden'); document.getElementById('modalStep1').classList.remove('hidden');"
            style="margin-top:10px; background:transparent; border:1px solid #444; color:#aaa; font-size:13px; padding:10px; width:100%; border-radius:10px; cursor:pointer;">
            ← تغییر یوزرنیم
        </button>
    </div>
</div>

<script>
    var selectedPlan = null;
    var currentCode = null;
    var userLoggedIn = {{ 'true' if user_tg else 'false' }};

    function selectPlan(key) {
        if (selectedPlan) document.getElementById(selectedPlan).classList.remove('selected');
        selectedPlan = 'plan-' + key;
        document.getElementById(selectedPlan).classList.add('selected');
        document.getElementById('selected_plan').value = key;
    }

    function handleOrder(e) {
        e.preventDefault();
        if (userLoggedIn) {
            document.getElementById('orderForm').submit();
        } else {
            document.getElementById('modalStep1').classList.remove('hidden');
        }
    }

    function sendOtp() {
        var username = document.getElementById('tgUsernameInput').value.trim().replace(/^@/, '');
        document.getElementById('err1').textContent = '';
        if (!username) {
            document.getElementById('err1').textContent = '⚠️ یوزرنیم تلگرام را وارد کنید';
            return;
        }
        fetch('/send_otp', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: username})
        }).then(r => r.json()).then(data => {
            if (data.ok) {
                currentCode = data.code;
                document.getElementById('displayCode').textContent = data.code;
                var botName = data.bot_username || 'ربات';
                document.getElementById('botLinkSpan').innerHTML = '<a href="https://t.me/' + botName + '" target="_blank" style="color:#00aaff;">@' + botName + '</a>';
                document.getElementById('modalStep1').classList.add('hidden');
                document.getElementById('modalStep2').classList.remove('hidden');
            } else {
                document.getElementById('err1').textContent = data.error || '⚠️ خطا';
            }
        }).catch(() => {
            document.getElementById('err1').textContent = '⚠️ خطا در اتصال';
        });
    }

    function verifyOtp() {
        document.getElementById('err2').textContent = '';
        if (!currentCode) return;
        fetch('/verify_otp', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code: currentCode})
        }).then(r => r.json()).then(data => {
            if (data.ok) {
                document.getElementById('modalStep2').classList.add('hidden');
                document.getElementById('orderForm').submit();
            } else {
                document.getElementById('err2').textContent = data.error || '⚠️ تأیید نشد';
            }
        }).catch(() => {
            document.getElementById('err2').textContent = '⚠️ خطا در اتصال';
        });
    }
</script>
''' + BASE_END

HTML_UPLOAD = BASE_START + '''
<div class="card">
    <h3 style="margin-bottom:12px;">✨ پیش‌فاکتور خرید ✨</h3>
    <div class="invoice">
        ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄<br>
        🆔 کد سفارش: <b>{{ order_code }}</b><br>
        🌍 سرور: {{ plan.server }}<br>
        📦 پلن: {{ plan.name }}<br>
        💰 مبلغ: <b>{{ "{:,.0f}".format(plan.price) }} تومان</b><br>
        💳 کارت به کارت: <b dir="ltr">{{ bank_card }}</b><br>
        👤 به نام: {{ bank_owner }}<br>
        ⚠️ بعد از واریز، رسید را ارسال کنید<br>
        ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
    </div>
    <form method="POST" action="/upload_receipt" enctype="multipart/form-data" style="margin-top: 18px;">
        <input type="hidden" name="order_code" value="{{ order_code }}">
        <input type="hidden" name="name" value="{{ name }}">
        <p class="section-title" style="margin-top:8px;">تصویر رسید پرداخت را انتخاب کنید:</p>
        <input type="file" name="receipt" accept="image/*" required>
        <button type="submit" style="margin-top:10px;">📤 رسید رو ارسال کنید</button>
    </form>
</div>
''' + BASE_END

HTML_PROFILE = BASE_START + '''
<style>
    @keyframes slideIn { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
    .profile-order { animation: slideIn 0.35s ease both; }
    {% for i in range(20) %}.profile-order:nth-child({{ i+1 }}) { animation-delay: {{ i*0.06 }}s; } {% endfor %}
</style>

<!-- کارت پروفایل -->
<div class="profile-hero" style="animation: fadeUp 0.4s ease;">
    <div class="profile-avatar">{{ username_initial }}</div>
    <div class="profile-info" style="flex:1;">
        <h2>{{ display_name }}</h2>
        <p>تلگرام: <span class="tg-tag">@{{ tg_username or user_tg }}</span></p>
    </div>
    <a href="/logout_user" style="color:#ef4444; font-size:12px; text-decoration:none; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.25); padding:7px 14px; border-radius:10px; white-space:nowrap; transition:0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.18)'" onmouseout="this.style.background='rgba(239,68,68,0.08)'">خروج 🚪</a>
</div>

<!-- آمار -->
<div class="profile-stats" style="animation: fadeUp 0.4s 0.1s ease both;">
    <div class="stat-card">
        <div class="stat-num">{{ orders|length }}</div>
        <div class="stat-label">کل سفارشات</div>
    </div>
    <div class="stat-card">
        <div class="stat-num" style="color:#22c55e;">{{ approved_count }}</div>
        <div class="stat-label">تایید شده</div>
    </div>
    <div class="stat-card">
        <div class="stat-num" style="color:#fbbf24;">{{ pending_count }}</div>
        <div class="stat-label">در انتظار</div>
    </div>
</div>

<!-- سفارشات -->
<div class="card" style="animation: fadeUp 0.4s 0.15s ease both;">
    {% if not orders %}
    <div style="text-align:center; padding:36px 0;">
        <div style="font-size:52px; margin-bottom:14px;">🛒</div>
        <p style="color:#475569; font-size:15px; margin-bottom:4px;">هنوز سفارشی ثبت نکرده‌اید</p>
        <p style="color:#334155; font-size:13px;">یک پلن انتخاب کنید و شروع کنید!</p>
        <a href="/" class="btn" style="margin-top:20px; max-width:220px; display:inline-block;">🚀 خرید VPN</a>
    </div>
    {% else %}
    <p class="section-title">سفارشات شما — {{ orders|length }} سفارش</p>

    {% for order in orders %}
    <div class="profile-order {{ order[5] }}">
        <div class="profile-order-header">
            <span class="order-plan-name">{{ order[7] }}</span>
            {% if order[5] == 'pending' %}
                <span class="badge badge-pending">⏳ در انتظار</span>
            {% elif order[5] == 'approved' %}
                <span class="badge badge-approved">✅ فعال</span>
            {% else %}
                <span class="badge badge-rejected">❌ رد شده</span>
            {% endif %}
        </div>
        <div class="order-meta">
            <span>💰 {{ "{:,.0f}".format(order[4]) }} تومان</span>
            <span>📅 {{ order[6] }}</span>
            <span style="color:#334155; font-size:11px;">{{ order[1] }}</span>
        </div>

        {% if order[5] == 'approved' and order[9] %}
        <div style="margin-top:12px;">
            <p style="font-size:12px; color:#22c55e; font-weight:600; margin-bottom:6px;">🔗 کانفیگ اختصاصی شما:</p>
            <div class="config-box" id="cfg-{{ order[0] }}">{{ order[9] }}</div>
            <button class="copy-btn" onclick="copyConfig('cfg-{{ order[0] }}', this)">📋 کپی کانفیگ</button>
        </div>
        {% elif order[5] == 'pending' %}
        <div style="margin-top:10px; padding:10px 14px; background:rgba(245,158,11,0.06); border-radius:10px; border:1px solid rgba(245,158,11,0.15);">
            <p style="color:#fbbf24; font-size:12px;">⏳ رسید دریافت شد — در انتظار تایید ادمین هستید</p>
        </div>
        {% elif order[5] == 'rejected' %}
        <div style="margin-top:10px; padding:10px 14px; background:rgba(239,68,68,0.06); border-radius:10px; border:1px solid rgba(239,68,68,0.15);">
            <p style="color:#f87171; font-size:12px;">❌ سفارش تایید نشد — برای راهنمایی با پشتیبانی تماس بگیرید</p>
        </div>
        {% endif %}
    </div>
    {% endfor %}
    {% endif %}
</div>

<a href="/" class="btn btn-outline" style="animation: fadeUp 0.4s 0.25s ease both;">🏠 بازگشت به صفحه اصلی</a>

<script>
function copyConfig(id, btn) {
    var text = document.getElementById(id).innerText.trim();
    navigator.clipboard.writeText(text).then(function() {
        btn.textContent = '✅ کپی شد!';
        btn.style.background = 'rgba(34,197,94,0.2)';
        btn.style.color = '#22c55e';
        btn.style.borderColor = 'rgba(34,197,94,0.3)';
        setTimeout(function(){ btn.textContent = '📋 کپی کانفیگ'; btn.style.background=''; btn.style.color=''; btn.style.borderColor=''; }, 2500);
    });
}
</script>
''' + BASE_END

HTML_CART = BASE_START + '''
<div class="card">
    <h3 style="margin-bottom:14px;">🛒 پیگیری سفارش</h3>
    <p class="section-title">کد سفارش خود را وارد کنید:</p>
    <form method="GET" action="/cart" style="margin-top:10px;">
        <div class="cart-search">
            <input type="text" name="code" placeholder="کد سفارش (مثال: A1B2C3D4)" value="{{ search_code or '' }}" style="text-transform:uppercase;" required>
            <button type="submit" style="width:auto; padding: 12px 22px; border-radius:10px;">🔍 جستجو</button>
        </div>
    </form>

    {% if order %}
    <hr style="margin-top:18px;">
    <div style="margin-top:14px;">
        <p><b>🆔 کد سفارش:</b> {{ order[1] }}</p>
        <p style="margin-top:6px;"><b>👤 نام:</b> {{ order[2] }}</p>
        <p style="margin-top:6px;"><b>📦 پلن:</b> {{ order[7] }}</p>
        <p style="margin-top:6px;"><b>💰 مبلغ:</b> {{ "{:,.0f}".format(order[4]) }} تومان</p>
        <p style="margin-top:6px;"><b>⏱ تاریخ:</b> {{ order[6] }}</p>
        <p style="margin-top:8px;"><b>وضعیت:</b>
        {% if order[5] == 'pending' %}
            <span class="badge badge-pending">⏳ در انتظار تایید</span>
            <p style="color:#aaa; font-size:13px; margin-top:8px;">رسید شما دریافت شد. لطفاً منتظر تایید ادمین باشید.</p>
        {% elif order[5] == 'approved' %}
            <span class="badge badge-approved">✅ تایید شده</span>
            {% if order[9] %}
            <p style="margin-top:12px; color:#00ffaa; font-weight:bold;">🔗 کانفیگ شما:</p>
            <div class="config-box">{{ order[9] }}</div>
            {% endif %}
        {% else %}
            <span class="badge badge-rejected">❌ رد شده</span>
            <p style="color:#aaa; font-size:13px; margin-top:8px;">با پشتیبانی تماس بگیرید.</p>
        {% endif %}
        </p>
    </div>
    {% elif search_code %}
    <p style="color:#ff6b6b; margin-top:16px;">⚠️ سفارشی با این کد پیدا نشد.</p>
    {% endif %}

    <div class="two-btn" style="margin-top:20px;">
        <a href="/" class="btn btn-outline">🏠 بازگشت به صفحه اصلی</a>
    </div>
</div>
''' + BASE_END

HTML_RECEIPT_SENT = BASE_START + '''
<div class="card" style="text-align:center; animation: fadeUp 0.5s ease;">
    <div class="success-icon">🎉</div>
    <h3 style="font-size:22px; font-weight:900; margin-bottom:8px;
        background:linear-gradient(90deg,#22c55e,#0ea5e9);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        رسید شما ارسال شد!
    </h3>
    <p style="color:#475569; margin-bottom:6px; font-size:14px;">ادمین پس از تایید، کانفیگ را مستقیم به تلگرام شما می‌فرستد.</p>

    {% if user_tg %}
    <div style="background:linear-gradient(135deg,rgba(34,197,94,0.08),rgba(14,165,233,0.08)); border-radius:16px; padding:18px; margin:20px 0; border:1px solid rgba(34,197,94,0.2);">
        <p style="font-size:13px; color:#64748b; margin-bottom:12px;">برای دیدن وضعیت سفارش:</p>
        <a href="/profile" class="btn btn-green" style="max-width:220px; display:inline-block;">👤 پروفایل من</a>
    </div>
    {% else %}
    <div style="background:rgba(14,165,233,0.06); border-radius:16px; padding:18px; margin:20px 0; border:1px solid rgba(14,165,233,0.2);">
        <p style="font-size:13px; color:#64748b;">کد پیگیری سفارش:</p>
        <p style="font-size:28px; font-weight:900; color:#0ea5e9; letter-spacing:4px; margin-top:8px; font-family:monospace;">{{ order_code }}</p>
        <p style="font-size:11px; color:#334155; margin-top:6px;">این کد را ذخیره کنید</p>
    </div>
    {% endif %}

    <div class="two-btn">
        {% if user_tg %}
        <a href="/profile" class="btn btn-green">👤 پروفایل من</a>
        {% else %}
        <a href="/cart?code={{ order_code }}" class="btn btn-green">🔍 پیگیری سفارش</a>
        {% endif %}
        <a href="/" class="btn btn-outline">🏠 بازگشت</a>
    </div>
</div>
''' + BASE_END

HTML_ADMIN = BASE_START + '''
<style>
    .admin-tabs { display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap; }
    .tab-btn { flex: 1; padding: 10px; border-radius: 10px; border: 2px solid #00aaff44; background: transparent; color: #aaa; font-size: 14px; cursor: pointer; font-family: Tahoma; transition: 0.2s; min-width: 120px; }
    .tab-btn.active { background: linear-gradient(90deg,#00aaff,#0066cc); color: #fff; border-color: transparent; }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .plan-card { background: #1e1f2c; border-radius: 14px; padding: 16px; margin-bottom: 14px; border: 1px solid #333; }
    .plan-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .plan-card-title { color: #00aaff; font-weight: bold; font-size: 15px; }
    .plan-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .plan-grid input { margin: 0; padding: 9px 12px; font-size: 14px; }
    .plan-grid label { font-size: 12px; color: #888; margin-bottom: 2px; display: block; }
    .field-group { display: flex; flex-direction: column; }
    .btn-delete { background: #f443361a; border: 1px solid #f44336; color: #f44336; border-radius: 8px; padding: 6px 14px; font-size: 13px; cursor: pointer; font-family: Tahoma; transition: 0.2s; width: auto; }
    .btn-delete:hover { background: #f44336; color: #fff; }
    .btn-save-plan { background: linear-gradient(90deg,#22c55e,#16a34a); width: 100%; margin-top: 10px; padding: 10px; border-radius: 10px; border: none; color: #fff; font-size: 15px; font-weight: bold; cursor: pointer; font-family: Tahoma; }
    .add-plan-section { background: #0d0f1c; border-radius: 14px; padding: 18px; border: 1px dashed #00aaff44; }
    .add-plan-section h4 { color: #00aaff; margin-bottom: 14px; }
    .bank-form input { margin: 8px 0; }
    .pending-count { background: #ff9800; border-radius: 50%; width: 22px; height: 22px; font-size: 12px; display: inline-flex; align-items: center; justify-content: center; margin-right: 4px; }
</style>

<div class="admin-panel">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <h2>🔧 پنل مدیریت</h2>
        <a href="/admin_logout" style="color:#f44336; font-size:13px; text-decoration:none; border:1px solid #f443364d; padding:6px 14px; border-radius:8px;">🚪 خروج</a>
    </div>

    <div class="admin-tabs">
        <button class="tab-btn active" onclick="showTab('orders', this)">
            📋 سفارشات
            {% if orders %}
            <span class="pending-count">{{ orders|length }}</span>
            {% endif %}
        </button>
        <button class="tab-btn" onclick="showTab('plans', this)">📦 مدیریت پلن‌ها</button>
        <button class="tab-btn" onclick="showTab('bank', this)">💳 تنظیمات بانکی</button>
    </div>

    <!-- TAB: Orders -->
    <div id="tab-orders" class="tab-content active">
        {% if not orders %}
        <div style="text-align:center; padding:40px; color:#aaa;">
            <div style="font-size:48px; margin-bottom:12px;">✅</div>
            <p>هیچ سفارش در انتظاری وجود ندارد.</p>
        </div>
        {% endif %}
        {% for order in orders %}
        <div class="order-item">
            <b>🆔 کد:</b> {{ order[1] }}&nbsp;&nbsp;
            <b>👤 نام:</b> {{ order[2] }}<br>
            <b>💰 مبلغ:</b> {{ "{:,.0f}".format(order[4]) }} تومان&nbsp;&nbsp;
            <b>📦 پلن:</b> {{ order[7] }}<br>
            <b>⏱ تاریخ:</b> {{ order[6] }}<br>
            {% if order[10] %}
            <b>📲 تلگرام مشتری:</b> <span style="color:#00aaff;">{{ order[10] }}</span><br>
            {% endif %}
            <span class="badge badge-pending">⏳ در انتظار تایید</span>
            <form method="POST" action="/approve/{{ order[0] }}" style="margin-top: 10px;">
                <textarea name="config" rows="2" placeholder="لینک یا کد کانفیگ را اینجا بنویسید..." required style="font-size:13px;"></textarea>
                <button type="submit" style="background:linear-gradient(90deg,#22c55e,#16a34a); padding:11px; font-size:15px;">✅ تایید و ارسال کانفیگ</button>
            </form>
            <a href="/reject/{{ order[0] }}" onclick="return confirm('مطمئنید؟')" style="color:#ff5555; font-size:13px; display:block; margin-top:8px;">❌ رد سفارش</a>
        </div>
        {% endfor %}
    </div>

    <!-- TAB: Plans -->
    <div id="tab-plans" class="tab-content">
        <p style="color:#aaa; font-size:13px; margin-bottom:14px;">پلن‌های موجود را ویرایش کنید یا پلن جدید اضافه کنید:</p>
        {% for key, plan in plans.items() %}
        <div class="plan-card">
            <div class="plan-card-header">
                <span class="plan-card-title">{{ plan.name }}</span>
                <form method="POST" action="/delete_plan/{{ key }}" style="display:inline;" onsubmit="return confirm('این پلن حذف شود؟')">
                    <button type="submit" class="btn-delete">🗑 حذف</button>
                </form>
            </div>
            <form method="POST" action="/update_plan/{{ key }}">
                <div class="plan-grid">
                    <div class="field-group"><label>نام پلن</label><input type="text" name="name" value="{{ plan.name }}" required></div>
                    <div class="field-group"><label>قیمت (تومان)</label><input type="number" name="price" value="{{ plan.price }}" required min="0"></div>
                    <div class="field-group"><label>سرور</label><input type="text" name="server" value="{{ plan.server }}" required></div>
                    <div class="field-group"><label>دسته‌بندی</label><input type="text" name="category" value="{{ plan.category }}" required></div>
                </div>
                <button type="submit" class="btn-save-plan">💾 ذخیره تغییرات</button>
            </form>
        </div>
        {% endfor %}
        <div class="add-plan-section" style="margin-top:20px;">
            <h4>➕ افزودن پلن جدید</h4>
            <form method="POST" action="/add_plan">
                <div class="plan-grid">
                    <div class="field-group"><label>نام پلن</label><input type="text" name="name" placeholder="مثال: دو ماهه 3 گیگابایت" required></div>
                    <div class="field-group"><label>قیمت (تومان)</label><input type="number" name="price" placeholder="مثال: 500000" required min="0"></div>
                    <div class="field-group"><label>سرور</label><input type="text" name="server" placeholder="مثال: 🇩🇪 آلمان"></div>
                    <div class="field-group"><label>دسته‌بندی</label><input type="text" name="category" placeholder="مثال: ویژه"></div>
                </div>
                <button type="submit" class="btn-save-plan" style="background:linear-gradient(90deg,#00aaff,#0066cc);">➕ افزودن پلن جدید</button>
            </form>
        </div>
    </div>

    <!-- TAB: Bank -->
    <div id="tab-bank" class="tab-content">
        <div class="bank-form">
            <p style="color:#aaa; font-size:13px; margin-bottom:10px;">شماره کارت و نام صاحب حساب برای دریافت پرداخت:</p>
            <form method="POST" action="/update_bank">
                <label style="font-size:12px; color:#888;">شماره کارت</label>
                <input type="text" name="bank_card" value="{{ bank_card }}" style="direction:ltr; letter-spacing:2px;">
                <label style="font-size:12px; color:#888;">نام صاحب حساب</label>
                <input type="text" name="bank_owner" value="{{ bank_owner }}">
                <button type="submit" style="margin-top:10px;">💾 ذخیره اطلاعات بانکی</button>
            </form>
        </div>
    </div>
</div>

<script>
function showTab(name, el) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    if (el) el.classList.add('active');
}
window.addEventListener('DOMContentLoaded', function() {
    var params = new URLSearchParams(window.location.search);
    var tab = params.get('tab');
    var msg = params.get('msg');
    if (tab) { var btns = document.querySelectorAll('.tab-btn'); var idx = ['orders','plans','bank'].indexOf(tab); if(idx>=0) showTab(tab, btns[idx]); }
    if (msg) {
        var msgs = { saved: '✅ با موفقیت ذخیره شد', added: '✅ پلن جدید اضافه شد', deleted: '🗑 پلن حذف شد' };
        var toast = document.createElement('div');
        toast.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#22c55e;color:#fff;padding:12px 28px;border-radius:12px;font-size:15px;font-weight:bold;z-index:9999;box-shadow:0 4px 20px #0005;';
        toast.textContent = msgs[msg] || '✅ ذخیره شد';
        document.body.appendChild(toast);
        setTimeout(function(){ toast.style.opacity='0'; toast.style.transition='opacity 0.5s'; setTimeout(function(){ toast.remove(); },500); }, 2500);
    }
});
</script>
''' + BASE_END

HTML_MESSAGE = BASE_START + '''
<div class="card">
    <h3>{{ title }}</h3>
    <p style="margin-top:10px; color:#aaa;">{{ message }}</p>
    <div class="two-btn" style="margin-top:20px;">
        <a href="/" class="btn">🏠 بازگشت به صفحه اصلی</a>
    </div>
</div>
''' + BASE_END

HTML_LOGIN = BASE_START + '''
<div class="card" style="max-width:380px; margin:40px auto;">
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:48px;">🔐</div>
        <h3 style="color:#00aaff; margin-top:8px;">ورود به پنل مدیریت</h3>
    </div>
    {% if error %}
    <p style="color:#f44336; text-align:center; margin-bottom:10px; font-size:14px;">❌ {{ error }}</p>
    {% endif %}
    <form method="POST" action="/admin_login">
        <label style="font-size:12px; color:#888;">رمز عبور</label>
        <input type="password" name="password" placeholder="رمز عبور ادمین را وارد کنید" autofocus required>
        <button type="submit" style="margin-top:10px;">🔑 ورود به پنل</button>
    </form>
</div>
''' + BASE_END

# ─── DATABASE ─────────────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_code TEXT UNIQUE,
        user_name TEXT,
        user_mobile TEXT,
        amount INTEGER,
        status TEXT DEFAULT 'pending',
        config TEXT DEFAULT '',
        created_at TIMESTAMP,
        plan_name TEXT,
        plan_key TEXT,
        telegram_id TEXT DEFAULT ''
    )''')
    try:
        c.execute("ALTER TABLE orders ADD COLUMN telegram_id TEXT DEFAULT ''")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

# ─── SETTINGS ─────────────────────────────────────────────────────────────────

def save_settings():
    with open('settings.json', 'w') as f:
        json.dump({'plans': PLANS, 'bank_card': BANK_CARD, 'bank_owner': BANK_OWNER}, f)

def load_settings():
    global PLANS, BANK_CARD, BANK_OWNER
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            data = json.load(f)
            PLANS = data.get('plans', PLANS)
            BANK_CARD = data.get('bank_card', BANK_CARD)
            BANK_OWNER = data.get('bank_owner', BANK_OWNER)

load_settings()

# ─── TELEGRAM HELPERS ─────────────────────────────────────────────────────────

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    try:
        files = {'photo': open(photo_path, 'rb')}
        data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption}
        requests.post(url, files=files, data=data, timeout=10)
    except:
        pass

def admin_required():
    return session.get('admin_logged_in') == True

def current_user_tg():
    return session.get('telegram_id', '')

# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML_HOME, plans=PLANS, user_tg=current_user_tg())

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    username = str(data.get('username', '')).strip().lstrip('@')
    if not username:
        return jsonify({'ok': False, 'error': '⚠️ یوزرنیم را وارد کنید'})
    code = str(random.randint(100000, 999999))
    # کد قدیمی همین یوزر را پاک کن
    for k in list(pending_otp.keys()):
        if pending_otp[k].get('username') == username:
            del pending_otp[k]
    pending_otp[code] = {'username': username, 'ts': time.time()}
    return jsonify({'ok': True, 'code': code, 'bot_username': BOT_USERNAME})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    code = str(data.get('code', '')).strip()
    if not code:
        return jsonify({'ok': False, 'error': '⚠️ کد معتبر نیست'})
    if code in verified_codes:
        info = verified_codes.pop(code)
        pending_otp.pop(code, None)
        session['telegram_id'] = info['chat_id']
        session['telegram_username'] = info['username']
        return jsonify({'ok': True})
    entry = pending_otp.get(code)
    if not entry:
        return jsonify({'ok': False, 'error': '⚠️ کد یافت نشد — دوباره درخواست کنید'})
    if time.time() - entry['ts'] > 300:
        del pending_otp[code]
        return jsonify({'ok': False, 'error': '⚠️ کد منقضی شده — دوباره دریافت کنید'})
    return jsonify({'ok': False, 'error': '⏳ هنوز کد را به ربات نفرستادید'})

@app.route('/logout_user')
def logout_user():
    session.pop('telegram_id', None)
    return redirect('/')

@app.route('/profile')
def profile():
    tg = current_user_tg()
    if not tg:
        return redirect('/cart')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, order_code, user_name, user_mobile, amount, status, created_at, plan_name, plan_key, config, telegram_id FROM orders WHERE telegram_id = ? ORDER BY id DESC", (tg,))
    orders = c.fetchall()
    conn.close()
    tg_username = session.get('telegram_username', '')
    display_name = f"@{tg_username}" if tg_username else f"کاربر {str(tg)[-4:]}"
    first_char = tg_username[0].upper() if tg_username else '؟'
    approved_count = sum(1 for o in orders if o[5] == 'approved')
    pending_count  = sum(1 for o in orders if o[5] == 'pending')
    return render_template_string(HTML_PROFILE, orders=orders, user_tg=tg,
                                  tg_username=tg_username, display_name=display_name,
                                  username_initial=first_char,
                                  approved_count=approved_count, pending_count=pending_count)

@app.route('/create_order', methods=['POST'])
def create_order():
    name = request.form['name']
    plan_key = request.form['plan_key']
    if plan_key not in PLANS:
        return render_template_string(HTML_MESSAGE, title="خطا", message="پلن نامعتبر است", user_tg=current_user_tg())
    plan = PLANS[plan_key]
    order_code = hashlib.md5(f"{name}{plan_key}{datetime.now()}".encode()).hexdigest()[:8].upper()
    tg = current_user_tg()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (order_code, user_name, user_mobile, amount, created_at, status, plan_name, plan_key, telegram_id) VALUES (?,?,?,?,?,?,?,?,?)",
              (order_code, name, '', plan['price'], datetime.now(), 'pending', plan['name'], plan_key, tg))
    conn.commit()
    conn.close()
    return render_template_string(HTML_UPLOAD, order_code=order_code, plan=plan, name=name,
                                  bank_card=BANK_CARD, bank_owner=BANK_OWNER, user_tg=tg)

@app.route('/upload_receipt', methods=['POST'])
def upload_receipt():
    order_code = request.form['order_code']
    name = request.form.get('name', '')
    file = request.files['receipt']
    if not file:
        return render_template_string(HTML_MESSAGE, title="خطا", message="لطفا عکس رسید را انتخاب کنید", user_tg=current_user_tg())
    os.makedirs('static/uploads', exist_ok=True)
    filename = f"receipt_{order_code}.jpg"
    filepath = os.path.join('static/uploads', filename)
    file.save(filepath)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT amount, plan_name FROM orders WHERE order_code = ?", (order_code,))
    order = c.fetchone()
    conn.close()
    amount = order[0] if order else 0
    plan_name = order[1] if order else "نامشخص"
    report = f"🛍️ <b>سفارش جدید</b>\n\n👤 نام: {name}\n📦 پلن: {plan_name}\n💰 مبلغ: {amount:,} تومان\n🆔 کد: {order_code}\n⌛️ {datetime.now().strftime('%Y/%m/%d %H:%M')}"
    send_telegram_message(ADMIN_CHAT_ID, report)
    send_telegram_photo(filepath, f"📸 رسید\n🆔 {order_code}\n👤 {name}\n💰 {amount:,} تومان")
    return render_template_string(HTML_RECEIPT_SENT, order_code=order_code, user_tg=current_user_tg())

@app.route('/cart')
def cart():
    tg = current_user_tg()
    if tg:
        return redirect('/profile')
    search_code = request.args.get('code', '').strip().upper()
    order = None
    if search_code:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id, order_code, user_name, user_mobile, amount, status, created_at, plan_name, plan_key, config, telegram_id FROM orders WHERE order_code = ?", (search_code,))
        order = c.fetchone()
        conn.close()
    return render_template_string(HTML_CART, order=order, search_code=search_code, user_tg=tg)

@app.route('/admin', methods=['GET'])
def admin():
    if not admin_required():
        return render_template_string(HTML_LOGIN, error=None, user_tg='')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, order_code, user_name, user_mobile, amount, status, created_at, plan_name, plan_key, config, telegram_id FROM orders WHERE status = 'pending' ORDER BY id DESC")
    orders = c.fetchall()
    conn.close()
    return render_template_string(HTML_ADMIN, orders=orders, plans=PLANS, bank_card=BANK_CARD, bank_owner=BANK_OWNER, user_tg='')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    pw = request.form.get('password', '')
    if pw == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return redirect(url_for('admin'))
    return render_template_string(HTML_LOGIN, error='رمز عبور اشتباه است', user_tg='')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))

@app.route('/update_plan/<plan_key>', methods=['POST'])
def update_plan(plan_key):
    if not admin_required(): return redirect(url_for('admin'))
    global PLANS
    if plan_key in PLANS:
        PLANS[plan_key]['name'] = request.form['name']
        PLANS[plan_key]['price'] = int(request.form['price'])
        PLANS[plan_key]['server'] = request.form['server']
        PLANS[plan_key]['category'] = request.form['category']
        save_settings()
    return redirect(url_for('admin') + '?tab=plans&msg=saved')

@app.route('/add_plan', methods=['POST'])
def add_plan():
    if not admin_required(): return redirect(url_for('admin'))
    global PLANS
    name = request.form['name']
    price = int(request.form['price'])
    server = request.form.get('server', '🌍 بین‌الملل')
    category = request.form.get('category', 'عادی')
    key = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:10]
    PLANS[key] = {'name': name, 'price': price, 'server': server, 'category': category}
    save_settings()
    return redirect(url_for('admin') + '?tab=plans&msg=added')

@app.route('/delete_plan/<plan_key>', methods=['POST'])
def delete_plan(plan_key):
    if not admin_required(): return redirect(url_for('admin'))
    global PLANS
    if plan_key in PLANS:
        del PLANS[plan_key]
        save_settings()
    return redirect(url_for('admin') + '?tab=plans&msg=deleted')

@app.route('/update_bank', methods=['POST'])
def update_bank():
    if not admin_required(): return redirect(url_for('admin'))
    global BANK_CARD, BANK_OWNER
    BANK_CARD = request.form['bank_card']
    BANK_OWNER = request.form['bank_owner']
    save_settings()
    return redirect(url_for('admin') + '?tab=bank&msg=saved')

@app.route('/approve/<int:order_id>', methods=['POST'])
def approve(order_id):
    if not admin_required(): return redirect(url_for('admin'))
    config_text = request.form['config']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE orders SET status = 'approved', config = ? WHERE id = ?", (config_text, order_id))
    c.execute("SELECT telegram_id, order_code, amount, plan_name, user_name FROM orders WHERE id = ?", (order_id,))
    order = c.fetchone()
    conn.commit()
    conn.close()
    if order:
        send_telegram_message(ADMIN_CHAT_ID, f"✅ سفارش {order[1]} تایید شد.\n👤 {order[4]}\n💰 {order[2]:,} تومان")
        if order[0]:
            customer_msg = f"✅ <b>سفارش شما تایید شد!</b>\n\n📦 پلن: {order[3]}\n💰 مبلغ: {order[2]:,} تومان\n\n🔗 کانفیگ شما:\n<code>{config_text}</code>"
            send_telegram_message(order[0], customer_msg)
    return redirect(url_for('admin'))

@app.route('/reject/<int:order_id>')
def reject(order_id):
    if not admin_required(): return redirect(url_for('admin'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT telegram_id, order_code, plan_name FROM orders WHERE id = ?", (order_id,))
    order = c.fetchone()
    c.execute("UPDATE orders SET status = 'rejected' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    if order:
        send_telegram_message(ADMIN_CHAT_ID, f"❌ سفارش {order[1]} رد شد.")
        if order[0]:
            send_telegram_message(order[0], f"❌ سفارش شما ({order[2]}) رد شد.\nبرای اطلاعات بیشتر با پشتیبانی تماس بگیرید: @chitaseee")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
