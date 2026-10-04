"""Owner-configured premium assets. IDs are obtained from real Telegram messages."""
import os
from telegram.ext import CommandHandler
from bot.presentation import ICONS


async def configure_premium(update, context):
    allowed = {x.strip() for x in os.environ.get('ADMIN_IDS', '').split(',') if x.strip()}
    if str(update.effective_user.id) not in allowed:
        await update.effective_message.reply_text('Bu sozlama faqat bot admini uchun.')
        return
    key = context.args[0] if context.args else ''
    replied = update.effective_message.reply_to_message
    if key == 'sticker' and replied and replied.sticker:
        # Persistence keeps this opaque Telegram file ID; no sticker URL or token is exposed.
        context.bot_data['welcome_sticker'] = replied.sticker.file_id
        await update.effective_message.reply_text('Salomlashuv stikeri saqlandi.')
        return
    if key not in ICONS or not replied:
        await update.effective_message.reply_text(
            'Premium emoji xabariga Reply qilib /premium KEY yozing.\n'
            'KEY: ' + ', '.join(ICONS) + '\nStiker uchun: /premium sticker'
        )
        return
    entities = tuple(replied.entities or ()) + tuple(replied.caption_entities or ())
    value = next((x.custom_emoji_id for x in entities if x.type == 'custom_emoji'), None)
    if not value:
        await update.effective_message.reply_text('Reply qilingan xabarda premium emoji topilmadi.')
        return
    context.bot_data.setdefault('premium_icons', {})[key] = value
    await update.effective_message.reply_text('Premium ikonka saqlandi. /start orqali tekshiring.')


def build_premium_handler():
    return CommandHandler('premium', configure_premium)
