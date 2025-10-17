import streamlit as st
import json, os
from datetime import datetime
import modules.scheduler as scheduler
import modules.mail_sender as mail_sender

SCHEDULE_FILE = "scheduled_emails.json"


def render_scheduled_emails():
    st.header("📅 Planlı Gönderimler")

    if not os.path.exists(SCHEDULE_FILE):
        st.info("📭 Henüz planlanmış bir e-posta yok.")
        return

    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        try:
            emails = json.load(f)
        except json.JSONDecodeError:
            st.error("Dosya okunamadı (bozulmuş JSON).")
            return

    if not emails:
        st.info("📭 Henüz planlanmış bir e-posta yok.")
        return

    for idx, email in enumerate(emails):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 4, 2, 2])

        with col1:
            st.markdown(f"**Alıcı:** {email['to']}")

        with col2:
            st.text(f"Konu: {email['subject']}")

        with col3:
            st.text(f"Zaman: {email.get('time', 'Belirtilmemiş')}")


        with col4:
            if email.get("sent"):
                st.success("✅ Gönderildi")
            else:
                st.warning("⏳ Bekliyor")

        with col5:
            if not email.get("sent"):
                if st.button("📤 Hemen Gönder", key=f"send_{idx}"):
                    success = mail_sender.send_email(
                        email["to"], email["subject"], email["body"]
                    )
                    if success:
                        email["sent"] = True
                        st.success(f"✅ {email['to']} adresine e-posta gönderildi!")
                        save_emails(emails)
                        st.rerun()
                if st.button("❌ İptal Et", key=f"cancel_{idx}"):
                    emails.pop(idx)
                    save_emails(emails)
                    st.toast("🗑️ E-posta iptal edildi.")
                    st.rerun()

    save_emails(emails)


def save_emails(emails):
    """Planlanan e-postaları JSON'a kaydeder"""
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(emails, f, ensure_ascii=False, indent=2)
