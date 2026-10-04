"""Telegram presentation with optional custom emoji and safe plain fallback."""
import logging
import os
from html import escape

from telegram import InlineKeyboardButton, KeyboardButton
from telegram.error import BadRequest

logger = logging.getLogger(__name__)
ICONS = {
    'join': '📝', 'brand': '🎨', 'energy': '⚡', 'contact': '📞',
    'office': '📍', 'region': '🔄', 'welcome': '👋', 'confirm': '✅',
    'website': '🌐', 'bot': '💬',
}


def emoji_id(key, bot_data=None):
    value = (bot_data or {}).get('premium_icons', {}).get(key)
    value = value or os.environ.get('EMOJI_' + key.upper(), '')
    return str(value) if str(value or '').isdigit() else None


def icon(key, bot_data=None):
    alt = ICONS[key]
    value = emoji_id(key, bot_data)
    return f'<tg-emoji emoji-id="{value}">{alt}</tg-emoji>' if value else alt


def inline_button(text, key, bot_data=None, **kwargs):
    value = emoji_id(key, bot_data)
    if value:
        kwargs['api_kwargs'] = {'icon_custom_emoji_id': value}
    return InlineKeyboardButton(text, **kwargs)


def menu_button(text, key):
    return KeyboardButton(text)


async def reply_html(message, rich, plain, **kwargs):
    try:
        return await message.reply_text(rich, parse_mode='HTML', **kwargs)
    except BadRequest as error:
        # Only unsupported custom emoji should trigger a second request.
        detail = str(error).lower()
        if '<tg-emoji' not in rich or not any(s in detail for s in ('emoji', 'entity', 'entities')):
            raise
        return await message.reply_text(plain, parse_mode='HTML', **kwargs)


async def welcome_sticker(message, bot_data=None):
    sticker = (bot_data or {}).get('welcome_sticker') or os.environ.get('WELCOME_STICKER_FILE_ID', '')
    if not sticker:
        return
    try:
        await message.reply_sticker(sticker)
    except BadRequest:
        logger.warning('Welcome sticker unavailable; continuing with text.')


def welcome(name, phone='', bot_data=None, premium=True):
    wave = icon('welcome', bot_data) if premium else ICONS['welcome']
    return (
        f'Assalomu alaykum, <b>{escape(name)}</b> {wave}\n\n'
        '<b>WB HUMO TAXI</b>\nWB Taxi rasmiy hamkori · O‘zbekiston\n'
        + (f'\nRaqamingiz saqlangan: {escape(phone)}\n' if phone else '')
        + '\nUlanish, brendlash va Spectre Energy uchun ariza qoldiring.\n'
        'Savolingizni yozishingiz yoki /connect orqali ulanishni boshlashingiz mumkin.'
    )
