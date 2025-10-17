import streamlit as st
from ics import Calendar, Event
import tempfile
import datetime
import re

def render_calendar_tools():
    st.header("📅 Takvim Daveti Oluşturucu")
    st.markdown("Toplantı veya etkinlik içeren bir e-posta metninden takvim daveti (.ics) dosyası oluşturabilirsin.")

    email_text = st.text_area("📩 E-posta içeriğini buraya yapıştır:", height=200)
    default_title = "Toplantı / Görüşme"
    event_title = st.text_input("🗓️ Etkinlik Başlığı", default_title)
    event_duration = st.slider("⏰ Süre (dakika)", 15, 180, 60)
    add_to_calendar = st.checkbox("📆 Takvime eklenebilir .ics dosyası oluştur")

    if st.button("✨ Takvim Daveti Oluştur"):
        if not email_text.strip():
            st.warning("Lütfen takvim oluşturmak için bir e-posta metni girin.")
            return

        with st.spinner("📅 Tarih ve saat aranıyor..."):
            start_dt = extract_datetime(email_text)
            if not start_dt:
                st.error("❌ E-postada tarih/saat bulunamadı. Lütfen manuel bir tarih girin:")
                start_dt = manual_date_input()
            else:
                st.success(f"📆 Otomatik tarih bulundu: {start_dt.strftime('%d %B %Y %H:%M')}")

        if add_to_calendar:
            create_ics(event_title, start_dt, event_duration)
            st.success("✅ .ics dosyası hazır! Takvime ekleyebilirsin.")


def extract_datetime(text):
    """Metin içinden tarih/saat bilgisi bulmaya çalışır"""
    # Basit tarih/saat yakalama (örnek: 20 Ekim 2025 15:30 veya 21/10/2025)
    date_patterns = [
        r"(\d{1,2})[\/\.](\d{1,2})[\/\.](\d{4})",        # 21/10/2025 veya 21.10.2025
        r"(\d{1,2})\s*(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s*(\d{4})",
        r"(?:saat|Saat)\s*(\d{1,2})[:\.](\d{2})"         # saat 14:30
    ]
    day = month = year = hour = minute = None

    month_names = {
        "Ocak":1, "Şubat":2, "Mart":3, "Nisan":4, "Mayıs":5, "Haziran":6,
        "Temmuz":7, "Ağustos":8, "Eylül":9, "Ekim":10, "Kasım":11, "Aralık":12
    }

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 3 and match.group(2).isdigit():
                # Biçim: 21/10/2025
                day, month, year = map(int, match.groups())
            elif len(match.groups()) == 3 and not match.group(2).isdigit():
                # Biçim: 21 Ekim 2025
                day = int(match.group(1))
                month = month_names.get(match.group(2), 1)
                year = int(match.group(3))
            elif len(match.groups()) == 2:
                hour, minute = map(int, match.groups())
    if not year:
        return None
    hour = hour or 9
    minute = minute or 0
    return datetime.datetime(year, month, day, hour, minute)


def manual_date_input():
    """Manuel tarih seçimi"""
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📅 Tarih Seç")
    with col2:
        time = st.time_input("⏰ Saat Seç")
    return datetime.datetime.combine(date, time)


def create_ics(title, start_datetime, duration_minutes):
    """ICS dosyası oluşturur"""
    c = Calendar()
    e = Event()
    e.name = title
    e.begin = start_datetime
    e.duration = datetime.timedelta(minutes=duration_minutes)
    e.created = datetime.datetime.now()
    c.events.add(e)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ics")
    with open(temp_file.name, "w", encoding="utf-8") as f:
        f.writelines(c.serialize_iter())

    with open(temp_file.name, "rb") as f:
        st.download_button("📥 Takvim (.ics) Dosyasını İndir", f, file_name="event.ics")
