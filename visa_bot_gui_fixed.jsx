import { useState, useEffect, useRef } from "react";

const COUNTRIES = [
  { id: "fr", label: "فرنسا",    flag: "🇫🇷", color: "#3b82f6", url: "https://fr.tlscontact.com/appointment/ma{CITY}2fr",       login: "https://fr.tlscontact.com/login/ma{CITY}2fr" },
  { id: "be", label: "بلجيكا",   flag: "🇧🇪", color: "#f59e0b", url: "https://visas-be.tlscontact.com/appointment/ma{CITY}2be", login: "https://visas-be.tlscontact.com/login/ma{CITY}2be" },
  { id: "de", label: "ألمانيا",  flag: "🇩🇪", color: "#ef4444", url: "https://de.tlscontact.com/appointment/ma{CITY}2de",       login: "https://de.tlscontact.com/login/ma{CITY}2de" },
  { id: "it", label: "إيطاليا",  flag: "🇮🇹", color: "#10b981", url: "https://visas-it.tlscontact.com/appointment/ma{CITY}2it", login: "https://visas-it.tlscontact.com/login/ma{CITY}2it" },
  { id: "nl", label: "هولندا",   flag: "🇳🇱", color: "#f97316", url: "https://visas-nl.tlscontact.com/appointment/ma{CITY}2nl", login: "https://visas-nl.tlscontact.com/login/ma{CITY}2nl" },
  { id: "es", label: "إسبانيا",  flag: "🇪🇸", color: "#a855f7", url: "https://visa.vfsglobal.com/mar/en/esp/",                  login: "https://visa.vfsglobal.com/mar/en/esp/login" },
  { id: "ca", label: "كندا",     flag: "🇨🇦", color: "#ec4899", url: "https://visa.vfsglobal.com/mar/en/can/",                  login: "https://visa.vfsglobal.com/mar/en/can/login" },
  { id: "cz", label: "التشيك",   flag: "🇨🇿", color: "#06b6d4", url: "https://visas-cz.tlscontact.com/appointment/ma{CITY}2cz", login: "https://visas-cz.tlscontact.com/login/ma{CITY}2cz" },
];

const CITIES = [
  { id: "RAK", label: "مراكش",          flag: "🏙️" },
  { id: "CAS", label: "الدار البيضاء",  flag: "🌆" },
  { id: "RBA", label: "الرباط",          flag: "🏛️" },
  { id: "TNG", label: "طنجة",            flag: "⚓" },
  { id: "FEZ", label: "فاس",             flag: "🕌" },
  { id: "AGA", label: "أكادير",          flag: "🌊" },
];

const OS_LIST = [
  { id: "windows", label: "Windows", icon: "🪟", cmd: "python visa_bot.py" },
  { id: "linux",   label: "Linux",   icon: "🐧", cmd: "python3 visa_bot.py" },
  { id: "mac",     label: "Mac",     icon: "🍎", cmd: "python3 visa_bot.py" },
];

// ─── Field ────────────────────────────────────────────────
function Field({ label, icon, type = "text", value, onChange, placeholder, hint }) {
  const [show, setShow] = useState(false);
  return (
    <div style={{ marginBottom: 14 }}>
      <label style={{ display: "block", fontSize: 11, color: "#94a3b8", marginBottom: 5, letterSpacing: 1, textTransform: "uppercase" }}>{label}</label>
      <div style={{ position: "relative" }}>
        <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", fontSize: 15 }}>{icon}</span>
        <input
          type={type === "password" ? (show ? "text" : "password") : type}
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder={placeholder}
          style={{ width: "100%", boxSizing: "border-box", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 9, padding: "11px 38px 11px 40px", color: "#f1f5f9", fontSize: 13, outline: "none" }}
          onFocus={e => e.target.style.borderColor = "#f59e0b"}
          onBlur={e => e.target.style.borderColor = "rgba(255,255,255,0.1)"}
        />
        {type === "password" && (
          <button onClick={() => setShow(!show)} style={{ position: "absolute", right: 10, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", fontSize: 14, color: "#64748b" }}>
            {show ? "🙈" : "👁️"}
          </button>
        )}
      </div>
      {hint && <p style={{ color: "#475569", fontSize: 10, margin: "4px 0 0" }}>{hint}</p>}
    </div>
  );
}

// ─── StepBar ──────────────────────────────────────────────
function StepBar({ current }) {
  const steps = [
    { id: 1, icon: "👤", label: "معلوماتك" },
    { id: 2, icon: "🌍", label: "الدولة" },
    { id: 3, icon: "📱", label: "التنبيهات" },
    { id: 4, icon: "🚀", label: "التشغيل" },
  ];
  return (
    <div style={{ display: "flex", justifyContent: "center", gap: 0, marginBottom: 28 }}>
      {steps.map((s, i) => (
        <div key={s.id} style={{ display: "flex", alignItems: "center" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
            <div style={{
              width: 36, height: 36, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
              background: current > s.id ? "#f59e0b" : current === s.id ? "rgba(245,158,11,0.2)" : "rgba(255,255,255,0.05)",
              border: current === s.id ? "2px solid #f59e0b" : "2px solid transparent",
              color: current > s.id ? "#000" : current === s.id ? "#f59e0b" : "#475569"
            }}>
              {current > s.id ? "✓" : s.icon}
            </div>
            <span style={{ fontSize: 10, color: current === s.id ? "#f59e0b" : "#475569", whiteSpace: "nowrap" }}>{s.label}</span>
          </div>
          {i < steps.length - 1 && (
            <div style={{ width: 40, height: 2, background: current > s.id ? "#f59e0b" : "rgba(255,255,255,0.07)", margin: "0 4px", marginBottom: 20 }} />
          )}
        </div>
      ))}
    </div>
  );
}

// ─── NavBtns ──────────────────────────────────────────────
function NavBtns({ onBack, onNext, nextLabel = "التالي ←", nextDisabled = false, nextColor = "#f59e0b" }) {
  return (
    <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
      {onBack && (
        <button onClick={onBack} style={{ flex: 1, padding: "12px", borderRadius: 10, cursor: "pointer", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#64748b", fontSize: 13 }}>
          ← رجوع
        </button>
      )}
      <button onClick={onNext} disabled={nextDisabled} style={{
        flex: 2, padding: "12px", borderRadius: 10, cursor: nextDisabled ? "not-allowed" : "pointer",
        background: nextDisabled ? "rgba(255,255,255,0.05)" : `linear-gradient(135deg, ${nextColor}, ${nextColor}cc)`,
        border: "none", color: nextDisabled ? "#475569" : nextColor === "#10b981" ? "#fff" : "#000",
        fontWeight: 700, fontSize: 14
      }}>
        {nextLabel}
      </button>
    </div>
  );
}

// ─── App ──────────────────────────────────────────────────
export default function App() {
  const [step, setStep]         = useState(1);
  const [os, setOs]             = useState("windows");
  const [copied, setCopied]     = useState(false);
  const [showCode, setShowCode] = useState(false);

  const [firstName,     setFirstName]     = useState("");
  const [lastName,      setLastName]      = useState("");
  const [gmail,         setGmail]         = useState("");
  const [gmailPass,     setGmailPass]     = useState("");
  const [tlsPass,       setTlsPass]       = useState("");
  const [country,       setCountry]       = useState("fr");
  const [city,          setCity]          = useState("RAK");
  const [checkInterval, setCheckInterval] = useState(10);
  const [autoBook,      setAutoBook]      = useState(true);
  const [twilioSid,     setTwilioSid]     = useState("");
  const [twilioToken,   setTwilioToken]   = useState("");
  const [waPhone,       setWaPhone]       = useState("");
  const [tgToken,       setTgToken]       = useState("");
  const [tgChatId,      setTgChatId]      = useState("");

  const selCountry = COUNTRIES.find(c => c.id === country);
  const selCity    = CITIES.find(c => c.id === city);
  const osObj      = OS_LIST.find(o => o.id === os);

  // ─── توليد الكود ──────────────────────────────────────
  const generateCode = () => {
    const urlFinal   = selCountry?.url.replace("{CITY}", city) ?? "";
    const loginFinal = selCountry?.login.replace("{CITY}", city) ?? "";
    const regFinal   = loginFinal.replace("/login/", "/register/");

    return `"""
🤖 visa_bot.py — ${selCountry?.flag} ${selCountry?.label} | ${selCity?.label}
تم توليده تلقائياً من بوت التأشيرة الذكي
"""

import subprocess, sys, importlib.util

# ══════════════════════
# 📦 تثبيت ذكي — مرة واحدة
# ══════════════════════
def install():
    libs = ["playwright", "twilio", "requests"]
    needs = [l for l in libs if importlib.util.find_spec(l) is None]
    if needs:
        print(f"⏳ تثبيت: {', '.join(needs)}...")
        for lib in needs:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib,
                "--quiet", "--break-system-packages"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ كلشي جاهز!\\n")
    else:
        print("✅ المكتبات مثبتة\\n")

install()

from playwright.sync_api import sync_playwright
import imaplib, email, re, time, requests, random
from datetime import datetime
from twilio.rest import Client

CONFIG = {
    "first_name":   "${firstName}",
    "last_name":    "${lastName}",
    "gmail":        "${gmail}",
    "gmail_pass":   "${gmailPass}",
    "tls_password": "${tlsPass}",
    "register_url": "${regFinal}",
    "login_url":    "${loginFinal}",
    "appt_url":     "${urlFinal}",
    "interval":     ${checkInterval},
    "auto_book":    ${autoBook ? "True" : "False"},
    "twilio_sid":   "${twilioSid}",
    "twilio_token": "${twilioToken}",
    "from_wa":      "whatsapp:+14155238886",
    "to_wa":        "whatsapp:${waPhone}",
    "tg_token":     "${tgToken}",
    "tg_chat_id":   "${tgChatId}",
}

def notify(msg):
    try:
        Client(CONFIG["twilio_sid"], CONFIG["twilio_token"]).messages.create(
            from_=CONFIG["from_wa"], to=CONFIG["to_wa"], body=msg)
        print("✅ WhatsApp أُرسل")
    except Exception as e:
        print(f"⚠️ WhatsApp: {e}")
    try:
        requests.post(f"https://api.telegram.org/bot{CONFIG['tg_token']}/sendMessage",
            json={"chat_id": CONFIG["tg_chat_id"], "text": msg}, timeout=10)
        print("✅ Telegram أُرسل")
    except Exception as e:
        print(f"⚠️ Telegram: {e}")

def get_activation_link(timeout=120):
    print("📧 ننتظر إيميل التفعيل...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            m = imaplib.IMAP4_SSL("imap.gmail.com")
            m.login(CONFIG["gmail"], CONFIG["gmail_pass"])
            m.select("inbox")
            for sender in ['FROM "noreply@tlscontact.com"', 'SUBJECT "confirm"', 'SUBJECT "activation"']:
                _, ids = m.search(None, f"{sender} UNSEEN")
                if ids[0].split():
                    _, data = m.fetch(ids[0].split()[-1], "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])
                    body = ""
                    for part in (msg.walk() if msg.is_multipart() else [msg]):
                        if part.get_content_type() in ("text/html", "text/plain"):
                            body += part.get_payload(decode=True).decode(errors="ignore")
                    for pat in [r'https?://[^\\s"\'<>]+confirm[^\\s"\'<>]+',
                                r'https?://[^\\s"\'<>]+activation[^\\s"\'<>]+']:
                        links = re.findall(pat, body)
                        if links:
                            m.logout()
                            return links[0]
            m.logout()
        except Exception as e:
            print(f"⚠️ Gmail: {e}")
        print("⏳ ما وصلش — نعاود بعد 10s")
        time.sleep(10)
    raise Exception("❌ ما وصلش إيميل التفعيل")

def register_tls(page):
    print("📝 كنسجلوا في TLS...")
    notify("⏳ كنسجل حسابك في TLS... استنى")
    page.goto(CONFIG["register_url"], timeout=30000)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    for sel in ['input[name="firstName"]', '#firstName', '[placeholder*="Prénom"]']:
        try: page.fill(sel, CONFIG["first_name"]); break
        except: pass
    for sel in ['input[name="lastName"]', '#lastName', '[placeholder*="Nom"]']:
        try: page.fill(sel, CONFIG["last_name"]); break
        except: pass
    for sel in ['input[type="email"]', 'input[name="email"]']:
        try: page.fill(sel, CONFIG["gmail"]); break
        except: pass
    for f in page.query_selector_all('input[type="password"]'):
        f.fill(CONFIG["tls_password"])
    time.sleep(1)
    for btn in ["text=S'inscrire", "text=Créer", "text=Register", 'button[type="submit"]']:
        try: page.click(btn, timeout=3000); break
        except: pass
    page.wait_for_load_state("networkidle")
    link = get_activation_link()
    page.goto(link, timeout=30000)
    page.wait_for_load_state("networkidle")
    notify("✅ تم تفعيل حسابك في TLS! 🎉")
    print("✅ الحساب مفعّل!")

def login_tls(page):
    print("🔐 كندخلوا لـ TLS...")
    page.goto(CONFIG["login_url"], timeout=30000)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    for sel in ['input[type="email"]', '#Email']:
        try: page.fill(sel, CONFIG["gmail"]); break
        except: pass
    time.sleep(0.5)
    for sel in ['input[type="password"]', '#Password']:
        try: page.fill(sel, CONFIG["tls_password"]); break
        except: pass
    time.sleep(0.5)
    for btn in ['button[type="submit"]', "text=Login", "text=Se connecter"]:
        try: page.click(btn, timeout=3000); break
        except: pass
    page.wait_for_load_state("networkidle")
    notify("🔐 تم الدخول — البوت بدا يراقب 👀")
    print("✅ تم الدخول!")

def check_slots(page):
    try:
        page.goto(CONFIG["appt_url"], timeout=30000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        for sel in [".available", ".day-available", "[data-available='true']", ".calendar-day:not(.disabled)"]:
            days = page.query_selector_all(sel)
            if days:
                texts = [d.inner_text().strip() for d in days if d.inner_text().strip()]
                if texts: return texts
        content = page.content().lower()
        no_slot = ["aucun créneau", "no appointment", "pas de rendez", "aucune disponibilité"]
        if not any(p in content for p in no_slot):
            return ["موعد محتمل — راجع المتصفح"]
    except Exception as e:
        print(f"⚠️ check_slots: {e}")
    return []

def book_slot(page):
    try:
        for sel in [".available", ".day-available", "[data-available='true']"]:
            days = page.query_selector_all(sel)
            if days: days[0].click(); break
        time.sleep(2)
        slots = page.query_selector_all(".time-slot, .slot, .heure, [class*='time']")
        if slots: slots[0].click(); time.sleep(1)
        for btn in ["text=Confirmer", "text=Valider", "text=Réserver", 'button[type="submit"]']:
            try: page.click(btn, timeout=2000); break
            except: pass
        page.wait_for_load_state("networkidle")
        page.screenshot(path=f"moua3id_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        return True
    except Exception as e:
        print(f"❌ book_slot: {e}")
        return False

def run():
    print("\\n" + "🤖 " * 18)
    print(f"  visa_bot.py — ${selCountry?.flag} ${selCountry?.label} | ${selCity?.label}")
    print("🤖 " * 18 + "\\n")

    notify(f"🤖 البوت بدا!\\n${selCountry?.flag} ${selCountry?.label} — ${selCity?.label}\\n⏱️ كنراقب كل ${checkInterval}s")

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

        register_tls(page)
        login_tls(page)

        checks = 0
        booked = False

        while not booked:
            checks += 1
            now = datetime.now().strftime("%H:%M:%S")
            slots = check_slots(page)

            if slots:
                dates = "، ".join(slots[:3])
                msg = (
                    f"🎉 لقينا موعد!\\n📅 {dates}\\n⏰ {now}\\n"
                    f"{'⏳ كنحجزوا دابا...' if CONFIG['auto_book'] else '👆 سارع وحجز!'}"
                )
                print(msg)
                notify(msg)

                if CONFIG["auto_book"]:
                    ok = book_slot(page)
                    if ok:
                        notify("✅ تم الحجز! 🎊\\n✉️ راجع إيميلك")
                        booked = True
                    else:
                        notify("⚠️ فشل الحجز — سارع يدوياً! 🏃")
                else:
                    booked = True
            else:
                print(f"[{checks}] {now} — ما زال ما لقيناش موعد")
                if checks % 10 == 0:
                    notify(f"🔍 فحص {checks}... ما لقيناش بعد 💪")

            if not booked:
                wait = CONFIG["interval"] + random.randint(0, 10)
                print(f"⏳ كنستناوو {wait}s...")
                time.sleep(wait)

        browser.close()

if __name__ == "__main__":
    run()
`;
  };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #0f172a 100%)", fontFamily: "'Segoe UI', Tahoma, sans-serif", direction: "rtl", padding: "24px 16px" }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 28 }}>
        <div style={{ fontSize: 44, marginBottom: 6 }}>🤖</div>
        <h1 style={{ color: "#f59e0b", margin: 0, fontSize: 26, fontWeight: 800 }}>بوت التأشيرة الذكي</h1>
        <p style={{ color: "#475569", margin: "4px 0 0", fontSize: 13 }}>داخل معلوماتك — البوت يدير كلشي وحده</p>
      </div>

      <div style={{ maxWidth: 600, margin: "0 auto" }}>
        <StepBar current={step} />
        <div style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, padding: 28 }}>

          {/* ── STEP 1 ── */}
          {step === 1 && (
            <div>
              <h2 style={{ color: "#f1f5f9", margin: "0 0 6px", fontSize: 17 }}>👤 معلوماتك الشخصية</h2>
              <p style={{ color: "#475569", fontSize: 12, margin: "0 0 20px" }}>البوت غادي يستعملها باش يسجل في TLS تلقائياً</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <Field label="الاسم الأول"  icon="👤" value={firstName} onChange={setFirstName} placeholder="محمد" />
                <Field label="الاسم الأخير" icon="👤" value={lastName}  onChange={setLastName}  placeholder="الأمين" />
              </div>
              <Field label="Gmail" icon="📧" value={gmail} onChange={setGmail} placeholder="email@gmail.com" hint="✅ IMAP مفعّل + App Password جاهز" />
              <Field label="App Password ديال Gmail" icon="🔑" type="password" value={gmailPass} onChange={setGmailPass} placeholder="xxxx xxxx xxxx xxxx" />
              <Field label="كلمة مرور لـ TLS (اخترها أنت)" icon="🔒" type="password" value={tlsPass} onChange={setTlsPass} placeholder="MotDePasse123!" hint="البوت غادي يسجل بها في TLS" />
              <NavBtns onNext={() => setStep(2)} nextDisabled={!firstName || !gmail || !gmailPass || !tlsPass} />
            </div>
          )}

          {/* ── STEP 2 ── */}
          {step === 2 && (
            <div>
              <h2 style={{ color: "#f1f5f9", margin: "0 0 18px", fontSize: 17 }}>🌍 الدولة والمدينة</h2>
              <p style={{ color: "#94a3b8", fontSize: 11, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 1 }}>الدولة</p>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8, marginBottom: 20 }}>
                {COUNTRIES.map(c => (
                  <button key={c.id} onClick={() => setCountry(c.id)} style={{ padding: "10px 4px", borderRadius: 10, cursor: "pointer", textAlign: "center", background: country === c.id ? `${c.color}22` : "rgba(255,255,255,0.04)", border: country === c.id ? `1.5px solid ${c.color}` : "1.5px solid rgba(255,255,255,0.07)", color: country === c.id ? c.color : "#64748b" }}>
                    <div style={{ fontSize: 20 }}>{c.flag}</div>
                    <div style={{ fontSize: 11, marginTop: 2 }}>{c.label}</div>
                  </button>
                ))}
              </div>
              <p style={{ color: "#94a3b8", fontSize: 11, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 1 }}>المدينة</p>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8, marginBottom: 20 }}>
                {CITIES.map(c => (
                  <button key={c.id} onClick={() => setCity(c.id)} style={{ padding: "10px 4px", borderRadius: 10, cursor: "pointer", textAlign: "center", background: city === c.id ? "rgba(245,158,11,0.15)" : "rgba(255,255,255,0.04)", border: city === c.id ? "1.5px solid #f59e0b" : "1.5px solid rgba(255,255,255,0.07)", color: city === c.id ? "#f59e0b" : "#64748b" }}>
                    <div style={{ fontSize: 18 }}>{c.flag}</div>
                    <div style={{ fontSize: 11, marginTop: 2 }}>{c.label}</div>
                  </button>
                ))}
              </div>
              <div style={{ display: "flex", gap: 20, alignItems: "flex-start" }}>
                <div>
                  <p style={{ color: "#94a3b8", fontSize: 11, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 1 }}>الفحص كل</p>
                  <div style={{ display: "flex", gap: 6 }}>
                    {[10, 30, 60].map(s => (
                      <button key={s} onClick={() => setCheckInterval(s)} style={{ padding: "7px 14px", borderRadius: 8, cursor: "pointer", background: checkInterval === s ? "rgba(245,158,11,0.15)" : "rgba(255,255,255,0.04)", border: checkInterval === s ? "1.5px solid #f59e0b" : "1.5px solid rgba(255,255,255,0.07)", color: checkInterval === s ? "#f59e0b" : "#64748b", fontSize: 12 }}>{s}s</button>
                    ))}
                  </div>
                </div>
                <div>
                  <p style={{ color: "#94a3b8", fontSize: 11, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 1 }}>الحجز</p>
                  <div onClick={() => setAutoBook(!autoBook)} style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
                    <div style={{ width: 40, height: 22, borderRadius: 11, position: "relative", background: autoBook ? "#f59e0b" : "rgba(255,255,255,0.1)", transition: "background 0.3s" }}>
                      <div style={{ position: "absolute", top: 3, left: autoBook ? 21 : 3, width: 16, height: 16, borderRadius: "50%", background: "#fff", transition: "left 0.3s" }} />
                    </div>
                    <span style={{ color: autoBook ? "#f59e0b" : "#64748b", fontSize: 12 }}>{autoBook ? "تلقائي ✅" : "تنبيه فقط"}</span>
                  </div>
                </div>
              </div>
              <NavBtns onBack={() => setStep(1)} onNext={() => setStep(3)} />
            </div>
          )}

          {/* ── STEP 3 ── */}
          {step === 3 && (
            <div>
              <h2 style={{ color: "#f1f5f9", margin: "0 0 20px", fontSize: 17 }}>📱 التنبيهات</h2>
              <div style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.15)", borderRadius: 10, padding: 12, marginBottom: 16 }}>
                <p style={{ color: "#f59e0b", fontSize: 12, margin: 0, fontWeight: 700 }}>📱 WhatsApp — Twilio</p>
              </div>
              <Field label="Twilio Account SID" icon="🔑" value={twilioSid} onChange={setTwilioSid} placeholder="ACxxxxxxxxxxxxxxxx" />
              <Field label="Twilio Auth Token"  icon="🛡️" type="password" value={twilioToken} onChange={setTwilioToken} placeholder="xxxxxxxxxxxxxxxx" />
              <Field label="رقم WhatsApp ديالك" icon="📲" value={waPhone} onChange={setWaPhone} placeholder="+212XXXXXXXXX" />
              <div style={{ background: "rgba(56,189,248,0.06)", border: "1px solid rgba(56,189,248,0.15)", borderRadius: 10, padding: 12, marginBottom: 16, marginTop: 16 }}>
                <p style={{ color: "#38bdf8", fontSize: 12, margin: 0, fontWeight: 700 }}>💬 Telegram</p>
              </div>
              <Field label="Telegram Bot Token" icon="🤖" type="password" value={tgToken} onChange={setTgToken} placeholder="1234567890:ABCdef..." />
              <Field label="Telegram Chat ID"   icon="💬" value={tgChatId} onChange={setTgChatId} placeholder="123456789" />
              <NavBtns onBack={() => setStep(2)} onNext={() => setStep(4)} nextLabel="التالي ←" nextDisabled={!twilioSid || !waPhone || !tgToken || !tgChatId} />
            </div>
          )}

          {/* ── STEP 4 ── */}
          {step === 4 && (
            <div>
              <h2 style={{ color: "#f1f5f9", margin: "0 0 18px", fontSize: 17 }}>🚀 لوحة التحكم</h2>

              {/* OS selector */}
              <p style={{ color: "#94a3b8", fontSize: 11, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 1 }}>نظام التشغيل</p>
              <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
                {OS_LIST.map(o => (
                  <button key={o.id} onClick={() => setOs(o.id)} style={{ flex: 1, padding: "10px", borderRadius: 10, cursor: "pointer", textAlign: "center", background: os === o.id ? "rgba(245,158,11,0.15)" : "rgba(255,255,255,0.04)", border: os === o.id ? "1.5px solid #f59e0b" : "1.5px solid rgba(255,255,255,0.07)", color: os === o.id ? "#f59e0b" : "#64748b" }}>
                    <div style={{ fontSize: 20 }}>{o.icon}</div>
                    <div style={{ fontSize: 11, marginTop: 2 }}>{o.label}</div>
                  </button>
                ))}
              </div>

              {/* ملخص */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 20 }}>
                {[
                  { icon: "👤", v: `${firstName} ${lastName}` },
                  { icon: selCountry?.flag, v: `${selCountry?.label} — ${selCity?.label}` },
                  { icon: "⏱️", v: `كل ${checkInterval}s` },
                  { icon: "📋", v: autoBook ? "حجز تلقائي" : "تنبيه فقط" },
                ].map((item, i) => (
                  <div key={i} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "8px 12px", fontSize: 12, color: "#94a3b8" }}>
                    {item.icon} {item.v}
                  </div>
                ))}
              </div>

              {/* ── إشعار التشغيل المحلي ── */}
              <div style={{ background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.25)", borderRadius: 12, padding: "14px 16px", marginBottom: 20 }}>
                <p style={{ color: "#f59e0b", fontSize: 13, margin: "0 0 8px", fontWeight: 700 }}>
                  ℹ️ البوت كيشتغل على جهازك مباشرة
                </p>
                <p style={{ color: "#94a3b8", fontSize: 12, margin: 0, lineHeight: 1.7 }}>
                  1. انسخ الكود من الأسفل<br/>
                  2. احفظه في ملف <code style={{ color: "#f59e0b", background: "rgba(0,0,0,0.3)", padding: "1px 5px", borderRadius: 4 }}>visa_bot.py</code><br/>
                  3. شغّله بالأمر:
                </p>
                <div style={{ background: "#0d1117", borderRadius: 8, padding: "8px 12px", marginTop: 8, direction: "ltr" }}>
                  <code style={{ color: "#10b981", fontSize: 13 }}>{osObj?.cmd}</code>
                </div>
              </div>

              {/* زر نسخ الكود */}
              <button
                onClick={() => setShowCode(!showCode)}
                style={{ width: "100%", padding: "11px", borderRadius: 10, cursor: "pointer", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#94a3b8", fontSize: 13, marginBottom: showCode ? 10 : 0 }}
              >
                {showCode ? "▲ إخفاء الكود" : "▼ عرض الكود + نسخه"}
              </button>

              {showCode && (
                <div>
                  <div style={{ background: "#0d1117", borderRadius: 11, padding: 14, maxHeight: 280, overflowY: "auto", border: "1px solid rgba(255,255,255,0.07)", marginBottom: 8 }}>
                    <pre style={{ color: "#e2e8f0", fontSize: 11, margin: 0, whiteSpace: "pre-wrap", lineHeight: 1.6, direction: "ltr", textAlign: "left" }}>
                      {generateCode()}
                    </pre>
                  </div>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(generateCode());
                      setCopied(true);
                      setTimeout(() => setCopied(false), 2500);
                    }}
                    style={{ width: "100%", padding: "12px", borderRadius: 10, cursor: "pointer", background: copied ? "rgba(16,185,129,0.2)" : "rgba(245,158,11,0.15)", border: `1px solid ${copied ? "#10b981" : "#f59e0b"}`, color: copied ? "#10b981" : "#f59e0b", fontWeight: 700, fontSize: 14 }}
                  >
                    {copied ? "✅ تم النسخ! الصقه في visa_bot.py" : "📋 انسخ visa_bot.py"}
                  </button>
                </div>
              )}

              <button
                onClick={() => { setStep(1); setShowCode(false); setCopied(false); }}
                style={{ width: "100%", marginTop: 12, padding: "11px", borderRadius: 10, cursor: "pointer", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", color: "#475569", fontSize: 12 }}
              >
                🔄 ابدأ من جديد
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
