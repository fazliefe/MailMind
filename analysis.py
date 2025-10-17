import streamlit as st
import matplotlib.pyplot as plt

def render(client):
    st.header("🧠 E-posta Analiz Aracı")
    st.markdown("Bu araç, e-postanın tonunu, profesyonellik düzeyini ve spam olasılığını analiz eder.")

    email_text = st.text_area("📩 Analiz etmek istediğiniz e-posta metnini buraya yapıştırın:", height=200)

    if st.button("🔍 Analiz Et"):
        if not email_text.strip():
            st.warning("Lütfen analiz etmek için bir e-posta metni girin.")
            return

        with st.spinner("🧠 Analiz ediliyor..."):
            try:
                prompt = f"""
                Bu e-postayı analiz et:
                - Genel duygu (pozitif, nötr, negatif)
                - Profesyonellik düzeyi (1-10)
                - Spam olasılığı (%)
                - Kısa geri bildirim ver
                E-Posta:
                {email_text}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4
                )
                analysis_text = response.choices[0].message.content.strip()
                st.success("✅ Analiz tamamlandı!")

                # Sonuçları yazdır
                st.markdown("### 🧾 Analiz Sonucu:")
                st.write(analysis_text)

                # Basit puanlama tahmini (görselleştirme için)
                sentiment_score = 7
                professionalism = 8
                spam_score = 15

                # Basit anahtar kelime aramasıyla tahmini puanlama
                if "negatif" in analysis_text.lower(): sentiment_score = 3
                if "pozitif" in analysis_text.lower(): sentiment_score = 9
                if "nötr" in analysis_text.lower(): sentiment_score = 5

                for num in range(1, 11):
                    if f"{num}/10" in analysis_text or f"{num} / 10" in analysis_text:
                        professionalism = num

                if "%" in analysis_text:
                    import re
                    match = re.search(r"(\d{1,2})%", analysis_text)
                    if match:
                        spam_score = int(match.group(1))

                # Grafiklerle göster
                show_analysis_charts(sentiment_score, professionalism, spam_score)

            except Exception as e:
                st.error(f"Hata oluştu: {e}")


def show_analysis_charts(sentiment_score, professionalism, spam_score):
    """Basit üçlü gösterge grafiği"""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💬 Duygu Skoru")
        st.progress(sentiment_score / 10)
        st.caption(f"{sentiment_score}/10")

    with col2:
        st.subheader("💼 Profesyonellik")
        st.progress(professionalism / 10)
        st.caption(f"{professionalism}/10")

    with col3:
        st.subheader("🚫 Spam Olasılığı")
        st.progress(spam_score / 100)
        st.caption(f"%{spam_score}")
