import streamlit as st
import json
import os
import datetime
import matplotlib.pyplot as plt

STATS_FILE = "usage_stats.json"

def render():
    st.header("📊 Kullanım İstatistikleri ve Analizler")
    st.markdown("Bu bölümde dil, ton ve tarih bazlı e-posta üretim istatistiklerini görebilirsin.")

    if not os.path.exists(STATS_FILE):
        st.info("Henüz hiç istatistik kaydı bulunmuyor. E-posta oluşturduktan sonra buraya tekrar gel!")
        return

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)

    if not stats:
        st.warning("Henüz veri kaydedilmemiş.")
        return

    # Genel sayılar
    st.subheader("📈 Genel Veriler")
    total_emails = len(stats)
    st.metric("Toplam Üretilen E-Posta", total_emails)

    langs = {}
    tones = {}
    dates = {}

    for item in stats:
        lang = item.get("lang", "Bilinmiyor")
        tone = item.get("tone", "Belirtilmemiş")
        date = item.get("date", "Yok")

        langs[lang] = langs.get(lang, 0) + 1
        tones[tone] = tones.get(tone, 0) + 1
        dates[date] = dates.get(date, 0) + 1

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌐 Dil Dağılımı")
        show_bar_chart(langs, "Dil", "E-posta Sayısı")
    with col2:
        st.subheader("🎭 Ton Dağılımı")
        show_bar_chart(tones, "Ton", "E-posta Sayısı")

    st.subheader("📅 Günlük Aktivite")
    show_line_chart(dates)

    if st.button("🗑️ Tüm İstatistikleri Sıfırla"):
        os.remove(STATS_FILE)
        st.success("Tüm istatistikler silindi.")


def save_stat(lang, tone):
    """Yeni bir e-posta üretildiğinde çağrılır"""
    data = {
        "lang": lang,
        "tone": tone,
        "date": datetime.date.today().isoformat()
    }

    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)
    else:
        stats = []

    stats.append(data)
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def show_bar_chart(data_dict, xlabel, ylabel):
    """Bar grafiği çizer"""
    fig, ax = plt.subplots()
    ax.bar(data_dict.keys(), data_dict.values())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)


def show_line_chart(data_dict):
    """Zaman bazlı çizgi grafiği çizer"""
    dates = sorted(data_dict.keys())
    values = [data_dict[d] for d in dates]
    fig, ax = plt.subplots()
    ax.plot(dates, values, marker="o")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Üretilen E-posta Sayısı")
    plt.xticks(rotation=45)
    st.pyplot(fig)
