import json, os, time, datetime, threading
from modules import mail_sender

SCHEDULE_FILE = "scheduled_emails.json"
CHECK_INTERVAL = 30  # saniyede bir kontrol et

def load_scheduled_emails():
    """Kaydedilmiş e-postaları oku"""
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_scheduled_emails(data):
    """E-postaları dosyaya yaz"""
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_scheduled_email(to, subject, body, send_time):
    """Yeni e-posta planı ekle"""
    data = load_scheduled_emails()

    # 🧠 datetime objesini string'e çevir
    if isinstance(send_time, datetime.datetime):
        send_time = send_time.strftime("%Y-%m-%d %H:%M")

    data.append({
        "to": to,
        "subject": subject,
        "body": body,
        "time": send_time,
        "sent": False
    })

    save_scheduled_emails(data)
    print(f"📅 Yeni planlanan e-posta eklendi → {to} ({send_time})")

def check_and_send_scheduled_emails():
    """Zamanı gelen e-postaları gönder"""
    while True:
        now = datetime.datetime.now()
        emails = load_scheduled_emails()
        updated = []

        for e in emails:
            try:
                send_time = datetime.datetime.strptime(e["time"], "%Y-%m-%d %H:%M")
                if not e.get("sent", False) and now >= send_time:
                    print(f"📤 E-posta gönderiliyor → {e['to']} ({e['subject']})")
                    mail_sender.send_email(e["to"], e["subject"], e["body"])
                    e["sent"] = True
                updated.append(e)
            except Exception as err:
                print("⚠️ E-posta gönderiminde hata:", err)
                updated.append(e)

        save_scheduled_emails(updated)
        time.sleep(CHECK_INTERVAL)

def start_scheduler():
    """Arka plan kontrolünü başlat"""
    thread = threading.Thread(target=check_and_send_scheduled_emails, daemon=True)
    thread.start()
    print("🕓 E-posta zamanlayıcı başlatıldı...")
