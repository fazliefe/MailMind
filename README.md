MailMind

GPT destekli kurumsal e-posta asistanı: yaz, yanıtla, analiz et; takvim daveti üret, planlı gönder, sesle komut ver ve TTS ile dinle.
✍️📬🧠📅⏰🗣️🔊

🚀 Özellikler

✍️ E-posta oluşturma – şablonlar, dil/ton seçimi, yaratıcılık sürgüsü (0.00–1.00)
↩️ Cevaplama modu – gelen e-postayı özetleyip uygun tonda yanıt taslağı
🧠 Duygu & spam analizi – skor + iyileştirme önerileri
📅 Takvim daveti üretimi – toplantı özeti/konum/bağlantı alanları
🗣️ Sesli komut – dikte ile içerik/komut verme
🔊 TTS (metinden sese) – taslağı ses dosyasına dönüştürme
⏰ Planlı gönderim – belirli tarih/saatte otomatik gönder
📊 İstatistikler – kullanım ve performans görünümü
👤 Profil & Ayarlar – varsayılan dil, ton, imza, yaratıcılık
🖥️ Ekranlar (kısa tur)
E-Posta Oluştur: Şablon → Amaç → Ton → Dil → Yaratıcılık → Opsiyonlar (Profesyonelleştir, TTS, Taslak, Planlı Gönder) → Oluştur
Cevapla: Metni yapıştır, ton/dil seç, yanıt taslağı al
Analiz Et: Duygu (pozitif/nötr/negatif) + spam skoru + ipuçları
Takvim: Toplantı daveti metni üret
Planlı Gönderimler: Kuyruktaki e-postaları ve zamanlamayı görüntüle
İstatistikler: Üretim/yanıt/analiz rakamları
Profil/Ayarlar: Tercihler ve imza yönetimi
Sesli Araçlar: Sesli komut ve TTS

⚡ Hızlı Başlangıç
# 1) Depoyu al
git clone <repo-url>
cd mailmind

# 2) Bağımlılıklar
# (Örnek: Node.js)
npm install
# (Alternatif: Python)
# pip install -r requirements.txt

# 3) Ortam değişkenleri
cp .env.example .env  # anahtarları ve SMTP bilgilerini doldurun

# 4) Geliştirme sunucusu
npm run dev
# veya
# python app.py

🔐 .env Örneği
# LLM
OPENAI_API_KEY=your_key
MODEL_NAME=gpt-4o-mini

# E-posta (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=example@gmail.com
SMTP_PASS=app_password
SENDER_NAME=MailMind

# TTS / STT
TTS_PROVIDER=elevenlabs
TTS_API_KEY=your_tts_key
STT_PROVIDER=whisper

# Planlı gönderim
JOB_CRON_TZ=Europe/Istanbul

🧭 Kullanım Akışı
Yeni E-Posta Oluştur sekmesine gir.
Amaç, Ton (Kısa/Resmi/Samimi…), Dil (TR/EN) ve Yaratıcılık değerini seç.

Gerekirse Profesyonelleştir, TTS, Taslak, Belirli tarihte gönder kutularını işaretle.
Oluştur’a bas; metni düzenle ve Gönder ya da Planla.

Cevapla ile gelen e-postaları aynı ayarlarla yanıtla.
Analiz Et ile duygu/spam sonuçlarını kontrol et; Takvim ile davet metni üret.

Planlı Gönderimler ekranından tarih/saat kuyruğunu takip et.
🧩 API Uçları (örnek)
POST /api/generate-email
Body: { purpose, tone, lang, creativity, options }
POST /api/reply
Body: { incomingText, tone, lang }
POST /api/analyze
Body: { text }  -> { sentiment, spamScore, tips }
POT /api/schedule
Body: { emailPayload, sendAt }  -> 204
GET  /api/stats
Yanıt örneği
{
  "subject": "Toplantı Erteleme",
  "body": "Merhaba ...",
  "language": "tr",
  "tone": "kısa",
  "tips": ["Daha net tarih verin", "Bağlantıyı ekleyin"]
}

🏗️ Teknik Mimari (özet)

UI: React/Vue (formlar, sekmeler)
Backend: Node/Express veya Python/FastAPI
LLM Katmanı: OpenAI API (prompt + sistem yönergeleri)
TTS/STT: Sağlayıcı eklentileri (modüler yapı)
Planlama: cron/queue (BullMQ, Celery, RQ)
Depolama: Taslaklar, planlar, loglar için DB (PostgreSQL/SQLite)
E-posta: SMTP/Graph API ile gönderim

🔒 Güvenlik & Gizlilik
API anahtarlarını .env’de tutun; sürüme eklemeyin.
SMTP için uygulama şifresi kullanın.
PII içeren metinleri loglarda maskeleyin.
Planlı gönderimde saat dilimini (JOB_CRON_TZ) doğru ayarlayın.

❓ SSS
Yaratıcılık sürgüsü ne işe yarar?
Düşük → daha net/resmi, yüksek → daha esnek/yaratıcı dil.
Sesli komut vs TTS?
Sesli komut girdi içindir; TTS çıktıyı sese çevirir.
Planlı gönderim çalışmıyor?
Sunucunun saat dilimi + cron job + SMTP ayarlarını kontrol edin.

🗺️ Yol Haritası

Değişkenli şablonlar ({{ad}}, {{tarih}})
Takvim API entegrasyonları (Google/Outlook)
Takım paylaşımı ve rol & yetki
Gelişmiş istatistikler ve dışa aktarma