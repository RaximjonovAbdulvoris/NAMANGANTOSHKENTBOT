"""Choose the existing website or the existing native driver conversation."""
import os
from secrets import token_hex
from urllib.parse import urlparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ConversationHandler

from bot.handlers.start import require_region
from bot.presentation import inline_button
from bot.regions import get_region, region_name

CONNECT_CHOICE = 50


def site_url():
    value = os.environ.get('CONNECT_SITE_URL', 'https://wb-humo-connect.abdulvoriszs.chatgpt.site').strip()
    parsed = urlparse(value)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        return None
    return value


async def choose_connection(update, context):
    if not await require_region(update, context):
        return ConversationHandler.END
    nonce = token_hex(8)
    context.user_data['connect_nonce'] = nonce
    buttons = []
    url = site_url()
    if url:
        # Personal data never goes into a public URL. The website collects and
        # validates its own contact fields until a trusted server bridge is added.
        buttons.append([inline_button('Saytda to‘ldirish', 'website', bot_data=context.bot_data, url=url)])
    buttons.append([inline_button('Botda to‘ldirish', 'bot', bot_data=context.bot_data, callback_data=f'connect:bot:{nonce}')])
    text = (f'<b>ULANISH · {region_name(get_region(context))}</b>\n\n'
            'Arizani qayerda to‘ldirasiz?')
    try:
        await update.effective_message.reply_text(
            text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons),
        )
    except BadRequest as error:
        if 'emoji' not in str(error).lower() or not any(
            button.api_kwargs for row in buttons for button in row
        ):
            raise
        plain = [[InlineKeyboardButton(b.text, url=b.url, callback_data=b.callback_data)
                  for b in row] for row in buttons]
        await update.effective_message.reply_text(
            text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(plain),
        )
    return CONNECT_CHOICE


async def connect_in_bot(update, context):
    from bot.handlers.driver import start_driver
    query = update.callback_query
    nonce = context.user_data.get('connect_nonce')
    if not nonce or query.data != f'connect:bot:{nonce}':
        await query.answer('Tanlov eskirgan. /connect ni qayta yuboring.', show_alert=True)
        return CONNECT_CHOICE
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    context.user_data.pop('connect_nonce', None)
    return await start_driver(update, context)
