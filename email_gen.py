import streamlit as st
from fpdf import FPDF
from gtts import gTTS
import tempfile
import json
import os
import datetime
import modules.stats as stats
import modules.scheduler as scheduler
import modules.database as database

# --- Hazır şablonlar ---
TEMPLATE_PATH = os.path.join("assets", "email_template.json")

def load_templates():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# =====================================================
# 📬 E-POSTA OLUŞTURMA MODU
# =====================================================
def render(client):
    st.header("📨 Yeni E-posta Oluştur")

    templates = load_templates()
    template_choice = st.selectbox(
        "📋 Hazır Şablon Seç",
        ["Kendi Konumu Belirteceğim"] + list(templates.keys()),
        key="template_create"
    )

    purpose = st.text_input(
        "🧠 E-posta Amacı",
        "" if template_choice != "Kendi Konumu Belirteceğim" else "Toplantı erteleme",
        key="purpose_create"
    )

    tone = st.selectbox(
        "🎭 Ton",
        ["Kısa", "Resmî", "Samimi", "Nazik", "Profesyonel"],
        key="tone_create"
    )

    lang = st.selectbox(
        "🌐 Dil",
        ["Türkçe", "İngilizce"],
        key="lang_create"
    )

    creativity = st.slider("✨ Yaratıcılık Seviyesi", 0.0, 1.0, 0.7, key="creativity_create")

    improve = st.checkbox("🧠 Daha profesyonel hale getir", key="improve_create")
    tts_enabled = st.checkbox("🎧 Sesli okuma oluştur (TTS)", key="tts_create")
    save_draft = st.checkbox("💾 Taslak olarak kaydet", key="draft_create")

    # 🕓 Planlama seçeneği
    plan_later = st.checkbox("📅 Belirli bir tarihte gönder", key="plan_checkbox")
    send_time = None
    to_email = None
    if plan_later:
        to_email = st.text_input("📧 Alıcı E-posta Adresi", key="to_email")
        date = st.date_input("📆 Gönderim tarihi seç", datetime.date.today(), key="plan_date")
        time_input = st.time_input("⏰ Gönderim saati seç", datetime.time(9, 0), key="plan_time")
        send_time = datetime.datetime.combine(date, time_input)

    if st.button("✉️ E-posta Oluştur", key="create_email"):
        with st.spinner("🧠 E-posta hazırlanıyor..."):
            topic = templates.get(template_choice, purpose)
            prompt = f"""
            Lütfen {lang} dilinde, {tone.lower()} tonunda, '{topic}' konulu kısa bir e-posta yaz.
            Format:
            KONUSATIRI:
            [Konu]
            EPOSTA:
            [Metin]
            """

            try:
                # OpenAI API çağrısı
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=creativity
                )
                result = response.choices[0].message.content.strip()

                # Yanıt ayrıştırma
                if "EPOSTA:" in result:
                    parts = result.split("EPOSTA:")
                    subject = parts[0].replace("KONUSATIRI:", "").strip()
                    email_text = parts[1].strip()
                else:
                    subject = "Konu bulunamadı"
                    email_text = result

                # Gösterim
                st.success("✅ E-posta oluşturuldu!")
                st.markdown(f"**Konu:** {subject}")
                st.text_area("📨 E-posta İçeriği", email_text, height=200, key="email_content")

                # PDF oluşturma
                create_pdf(subject, email_text)

                # Sesli okuma
                if tts_enabled:
                    play_tts(email_text, lang)

                # Profesyonelleştirme
                if improve:
                    improve_email(client, email_text, lang)

                # Taslak kaydetme
                if save_draft:
                    save_draft_to_file(subject, email_text)
                    st.toast("💾 Taslak kaydedildi ✅")

                # Planlı gönderim
                if plan_later and to_email and send_time:
                    scheduler.add_scheduled_email(to_email, subject, email_text, send_time)
                    st.success(f"📅 E-posta {send_time.strftime('%d %B %Y %H:%M')} tarihinde gönderilmek üzere planlandı.")
                elif plan_later:
                    st.warning("⚠️ Planlı gönderim için alıcı adresini girmen gerekiyor!")

                # Geçmiş kaydı
                database.save_to_history(email_text, tone, lang)

            except Exception as e:
                st.error(f"Hata: {e}")

# =====================================================
# 💬 E-POSTA CEVAPLAMA MODU
# =====================================================
def reply_mode(client):
    st.header("💬 E-Posta Cevaplama Modu")
    incoming = st.text_area("📥 Gelen E-Posta Metni", height=200, key="incoming_reply")
    tone = st.selectbox("🎭 Yanıt Tonu", ["Kısa", "Resmî", "Samimi", "Nazik", "Profesyonel"], key="tone_reply")
    lang = st.selectbox("🌐 Yanıt Dili", ["Türkçe", "İngilizce"], key="lang_reply")
    creativity = st.slider("✨ Yaratıcılık", 0.0, 1.0, 0.7, key="creativity_reply")

    if st.button("✉️ Yanıt Oluştur", key="reply_btn"):
        with st.spinner("🧠 Cevap hazırlanıyor..."):
            prompt = f"Bu e-postaya {lang} dilinde, {tone.lower()} tonunda kibar bir yanıt yaz:\n\n{incoming}"
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=creativity
                )
                reply = response.choices[0].message.content.strip()
                st.success("✅ Yanıt oluşturuldu!")
                st.text_area("📨 Önerilen Yanıt", reply, height=200, key="reply_output")
                stats.save_stat(lang, tone)
                database.save_to_history(reply, tone, lang)
            except Exception as e:
                st.error(f"Hata: {e}")

# =====================================================
# 🧰 Yardımcı Fonksiyonlar
# =====================================================
def create_pdf(subject, email_text):
    """Türkçe karakter destekli PDF üretimi"""
    pdf = FPDF()
    pdf.add_page()
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)
    pdf.multi_cell(0, 10, f"Konu: {subject}\n\n{email_text}")

    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(pdf_output.name)
    with open(pdf_output.name, "rb") as f:
        st.download_button("📄 PDF olarak indir", f, file_name="email.pdf")

def play_tts(email_text, lang):
    """E-postayı sesli okutma"""
    st.markdown("🎧 Ses dosyası oluşturuluyor...")
    tts = gTTS(email_text, lang="tr" if lang == "Türkçe" else "en")
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(audio_path.name)
    st.audio(audio_path.name)

def improve_email(client, email_text, lang):
    """E-postayı daha profesyonel hale getir"""
    with st.spinner("🧠 E-posta geliştiriliyor..."):
        prompt = f"Bu e-postayı {lang} dilinde daha profesyonel ve etkileyici hale getir:\n\n{email_text}"
        improved = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        improved_text = improved.choices[0].message.content.strip()
        st.markdown("### 💼 Geliştirilmiş Versiyon")
        st.text_area("Geliştirilmiş E-posta", improved_text, height=200, key="improved_output")

def save_draft_to_file(subject, email_text):
    """Taslakları JSON dosyasına kaydet"""
    draft = {"subject": subject, "content": email_text}
    drafts_path = "drafts.json"
    if os.path.exists(drafts_path):
        with open(drafts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.insert(0, draft)
    with open(drafts_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
