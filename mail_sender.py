import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import streamlit as st

# Ortam değişkenlerini yükle
load_dotenv()

def send_email(to, subject, body, smtp_server="smtp.gmail.com", smtp_port=587):
    """
    E-posta gönderimi yapan yardımcı fonksiyon.
    .env dosyasında SMTP_EMAIL ve SMTP_PASS tanımlı olmalıdır.
    """
    sender = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASS")

    if not sender or not password:
        msg = "⚠️ SMTP bilgileri eksik (.env dosyasını kontrol et)"
        print(msg)
        st.warning(msg)
        return False

    try:
        # E-posta mesajı oluştur
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # SMTP bağlantısı başlat
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(msg)

        print(f"✅ E-posta gönderildi → {to}")
        st.success(f"📤 E-posta gönderildi → {to}")
        return True

    except smtplib.SMTPAuthenticationError:
        msg = "❌ SMTP kimlik doğrulama hatası: kullanıcı adı veya şifre hatalı."
        print(msg)
        st.error(msg)
        return False

    except Exception as e:
        msg = f"❌ Gönderim hatası: {e}"
        print(msg)
        st.error(msg)
        return False
