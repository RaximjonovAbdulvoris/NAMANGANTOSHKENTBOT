# WB HUMO Taxi · Telegram bot

Namuna va ofis rasmlari `bot/templates` papkasida. Rasm topilmasa, bot matn bilan davom etadi.

NAMANTOSH loyihasidagi mavjud haydovchi, brend, Spectre va hududiy operator oqimlarini saqlagan alohida bot nusxasi.

## Yangilanish

- **Aloqa va manzil**: telefon, Telegram, Instagram, ofis manzili va xarita bitta postda, shahar bo‘yicha.
- Shaxsiy salomlashuv, ixcham ikki ustunli menyu; Toshkent/Namangan yo‘nalishlari saqlangan.
- `Ulanish uchun Ariza` va `/connect`: sayt yoki bot ichida ariza.
- Bot ichidagi mavjud hujjatlar, rasmlar, obuna tekshiruvi va operator/arxiv tugmalari saqlangan.
- Telefon `+998` va 9 raqam bilan tekshiriladi. Boshqa odamning kontakti qabul qilinmaydi.
- Botda yuborilgan telefon keyingi `/start` va hudud almashtirishda saqlanadi.
- Premium salomlashuv emojisi, ulanish tanlovidagi premium tugma ikonkalari va ixtiyoriy salomlashuv stikeri.

## Ishga tushirish

Python 3.11+ kerak. `python -m pip install -r requirements.txt`, keyin `python -m bot.main`.
`.env.example` dagi sozlamalarni Replit Secrets yoki hosting environment’ga kiriting. `.env` fayli avtomatik o‘qilmaydi. `PERSIST_DIR` doimiy yozish mumkin bo‘lgan disk bo‘lsin; shu joyda suhbat holatlari saqlanadi. Bitta token bilan bitta polling xizmati ishlasin.

Bu repo o‘zidan-o‘zi mavjud asosiy botni o‘zgartirmaydi. Ishga tushirishdan oldin kerakli token va guruhlar sozlanadi. Asosiy token bilan ishga tushirishda Replitdagi eski xizmat to‘xtatiladi.

## Premium sozlash

Botni yaratgan akkauntda Premium yoki Telegram ruxsat beradigan boshqa custom emoji imkoniyati kerak. `ADMIN_IDS` ga adminning raqamli Telegram ID sini kiriting. Botga premium emoji yuboring, unga Reply qilib `/premium welcome`, `/premium website` yoki `/premium bot` yozing. Stikerga Reply qilib `/premium sticker` yozing. Sozlamalar persistence’da saqlanadi. `EMOJI_*` va `WELCOME_STICKER_FILE_ID` orqali ham sozlash mumkin.

Emoji uchun faqat Telegramdan olingan haqiqiy ID ishlatiladi; repo ichida to‘qilgan ID yo‘q. Premium emoji matni Telegram tomonidan rad qilinsa, salomlashuv oddiy emoji bilan yuboriladi. Oddiy menyu tugmalari eski nomlarini saqlaydi; premium ikonka server imkoniyatiga qarab ulanishning inline tugmalarida ko‘rsatiladi.

## Sayt bilan aloqa

`CONNECT_SITE_URL` HTTPS ulanish formasi. U saytni ochadi, telefon yoki hujjatlarni ochiq URLga joylamaydi. Hozir bu alohida repo saytdagi telefonni avtomatik to‘ldirmaydi: saytda kontakt maydonlari kiritiladi. Telegramdagi tasdiqlangan telefonni saytga avtomatik uzatish uchun autentifikatsiyali server integratsiyasi alohida kerak.

Mavjud bot hujjatlarni operatorlarga yuboradi. Ushbu nusxaga AI tekshiruvi yoki WB bazasiga avtomatik yuborish qo‘shilmadi.

## Tekshirish

`python -m unittest discover -s tests -v`
