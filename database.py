import streamlit as st
import json
import os
import datetime

PROFILE_FILE = "user_profile.json"
HISTORY_FILE = "email_history.json"


# =====================================================
# 🧑 Kullanıcı Profili
# =====================================================

def load_profile():
    """Kullanıcı profilini JSON'dan yükler"""
    if not os.path.exists(PROFILE_FILE):
        return {"name": "", "email": "", "preferred_lang": "Türkçe", "preferred_tone": "Kısa"}
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(profile):
    """Kullanıcı profilini kaydeder"""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def render_profile():
    st.header("👤 Kullanıcı Profili ve Ayarlar")
    profile = load_profile()

    st.subheader("🧑 Profil Bilgileri")
    profile["name"] = st.text_input("Ad Soyad", profile.get("name", ""))
    profile["email"] = st.text_input("E-posta Adresi", profile.get("email", ""))
    profile["preferred_lang"] = st.selectbox("🌐 Tercih Edilen Dil", ["Türkçe", "İngilizce"], index=0 if profile.get("preferred_lang") == "Türkçe" else 1)
    profile["preferred_tone"] = st.selectbox("🎭 Tercih Edilen Ton", ["Kısa", "Resmî", "Samimi", "Nazik", "Profesyonel"], index=0)

    if st.button("💾 Profili Kaydet"):
        save_profile(profile)
        st.success("✅ Profil başarıyla kaydedildi!")

    st.markdown("---")
    render_history_section()


# =====================================================
# ✉️ E-posta Geçmişi ve Taslaklar
# =====================================================

def load_history():
    """Geçmiş e-postaları yükler"""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_history(email_text, tone, lang):
    """Yeni e-postayı geçmişe ekler"""
    history = load_history()
    entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tone": tone,
        "lang": lang,
        "content": email_text
    }
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def render_history_section():
    """Geçmiş ve taslak yönetimi"""
    st.subheader("📜 E-posta Geçmişi ve Taslaklar")

    history = load_history()
    if not history:
        st.info("Henüz kaydedilmiş e-posta bulunmuyor.")
        return

    for i, item in enumerate(reversed(history[-10:])):  # son 10 e-posta
        with st.expander(f"📧 {item['date']} - {item['tone']} ({item['lang']})"):
            st.text_area("İçerik", item["content"], height=150)
            if st.button(f"💾 Taslak Olarak Kaydet {i}"):
                save_draft(item["content"])
                st.success("Taslak olarak kaydedildi!")

    if st.button("🗑️ Tüm geçmişi sil"):
        os.remove(HISTORY_FILE)
        st.warning("Tüm geçmiş silindi.")


# =====================================================
# 📝 Taslaklar
# =====================================================

DRAFT_FILE = "draft.txt"

def save_draft(text):
    """Taslak kaydeder"""
    with open(DRAFT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def load_draft():
    """Kaydedilmiş taslağı döndürür"""
    if not os.path.exists(DRAFT_FILE):
        return ""
    with open(DRAFT_FILE, "r", encoding="utf-8") as f:
        return f.read()
