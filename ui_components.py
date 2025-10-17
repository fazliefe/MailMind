import streamlit as st

# =====================================================
# 🎨 Tema & UI Bileşenleri
# =====================================================

def inject_custom_css():
    """Uygulamanın genel stilini özelleştirir"""
    st.markdown("""
        <style>
        /* Genel gövde rengi */
        body {
            background-color: #f9fafc;
            color: #333333;
        }

        /* Ana başlık */
        .main-title {
            font-size: 40px;
            font-weight: 700;
            background: linear-gradient(90deg, #5c6bc0, #3949ab);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5em;
        }

        /* Alt başlık */
        .subtitle {
            color: #555;
            font-size: 18px;
            margin-bottom: 1.2em;
        }

        /* Kart tasarımı */
        .stCard {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1.2em 1.5em;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5em;
        }

        /* Buton rengi */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #3949ab, #1e88e5);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            background: linear-gradient(90deg, #1e88e5, #42a5f5);
        }

        /* Sekme başlıkları */
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f4f8;
            border-radius: 8px;
            padding: 8px 16px;
            margin: 2px;
        }

        /* Kaydırma çubuğu */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #aab4be;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)


def show_header():
    """Sayfanın üst kısmındaki başlık bölümü"""
    st.markdown("<h1 class='main-title'>📨 Akıllı E-Posta Asistanı v4</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Yapay zekâ destekli e-posta oluşturma, analiz, sesli araçlar ve daha fazlası.</p>", unsafe_allow_html=True)


def show_sidebar():
    """Sol menü (logo + bilgi)"""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/732/732200.png", width=80)
        st.markdown("### 💼 Email Assistant v4")
        st.markdown("**GPT-4 destekli kurumsal e-posta asistanı** 🧠")
        st.markdown("---")
        st.markdown("#### 📘 Özellikler")
        st.markdown("""
        - 📨 E-posta oluşturma  
        - 💬 Cevaplama modu  
        - 🧠 Duygu ve spam analizi  
        - 📅 Takvim daveti üretimi  
        - 🎙️ Sesli komut  
        - 📊 İstatistikler  
        - 👤 Profil yönetimi  
        """)
        st.markdown("---")
        st.markdown("© 2025 | Developed with ❤️ by YOU")
