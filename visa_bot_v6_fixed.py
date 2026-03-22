"""
🎬 VISA BOT v6 — BLS Spain — Headful mode (watch the browser)
✅ Registers via "Create an account" on the Login page
✅ Two-step login: Email → Verify → Password → Login
✅ Watch every step directly in the browser
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
import imaplib, email, re, time, requests, logging, os
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

# ══════════════════════════════════════════
# 🔐 Load credentials from .env
# ══════════════════════════════════════════

load_dotenv()

CFG = {
    "first_name":   os.getenv("FIRST_NAME",   "XXX"),
    "last_name":    os.getenv("LAST_NAME",     "XXX"),
    "gmail":        os.getenv("GMAIL",         "XXX@gmail.com"),
    "gmail_pass":   os.getenv("GMAIL_PASS",    "XXX"),
    "tls_password": os.getenv("TLS_PASSWORD",  "XXX"),

    "login_url":    "https://www.blsspainmorocco.net/MAR/account/Login",
    "appt_url":     "https://www.blsspainmorocco.net/MAR/appointment/",

    "interval":      45,
    "auto_book":     True,
    "retry_on_fail": True,
    "headless":      False,
    "step_delay":    4,

    "twilio_sid":   os.getenv("TWILIO_SID",   "XXX"),
    "twilio_token": os.getenv("TWILIO_TOKEN", "XXX"),
    "from_wa":      "whatsapp:+14155238886",
    "to_wa":        f"whatsapp:{os.getenv('WA_PHONE', '+212XXXXXXXXX')}",
    "tg_token":     os.getenv("TG_TOKEN",     "XXX"),
    "tg_chat_id":   os.getenv("TG_CHAT_ID",   "XXX"),
}

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

def step(msg):
    print("\n" + "═" * 55)
    print(f"  {msg}")
    print("═" * 55)
    time.sleep(CFG["step_delay"])

# ══════════════════════════════════════════
# 📱 Notifications
# ══════════════════════════════════════════

def notify(msg):
    try:
        Client(CFG["twilio_sid"], CFG["twilio_token"]).messages.create(
            from_=CFG["from_wa"], to=CFG["to_wa"], body=msg)
        log.info("✅ WhatsApp sent")
    except Exception as e:
        log.warning(f"⚠️ WhatsApp: {e}")
    try:
        requests.post(
            f"https://api.telegram.org/bot{CFG['tg_token']}/sendMessage",
            json={"chat_id": CFG["tg_chat_id"], "text": msg}, timeout=10)
        log.info("✅ Telegram sent")
    except Exception as e:
        log.warning(f"⚠️ Telegram: {e}")

# ══════════════════════════════════════════
# 📧 Gmail — get activation link
# ══════════════════════════════════════════

def get_activation_link(timeout=120):
    log.info("📧 Waiting for activation email...")
    end = time.time() + timeout
    while time.time() < end:
        try:
            m = imaplib.IMAP4_SSL("imap.gmail.com")
            m.login(CFG["gmail"], CFG["gmail_pass"])
            m.select("inbox")
            for sender in [
                'FROM "noreply@blsspainmorocco.net"',
                'FROM "no-reply@blsspainmorocco.net"',
                'FROM "noreply@tlscontact.com"',
                'SUBJECT "activation"',
                'SUBJECT "confirm"',
                'SUBJECT "verify"',
                'SUBJECT "account"',
            ]:
                _, ids = m.search(None, f"{sender} UNSEEN")
                if ids[0].split():
                    _, data = m.fetch(ids[0].split()[-1], "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])
                    body = ""
                    for part in (msg.walk() if msg.is_multipart() else [msg]):
                        if part.get_content_type() in ("text/html", "text/plain"):
                            body += part.get_payload(decode=True).decode(errors="ignore")
                    for pattern in [
                        r'https?://[^\s"\'<>]*confirm[^\s"\'<>]*',
                        r'https?://[^\s"\'<>]*activation[^\s"\'<>]*',
                        r'https?://[^\s"\'<>]*verify[^\s"\'<>]*',
                        r'https?://[^\s"\'<>]*activate[^\s"\'<>]*',
                        r'https?://[^\s"\'<>]*account[^\s"\'<>]*token[^\s"\'<>]*',
                    ]:
                        links = re.findall(pattern, body)
                        if links:
                            m.logout()
                            log.info("✅ Activation link found!")
                            return links[0]
            m.logout()
        except Exception as e:
            log.warning(f"⚠️ Gmail: {e}")
        log.info("⏳ Not received yet — retrying in 10s")
        time.sleep(10)
    raise Exception("❌ Activation email not received within timeout")

# ══════════════════════════════════════════
# 🔍 Check if account exists
# ══════════════════════════════════════════

def wait_if_blocked(page, context=""):
    content = page.content().lower()
    if "too many requests" in content or "429" in page.url:
        log.warning(f"🚫 Too Many Requests {context} — waiting 10 minutes...")
        notify("🚫 BLS blocked IP temporarily\nWaiting 10 minutes then retrying automatically ⏳")
        time.sleep(600)
        return True
    return False


def check_account_exists(page) -> str:
    step("🔍 Step 1 — Checking if account exists...")

    page.goto(CFG["login_url"], timeout=30000)
    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    if wait_if_blocked(page, "check_account"):
        page.goto(CFG["login_url"], timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(CFG["step_delay"])

    for sel in ['input[type="email"]', '#Email', 'input[name="Email"]']:
        try: page.fill(sel, CFG["gmail"]); break
        except: pass

    time.sleep(1)

    for btn in ["text=Verify", "text=Next", 'button[type="submit"]', 'input[type="submit"]']:
        try: page.click(btn, timeout=3000); break
        except: pass

    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    content = page.content().lower()

    not_found_signs = [
        "not registered", "no account", "email not found",
        "user not found", "invalid email", "does not exist",
        "n'existe pas", "introuvable"
    ]
    if any(s in content for s in not_found_signs):
        log.info("📝 Account not found")
        return "not_found"

    for sel in ['input[type="password"]', '#Password', 'input[name="Password"]']:
        try:
            if page.is_visible(sel, timeout=4000):
                log.info("✅ Account exists — proceeding with password")

                page.fill(sel, CFG["tls_password"])
                time.sleep(1)

                for btn in ["text=Login", "text=Sign in", "text=Se connecter",
                            'button[type="submit"]', 'input[type="submit"]']:
                    try: page.click(btn, timeout=3000); break
                    except: pass

                page.wait_for_load_state("networkidle")
                time.sleep(CFG["step_delay"])

                url2     = page.url.lower()
                content2 = page.content().lower()

                success = ["dashboard", "appointment", "book", "home",
                           "manage", "newappointment", "index"]
                if any(s in url2 or s in content2 for s in success):
                    log.info("✅ Logged in directly!")
                    return "logged_in"

                wrong = ["invalid", "incorrect", "wrong", "err=", "error"]
                if any(s in content2 or s in url2 for s in wrong):
                    log.warning("⚠️ Wrong password!")
                    notify("⚠️ Wrong password!\nCheck TLS_PASSWORD in your .env")
                    return "wrong_pass"

                return "logged_in"
        except: pass

    log.info("📝 Unknown state — will register")
    return "not_found"

# ══════════════════════════════════════════
# 📝 Register new account
# ══════════════════════════════════════════

def register(page):
    step("📝 Step 2 — Registering new BLS account...")
    notify("📝 Registering your BLS account... Please wait 🙏")

    page.goto(CFG["login_url"], timeout=30000)
    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    log.info("🔗 Looking for Create an account button...")
    clicked = False
    for btn in [
        "text=Create an account",
        "text=Create Account",
        "text=Register",
        "text=Sign up",
        "text=S'inscrire",
        "text=Créer un compte",
        "a[href*='Register']",
        "a[href*='register']",
        "a[href*='signup']",
    ]:
        try:
            page.click(btn, timeout=3000)
            log.info(f"✅ Clicked: {btn}")
            clicked = True
            break
        except: pass

    if not clicked:
        log.warning("⚠️ Register button not found — taking screenshot...")
        page.screenshot(path="debug_register.png")

    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    log.info("📝 Filling registration form...")

    for sel in ['input[name="FirstName"]', '#FirstName', '[placeholder*="First"]',
                'input[name="firstName"]', '[placeholder*="Prénom"]']:
        try: page.fill(sel, CFG["first_name"]); log.info(f"✅ FirstName -> {sel}"); break
        except: pass

    for sel in ['input[name="LastName"]', '#LastName', '[placeholder*="Last"]',
                'input[name="lastName"]', '[placeholder*="Nom"]']:
        try: page.fill(sel, CFG["last_name"]); log.info(f"✅ LastName -> {sel}"); break
        except: pass

    for sel in ['input[type="email"]', '#Email', 'input[name="Email"]', '[placeholder*="Email"]']:
        try: page.fill(sel, CFG["gmail"]); log.info(f"✅ Email -> {sel}"); break
        except: pass

    for sel in ['input[name="PhoneNumber"]', '#PhoneNumber', '[placeholder*="Phone"]',
                '[placeholder*="Mobile"]']:
        try: page.fill(sel, CFG["to_wa"].replace("whatsapp:", "")); log.info(f"✅ Phone -> {sel}"); break
        except: pass

    pwd_fields = page.query_selector_all('input[type="password"]')
    for f in pwd_fields:
        try: f.fill(CFG["tls_password"])
        except: pass
    log.info(f"✅ Filled {len(pwd_fields)} password field(s)")

    time.sleep(1)
    page.screenshot(path="debug_before_submit.png")

    for btn in ["text=Register", "text=Create Account", "text=Create an account",
                "text=Submit", "text=Sign up", "text=S'inscrire",
                'button[type="submit"]', 'input[type="submit"]']:
        try: page.click(btn, timeout=3000); log.info(f"✅ Submitted: {btn}"); break
        except: pass

    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])
    page.screenshot(path="debug_after_submit.png")

    content = page.content().lower()

    if any(s in content for s in ["already exists", "already registered",
                                   "email exist", "déjà utilisé", "already taken"]):
        log.warning("⚠️ Email already registered!")
        notify("⚠️ Email already registered — attempting direct login")
        return

    step("📧 Step 3 — Waiting for activation email...")
    try:
        link = get_activation_link(timeout=120)
        log.info("🔗 Opening activation link...")
        page.goto(link, timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(CFG["step_delay"])
        page.screenshot(path="debug_activated.png")
        notify("✅ Account registered and activated! 🎉")
        log.info("✅ Account activated!")
    except Exception as e:
        log.error(f"❌ {e}")
        notify("⚠️ Please activate your account manually from email, then restart the bot")

# ══════════════════════════════════════════
# 🔑 Two-step login
# ══════════════════════════════════════════

def bls_login(page) -> bool:
    step("🔐 Logging in — two steps...")

    page.goto(CFG["login_url"], timeout=30000)
    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    for sel in ['input[type="email"]', '#Email', 'input[name="Email"]']:
        try: page.fill(sel, CFG["gmail"]); break
        except: pass

    time.sleep(1)

    for btn in ["text=Verify", "text=Next", 'button[type="submit"]', 'input[type="submit"]']:
        try: page.click(btn, timeout=3000); break
        except: pass

    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    pwd_shown = False
    for sel in ['input[type="password"]', '#Password', 'input[name="Password"]']:
        try:
            if page.is_visible(sel, timeout=4000):
                page.fill(sel, CFG["tls_password"])
                pwd_shown = True
                break
        except: pass

    if not pwd_shown:
        log.warning("⚠️ Password field not visible")
        return False

    time.sleep(1)

    for btn in ["text=Login", "text=Sign in", "text=Se connecter",
                'button[type="submit"]', 'input[type="submit"]']:
        try: page.click(btn, timeout=3000); break
        except: pass

    page.wait_for_load_state("networkidle")
    time.sleep(CFG["step_delay"])

    url     = page.url.lower()
    content = page.content().lower()
    success = ["dashboard", "appointment", "book", "home", "manage", "newappointment"]

    if any(s in url or s in content for s in success):
        log.info("✅ Login successful!")
        notify("🔐 Logged in — bot is now monitoring 👀")
        return True

    log.warning("⚠️ Login failed")
    return False

# ══════════════════════════════════════════
# 🔍 Check appointment slots
# ══════════════════════════════════════════

def check_slots(page) -> list:
    try:
        page.goto(CFG["appt_url"], timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        if wait_if_blocked(page, "check_slots"):
            return []

        for sel in [".available", ".day-available", ".slot-available",
                    "[data-available='true']", "[class*='available']"]:
            days = page.query_selector_all(sel)
            if days:
                texts = [d.inner_text().strip() for d in days if d.inner_text().strip()]
                if texts: return texts

        no_slot = ["no appointment", "no slots", "no availability",
                   "aucun créneau", "complet", "fully booked"]
        if not any(p in page.content().lower() for p in no_slot):
            return ["Potential slot — check browser! 👀"]

        return []
    except Exception as e:
        log.warning(f"⚠️ check_slots: {e}")
        return []

# ══════════════════════════════════════════
# 📅 Book appointment
# ══════════════════════════════════════════

def book_slot(page) -> bool:
    step("📅 Booking appointment...")
    try:
        for sel in [".available", ".day-available", "[data-available='true']"]:
            days = page.query_selector_all(sel)
            if days: days[0].click(); break

        time.sleep(2)

        slots = page.query_selector_all(".time-slot,.slot,.heure,[class*='time'],[class*='slot']")
        if slots: slots[0].click(); time.sleep(1)

        for btn in ["text=Confirmer", "text=Valider", "text=Réserver",
                    "text=Confirm", "text=Book", 'button[type="submit"]']:
            try: page.click(btn, timeout=2000); break
            except: pass

        page.wait_for_load_state("networkidle")
        time.sleep(CFG["step_delay"])

        shot = f"booked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=shot)
        log.info(f"📸 Screenshot: {shot}")
        return True
    except Exception as e:
        log.error(f"❌ book_slot: {e}")
        return False

# ══════════════════════════════════════════
# 👁️ Monitor appointments
# ══════════════════════════════════════════

def monitor(page):
    step("👁️ Monitoring slots — checking every " + str(CFG["interval"]) + "s")

    checks = 0
    fail_count = 0

    import random
    while True:
        checks += 1
        now   = datetime.now().strftime("%H:%M:%S")
        slots = check_slots(page)

        if slots:
            dates = ", ".join(slots[:3])
            msg = (
                f"🎉 Slot found!\n"
                f"📅 {dates}\n"
                f"⏰ {now}\n"
                f"{'⏳ Booking now...' if CFG['auto_book'] else '👆 Book manually!'}"
            )
            log.info(msg)
            notify(msg)

            if CFG["auto_book"]:
                ok = book_slot(page)
                if ok:
                    notify("✅ Booking confirmed! 🎊\n✉️ Check your email")
                    break
                else:
                    fail_count += 1
                    if CFG["retry_on_fail"] and fail_count < 3:
                        notify(f"⚠️ Attempt {fail_count}/3 — retrying...")
                        time.sleep(5)
                        continue
                    else:
                        notify("⚠️ Booking failed — book manually! 🏃\n" + CFG["appt_url"])
                        break
            else:
                break
        else:
            log.info(f"[{checks}] {now} — No slots yet")
            if checks % 10 == 0:
                notify(f"🔍 Check #{checks}... Still no slots 💪")

        wait = CFG["interval"] + random.randint(0, 15)
        log.info(f"⏳ Waiting {wait}s...")
        time.sleep(wait)

# ══════════════════════════════════════════
# 🚀 Main bot
# ══════════════════════════════════════════

def run():
    print("\n" + "🤖 " * 18)
    print("  VISA BOT v6 — BLS Spain — Headful mode 🎬")
    print("🤖 " * 18 + "\n")

    notify("🎬 Visa Bot v6 started!\nWatch the browser 👀")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1500,
            args=["--no-sandbox",
                  "--disable-blink-features=AutomationControlled",
                  "--start-maximized"]
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="fr-FR",
            timezone_id="Africa/Casablanca",
        )
        page = ctx.new_page()

        status = check_account_exists(page)

        if status == "logged_in":
            log.info("✅ Account found — starting monitoring")
            monitor(page)

        elif status == "wrong_pass":
            log.error("❌ Check TLS_PASSWORD in your .env")

        else:
            register(page)
            ok = bls_login(page)
            if ok:
                monitor(page)
            else:
                log.error("❌ Login failed — check your .env")
                notify("❌ Login failed — check your .env credentials")
                page.screenshot(path="debug_login_failed.png")

        input("\n⏸️  Press Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    run()
