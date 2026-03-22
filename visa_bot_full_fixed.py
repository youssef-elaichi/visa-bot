"""
🤖 VISA BOT — Full Version
=========================================================
✅ Auto-registers a TLS account
✅ Reads Gmail and activates the account
✅ Monitors appointment slots every X seconds
✅ Auto-books the first available slot
✅ Sends WhatsApp + Telegram alerts
✅ Credentials loaded securely from .env
"""

import subprocess, sys, importlib.util

# ══════════════════════════════════════════
# 📦 Smart install — only once
# ══════════════════════════════════════════

def install():
    libs = ["playwright", "twilio", "requests", "python-dotenv"]
    needs = [l for l in libs if importlib.util.find_spec(l.replace("-", "_")) is None]
    if needs:
        print(f"⏳ Installing: {', '.join(needs)}...")
        for lib in needs:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib,
                "--quiet", "--break-system-packages"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ All dependencies installed!\n")
    else:
        print("✅ Dependencies already installed\n")

install()

from playwright.sync_api import sync_playwright
import imaplib, email, re, time, logging, requests, os
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

# ══════════════════════════════════════════
# 🔐 Load credentials from .env
# ══════════════════════════════════════════
# Create a .env file in the same folder:
#
#   FIRST_NAME=XXX
#   LAST_NAME=XXX
#   GMAIL=XXX@gmail.com
#   GMAIL_PASS=xxxx xxxx xxxx xxxx
#   TLS_PASSWORD=XXX
#   CITY=marrakech
#   COUNTRY=fr
#   INTERVAL=10
#   TWILIO_SID=XXX
#   TWILIO_TOKEN=XXX
#   WA_PHONE=+212XXXXXXXXX
#   TG_TOKEN=XXX
#   TG_CHAT_ID=XXX

load_dotenv()

CONFIG = {
    "first_name":       os.getenv("FIRST_NAME",   "XXX"),
    "last_name":        os.getenv("LAST_NAME",     "XXX"),
    "gmail":            os.getenv("GMAIL",         "XXX@gmail.com"),
    "gmail_pass":       os.getenv("GMAIL_PASS",    "XXX"),
    "tls_password":     os.getenv("TLS_PASSWORD",  "XXX"),
    "city":             os.getenv("CITY",          "marrakech"),
    "country":          os.getenv("COUNTRY",       "fr"),
    "interval":         int(os.getenv("INTERVAL",  "10")),
    "twilio_sid":       os.getenv("TWILIO_SID",    "XXX"),
    "twilio_token":     os.getenv("TWILIO_TOKEN",  "XXX"),
    "whatsapp_to":      os.getenv("WA_PHONE",      "+212XXXXXXXXX"),
    "telegram_token":   os.getenv("TG_TOKEN",      "XXX"),
    "telegram_chat_id": os.getenv("TG_CHAT_ID",    "XXX"),
}

# ══════════════════════════════════════════
# URLs by city and country
# ══════════════════════════════════════════

CITY_CODES = {
    "marrakech": "RAK", "casablanca": "CAS",
    "rabat": "RBA", "tanger": "TNG",
    "fes": "FEZ", "agadir": "AGA",
}

COUNTRY_URLS = {
    "fr": "https://fr.tlscontact.com",
    "be": "https://visas-be.tlscontact.com",
    "de": "https://de.tlscontact.com",
    "it": "https://visas-it.tlscontact.com",
    "nl": "https://visas-nl.tlscontact.com",
}

city_code = CITY_CODES.get(CONFIG["city"], "RAK")
base_url  = COUNTRY_URLS.get(CONFIG["country"], "https://fr.tlscontact.com")
country   = CONFIG["country"]

TLS_REGISTER = f"{base_url}/register"
TLS_LOGIN    = f"{base_url}/login/ma{city_code}2{country}"
TLS_APPT     = f"{base_url}/appointment/ma{city_code}2{country}"

# ══════════════════════════════════════════
# 📝 Logging
# ══════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("visa_bot.log", encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════
# 📱 Notifications
# ══════════════════════════════════════════

def send_whatsapp(msg: str):
    try:
        Client(CONFIG["twilio_sid"], CONFIG["twilio_token"]).messages.create(
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{CONFIG['whatsapp_to']}",
            body=msg
        )
        log.info("✅ WhatsApp sent!")
    except Exception as e:
        log.error(f"❌ WhatsApp error: {e}")


def send_telegram(msg: str):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendMessage"
        requests.post(url, json={"chat_id": CONFIG["telegram_chat_id"], "text": msg}, timeout=10)
        log.info("✅ Telegram sent!")
    except Exception as e:
        log.error(f"❌ Telegram error: {e}")


def notify(msg: str):
    send_whatsapp(msg)
    send_telegram(msg)

# ══════════════════════════════════════════
# 📧 Gmail — get activation link
# ══════════════════════════════════════════

def get_activation_link(timeout=120) -> str:
    log.info("📧 Waiting for TLS activation email...")
    start = time.time()

    while time.time() - start < timeout:
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(CONFIG["gmail"], CONFIG["gmail_pass"])
            mail.select("inbox")

            _, msgs = mail.search(None, 'FROM "noreply@tlscontact.com" UNSEEN')
            ids = msgs[0].split()

            if ids:
                _, data = mail.fetch(ids[-1], "(RFC822)")
                msg_body = email.message_from_bytes(data[0][1])

                body = ""
                if msg_body.is_multipart():
                    for part in msg_body.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg_body.get_payload(decode=True).decode(errors="ignore")

                links = re.findall(r'https?://[^\s"\'<>]+confirm[^\s"\'<>]+', body)
                if links:
                    log.info("✅ Activation link received!")
                    mail.logout()
                    return links[0]

            mail.logout()
        except Exception as e:
            log.error(f"Gmail error: {e}")

        log.info("⏳ Email not received yet — retrying in 10s")
        time.sleep(10)

    raise Exception("❌ Activation email not received within timeout")

# ══════════════════════════════════════════
# 🔐 Register TLS account
# ══════════════════════════════════════════

def register_tls(page) -> bool:
    try:
        log.info("📝 Registering new TLS account...")
        page.goto(TLS_REGISTER, timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        for sel in ['input[name="firstName"]', 'input[placeholder*="Prénom"]', '#firstName']:
            try: page.fill(sel, CONFIG["first_name"]); break
            except: pass

        for sel in ['input[name="lastName"]', 'input[placeholder*="Nom"]', '#lastName']:
            try: page.fill(sel, CONFIG["last_name"]); break
            except: pass

        for sel in ['input[type="email"]', 'input[name="email"]']:
            try: page.fill(sel, CONFIG["gmail"]); break
            except: pass

        pwd_fields = page.query_selector_all('input[type="password"]')
        for f in pwd_fields:
            f.fill(CONFIG["tls_password"])

        time.sleep(1)

        for btn in ["text=S'inscrire", "text=Créer", "text=Register", 'button[type="submit"]']:
            try: page.click(btn, timeout=3000); break
            except: pass

        page.wait_for_load_state("networkidle")
        log.info("✅ Registration submitted — waiting for activation email")

        link = get_activation_link(timeout=120)
        page.goto(link, timeout=30000)
        page.wait_for_load_state("networkidle")
        log.info("✅ Account activated!")
        return True

    except Exception as e:
        log.error(f"❌ Registration failed: {e}")
        return False

# ══════════════════════════════════════════
# 🔑 Login
# ══════════════════════════════════════════

def login_tls(page) -> bool:
    try:
        log.info("🔐 Logging in...")
        page.goto(TLS_LOGIN, timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        page.fill('input[type="email"]', CONFIG["gmail"])
        time.sleep(0.5)
        page.fill('input[type="password"]', CONFIG["tls_password"])
        time.sleep(0.5)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")

        url = page.url.lower()
        if any(s in url for s in ["dashboard", "appointment", "accueil", "home"]):
            log.info("✅ Login successful!")
        else:
            log.info("✅ Logged in!")
        return True

    except Exception as e:
        log.error(f"❌ Login failed: {e}")
        return False

# ══════════════════════════════════════════
# 🔍 Check appointment slots
# ══════════════════════════════════════════

def check_slots(page) -> list:
    try:
        page.goto(TLS_APPT, timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        for sel in [".available", ".day-available", "[data-available='true']", ".calendar-day:not(.disabled)"]:
            days = page.query_selector_all(sel)
            if days:
                return [d.inner_text().strip() for d in days if d.inner_text().strip()]

        content = page.content().lower()
        no_slot = ["aucun créneau", "no appointment", "pas de rendez", "aucune disponibilité"]
        if not any(p in content for p in no_slot):
            return ["Potential slot — check browser manually"]

        return []

    except Exception as e:
        log.error(f"❌ Slot check error: {e}")
        return []

# ══════════════════════════════════════════
# 📅 Book appointment
# ══════════════════════════════════════════

def book_slot(page, date: str) -> bool:
    try:
        log.info(f"📅 Booking: {date}")

        for sel in [".available", ".day-available", "[data-available='true']"]:
            days = page.query_selector_all(sel)
            if days: days[0].click(); break

        time.sleep(2)

        slots = page.query_selector_all(".time-slot, .slot, .heure, .créneau")
        if slots: slots[0].click(); time.sleep(1)

        for btn in ["text=Confirmer", "text=Valider", "text=Réserver", 'button[type="submit"]']:
            try: page.click(btn, timeout=2000); break
            except: pass

        page.wait_for_load_state("networkidle")
        shot = f"booked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=shot)
        log.info(f"📸 Screenshot saved: {shot}")
        return True

    except Exception as e:
        log.error(f"❌ Booking failed: {e}")
        return False

# ══════════════════════════════════════════
# 🚀 Main bot
# ══════════════════════════════════════════

def run():
    log.info("=" * 55)
    log.info(f"🤖 Visa Bot — {CONFIG['city'].upper()} / {CONFIG['country'].upper()}")
    log.info("=" * 55)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="fr-FR",
            timezone_id="Africa/Casablanca",
        )
        page = ctx.new_page()

        # Step 1: Register
        log.info("━" * 40)
        log.info("📝 Step 1 — Register TLS account")
        registered = register_tls(page)
        if not registered:
            log.error("❌ Registration failed — check your .env")
            browser.close()
            return

        # Step 2: Login
        log.info("━" * 40)
        log.info("🔐 Step 2 — Login")
        logged = login_tls(page)
        if not logged:
            log.error("❌ Login failed — check your .env")
            browser.close()
            return

        notify(
            f"🤖 Visa Bot started!\n"
            f"🏙️ {CONFIG['city']} | 🌍 {CONFIG['country'].upper()}\n"
            f"⏱️ Checking every {CONFIG['interval']}s\n"
            f"✅ Account ready"
        )

        # Step 3: Monitor slots
        log.info("━" * 40)
        log.info("🔍 Step 3 — Monitoring slots 24/7")

        checks = 0
        booked = False

        import random
        while not booked:
            checks += 1
            now = datetime.now().strftime("%H:%M:%S")

            slots = check_slots(page)
            status = f"✅ {len(slots)} slot(s) found!" if slots else "❌ No slots"
            log.info(f"[{checks}] {now} — {status}")

            if slots:
                msg = (
                    f"🚨 Slot available!\n"
                    f"📅 {', '.join(slots[:3])}\n"
                    f"🏙️ {CONFIG['city']} | {CONFIG['country'].upper()}\n"
                    f"⏰ {now}\n"
                    f"⏳ Booking now..."
                )
                notify(msg)

                success = book_slot(page, slots[0])
                if success:
                    notify(
                        f"✅ Booking confirmed! 🎉\n"
                        f"📅 {slots[0]}\n"
                        f"🏙️ {CONFIG['city']} | {CONFIG['country'].upper()}\n"
                        f"✉️ Check your email for confirmation"
                    )
                    log.info("🏁 Booking done — bot stopped")
                    booked = True
                else:
                    log.warning("⚠️ Booking failed — retrying")

            if not booked:
                wait = CONFIG["interval"] + random.randint(0, 10)
                log.info(f"⏳ Waiting {wait}s...")
                time.sleep(wait)

        browser.close()


if __name__ == "__main__":
    run()
