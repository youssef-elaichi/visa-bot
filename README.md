<div align="center">

# 🤖 Visa Bot — Automatic Visa Appointment Booker

**A Python bot that monitors visa appointment slots 24/7 and auto-books the first available one**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?style=for-the-badge&logo=twilio&logoColor=white)](https://twilio.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org)

</div>

---

## ✨ Features

- 🔄 **24/7 Monitoring** — checks for available slots every X seconds
- 📅 **Auto-booking** — instantly books the first available appointment
- 📱 **WhatsApp alerts** — via Twilio
- 💬 **Telegram alerts** — via Telegram Bot
- 📧 **Auto-registration** — registers a TLS account and activates it via Gmail
- 🌍 **Multi-country** — France, Belgium, Germany, Italy, Netherlands, Spain, Canada
- 🏙️ **Multi-city** — Marrakech, Casablanca, Rabat, Tangier, Fes, Agadir
- 🎨 **React GUI** — generates the bot code automatically from a web interface

---

## 📁 Project Structure

```
visa-bot/
├── visa_bot_full_fixed.py    # Full bot — TLS (France, Belgium, ...)
├── visa_bot_v6_fixed.py      # BLS Spain version
├── visa_bot_gui_fixed.jsx    # React GUI — generates custom code
├── .env.example              # Environment variables template
├── .gitignore
└── README.md
```

---

## ⚡ Quick Setup

### 1. Clone the repository

```bash
git clone https://github.com/youssef-elaichi/visa-bot.git
cd visa-bot
```

### 2. Create your `.env` file

```bash
cp .env.example .env
```

Fill in your details:

```env
FIRST_NAME=John
LAST_NAME=Doe
GMAIL=your@gmail.com
GMAIL_PASS=xxxx xxxx xxxx xxxx
TLS_PASSWORD=YourPassword123!

CITY=marrakech        # marrakech / casablanca / rabat / tanger / fes / agadir
COUNTRY=fr            # fr / be / de / it / nl / es / ca
INTERVAL=10           # check every X seconds

TWILIO_SID=ACxxxxxxxx
TWILIO_TOKEN=xxxxxxxx
WA_PHONE=+212XXXXXXXXX

TG_TOKEN=xxxxxxxxx:xxxxxxxxx
TG_CHAT_ID=xxxxxxxxx
```

### 3. Run the bot

```bash
# Windows
python visa_bot_full_fixed.py

# Linux / Mac
python3 visa_bot_full_fixed.py
```

> ✅ All dependencies are installed automatically on first run — no manual setup needed

---

## 🛠️ Requirements

| Tool | Purpose | Link |
|------|---------|------|
| Python 3.8+ | Run the bot | [python.org](https://python.org) |
| Gmail IMAP | Receive activation email | [Enable IMAP](https://mail.google.com/mail/u/0/#settings/fwdandpop) |
| Gmail App Password | Secure login | [Create one](https://myaccount.google.com/apppasswords) |
| Twilio | WhatsApp notifications | [twilio.com](https://twilio.com) |
| Telegram Bot | Telegram notifications | [@BotFather](https://t.me/BotFather) |

### 📧 Gmail App Password — Steps

1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Enable **2-Step Verification** if not already active
3. **App passwords** → select "Mail" → **Generate**
4. Copy the 16-character password into `.env` under `GMAIL_PASS`

### 💬 Telegram Bot — Steps

1. Open [@BotFather](https://t.me/BotFather) and send `/newbot`
2. Save your **TOKEN**
3. Send `/start` to your new bot
4. Open: `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Copy the **chat_id** from the response

---

## 🌍 Supported Countries

| Country | Code | Platform |
|---------|------|----------|
| 🇫🇷 France | `fr` | TLS Contact |
| 🇧🇪 Belgium | `be` | TLS Contact |
| 🇩🇪 Germany | `de` | TLS Contact |
| 🇮🇹 Italy | `it` | TLS Contact |
| 🇳🇱 Netherlands | `nl` | TLS Contact |
| 🇪🇸 Spain | `es` | BLS Spain |
| 🇨🇦 Canada | `ca` | VFS Global |

---

## 🎨 React GUI

`visa_bot_gui_fixed.jsx` is a React component that generates a fully customized Python script from a clean web interface:

```
Step 1 → Enter your personal info
Step 2 → Select country, city & check interval
Step 3 → Add Twilio & Telegram credentials
Step 4 → Copy the generated code and run it
```

---

## 🔒 Security

> **⚠️ Important** — never push your `.env` file to GitHub

- ✅ All sensitive data stays in `.env` only
- ✅ `.gitignore` automatically excludes `.env` from commits
- ✅ No hardcoded credentials anywhere in the source code

---

## ⚠️ Disclaimer

This bot is intended for personal use only. Please review the terms of service of the platform you are using before running it.

---

## 📄 License

MIT License — free to use with attribution.

---

<div align="center">
Made with ❤️ for Moroccans hunting visa appointments
</div>
