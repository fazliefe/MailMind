import streamlit as st
import tempfile
from gtts import gTTS
import speech_recognition as sr
import os

def render_voice_tools():
    st.header("🎙️ Sesli Giriş / Okuma Aracı")
    st.markdown("Bu araçla mikrofondan konuşarak e-posta oluşturabilir veya e-postayı sesli dinleyebilirsin.")

    tab1, tab2 = st.tabs(["🎤 Sesle Yaz", "🔊 Sesli Oku"])

    # --- Sesle e-posta yazma ---
    with tab1:
        st.subheader("🎧 Mikrofonla Konuş, Yazıya Dönüştür")
        st.caption("Konuşmayı algılamak için 'Kaydı Başlat' tuşuna bas. Mikrofon izni gerektiğinde 'İzin ver' seçeneğini seç.")
        if st.button("🎙️ Kaydı Başlat"):
            recognize_speech()

    # --- Yazıyı sesli okuma ---
    with tab2:
        st.subheader("🗣️ E-postayı Sesli Oku")
        text = st.text_area("📩 E-posta metnini buraya yapıştır:", height=200)
        lang = st.selectbox("🌐 Dil", ["Türkçe", "İngilizce"], key="tts_lang")

        if st.button("🔊 Sesli Oynat"):
            if not text.strip():
                st.warning("Lütfen sesli okunacak metni girin.")
            else:
                play_tts(text, lang)


def recognize_speech():
    """Mikrofondan ses alıp yazıya dönüştürür"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎧 Dinleniyor... Lütfen konuşun (5 saniye boyunca)")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.success("✅ Ses alındı, çözümleme yapılıyor...")
            text = recognizer.recognize_google(audio_data, language="tr-TR")
            st.text_area("📝 Algılanan Metin", text, height=200)
        except sr.WaitTimeoutError:
            st.error("⏰ Süre doldu, konuşma algılanamadı.")
        except sr.UnknownValueError:
            st.error("🤔 Ses anlaşılamadı, lütfen tekrar deneyin.")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")


def play_tts(text, lang):
    """Metni sesli okur"""
    st.info("🔊 Ses dosyası hazırlanıyor...")
    tts = gTTS(text, lang="tr" if lang == "Türkçe" else "en")
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(audio_path.name)
    st.audio(audio_path.name)
    st.success("🎶 Sesli oynatma hazır!")
