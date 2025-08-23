# Telegram Auto-Notify Bot for GAG API

Bot Telegram ini memantau API [GAG API](https://gagapi.onrender.com/alldata) secara real-time, menampilkan data seperti **Weather**, **Weather History**, **Traveling Merchant**, dan item kategori lain. Bot akan **mengirim pesan baru setiap ada perubahan** tanpa harus dikontrol lewat chat.

---

## Fitur

- Menampilkan **Weather** termasuk `type`, `active`, `effects`, dan `lastUpdated`.
- Menampilkan **Weather History**.
- Menampilkan **Traveling Merchant** beserta item, ketersediaan, dan waktu kedatangan/pulang.
- Menampilkan semua kategori item (`gear`, `seeds`, `eggs`, `honey`, `cosmetics`, dll).
- Mengirim pesan baru otomatis ketika data berubah.
- Interval update bisa disesuaikan (default 10 detik).

---
## Untuk Windows
```bash

set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
set TARGET_CHAT_ID=YOUR_CHAT_ID
set WATCH_INTERVAL=10

## Persiapan

1. Install Python 3.10+  
2. Clone repository:

```bash
git clone https://github.com/username/telegram-gag-bot.git
cd telegram-gag-bot


