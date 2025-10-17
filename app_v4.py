# =============================================================
# 💌 E-Posta Asistanı v4
# =============================================================

import sys, os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# --- Modül dizinini tanımla ---
sys.path.append(os.path.join(os.getcwd(), "modules"))

# --- Paketleri içe aktar ---
from modules import (
    ui_components,
    email_gen,
    analysis,
    calendar_utils,
    stats,
    voice_io,
    database,
    scheduler
)
import modules.scheduled_view as scheduled_view

# --- Ortam değişkenleri ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Zamanlayıcıyı başlat ---
scheduler.start_scheduler()

# --- Sayfa ayarları ---
st.set_page_config(
    page_title="💌 E-Posta Asistanı v4",
    page_icon="📨",
    layout="wide"
)

# --- Arayüz başlat ---
ui_components.inject_custom_css()
ui_components.show_sidebar()
ui_components.show_header()

# ui_components.set_theme()  # (gerekirse ileride aktif edilir)

# --- Navigasyon sekmeleri ---
tabs = st.tabs([
    "📨 E-posta Oluştur",
    "💬 Cevapla",
    "🧠 Analiz Et",
    "📅 Takvim",
    "🕓 Planlı Gönderimler",   # 👈 yeni sekme
    "📊 İstatistikler",
    "👤 Profil / Ayarlar",
    "🎙️ Sesli Araçlar"
])


# --- Sekme içerikleri ---
with tabs[0]:
    email_gen.render(client)

with tabs[1]:
    email_gen.reply_mode(client)

with tabs[2]:
    analysis.render(client)

with tabs[3]:
    calendar_utils.render_calendar_tools()

with tabs[4]:
    stats.render()

with tabs[5]:
    database.render_profile()

with tabs[6]:
    voice_io.render_voice_tools()
with tabs[4]:
    scheduled_view.render_scheduled_emails()

with tabs[5]:
    stats.render()
