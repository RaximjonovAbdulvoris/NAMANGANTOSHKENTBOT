import os
import unittest
from types import SimpleNamespace as N
from unittest.mock import AsyncMock, patch

for key in ('TELEGRAM_BOT_TOKEN', 'DRIVER_GROUP_1', 'DRIVER_GROUP_2', 'BRAND_GROUP'):
    os.environ.setdefault(key, '123:test' if key == 'TELEGRAM_BOT_TOKEN' else '-1001')

from telegram.error import BadRequest
from telegram.ext import ConversationHandler
from bot.handlers import connect, driver, premium
from bot.presentation import welcome, reply_html
from bot.regions import clear_application


def fixture():
    message = N(reply_text=AsyncMock(), reply_to_message=None, contact=None, text='')
    update = N(effective_chat=N(type='private'), effective_user=N(id=123),
               effective_message=message, message=message, callback_query=None)
    context = N(user_data={'region':'tashkent'}, bot_data={}, args=[])
    return update, context


class ConnectTests(unittest.IsolatedAsyncioTestCase):
    async def test_two_choices_without_private_data_in_url(self):
        update, ctx = fixture()
        ctx.user_data['phone'] = '+998901234567'
        with patch.dict(os.environ, {'CONNECT_SITE_URL':'https://example.com/connect'}):
            self.assertEqual(await connect.choose_connection(update, ctx), connect.CONNECT_CHOICE)
        rows = update.effective_message.reply_text.await_args.kwargs['reply_markup'].inline_keyboard
        self.assertEqual(rows[0][0].url, 'https://example.com/connect')
        self.assertNotIn('998', rows[0][0].url)
        self.assertEqual(rows[1][0].callback_data, 'connect:bot:' + ctx.user_data['connect_nonce'])

    async def test_old_callback_cannot_open_native_form(self):
        update, ctx = fixture()
        ctx.user_data['connect_nonce'] = 'new'
        update.callback_query = N(data='connect:bot:old', answer=AsyncMock())
        with patch.object(driver, 'start_driver', AsyncMock()) as begin:
            await connect.connect_in_bot(update, ctx)
            begin.assert_not_awaited()

    async def test_current_callback_enters_existing_driver_state(self):
        update, ctx = fixture()
        ctx.user_data['connect_nonce'] = 'current'
        update.callback_query = N(data='connect:bot:current', answer=AsyncMock(), edit_message_reply_markup=AsyncMock())
        with patch.object(driver, 'start_driver', AsyncMock(return_value=driver.NAME)) as begin:
            self.assertEqual(await connect.connect_in_bot(update, ctx), driver.NAME)
            begin.assert_awaited_once()
        self.assertNotIn('connect_nonce', ctx.user_data)

    async def test_premium_rejection_keeps_connection_buttons_working(self):
        update, ctx = fixture()
        ctx.bot_data['premium_icons'] = {'website':'123'}
        update.effective_message.reply_text.side_effect = [BadRequest('CUSTOM_EMOJI_INVALID'), None]
        await connect.choose_connection(update, ctx)
        rows = update.effective_message.reply_text.await_args.kwargs['reply_markup'].inline_keyboard
        self.assertTrue(all(not b.api_kwargs for row in rows for b in row))

    async def test_untrusted_contact_and_invalid_number_rejected(self):
        update, ctx = fixture()
        update.message.contact = N(user_id=999, phone_number='998901234567')
        self.assertEqual(await driver.get_phone(update, ctx), driver.PHONE)
        self.assertNotIn('phone', ctx.user_data)
        update.message.contact = None
        update.message.text = '123456789'
        self.assertEqual(await driver.get_phone(update, ctx), driver.PHONE)
        update.message.text = '+998 90 123 45 67'
        self.assertEqual(await driver.get_phone(update, ctx), driver.WARN_DOCS)
        clear_application(ctx)
        self.assertEqual(ctx.user_data['profile']['phone'], '+998901234567')

    async def test_premium_configuration_requires_admin(self):
        update, ctx = fixture()
        with patch.dict(os.environ, {'ADMIN_IDS':'456'}):
            await premium.configure_premium(update, ctx)
        self.assertEqual(ctx.bot_data, {})

    async def test_premium_asset_is_taken_from_replied_message(self):
        update, ctx = fixture()
        ctx.args = ['welcome']
        update.message.reply_to_message = N(entities=[N(type='custom_emoji',custom_emoji_id='12345')],caption_entities=[])
        with patch.dict(os.environ, {'ADMIN_IDS':'123'}):
            await premium.configure_premium(update, ctx)
        self.assertEqual(ctx.bot_data['premium_icons']['welcome'], '12345')
        self.assertIn('emoji-id="12345"', welcome('<User>', bot_data=ctx.bot_data))
        self.assertIn('&lt;User&gt;', welcome('<User>', bot_data=ctx.bot_data))

    async def test_emoji_text_has_plain_fallback(self):
        message = N(reply_text=AsyncMock(side_effect=[BadRequest('CUSTOM_EMOJI_INVALID'), None]))
        await reply_html(message, '<tg-emoji emoji-id="123">👋</tg-emoji>', '👋')
        self.assertEqual(message.reply_text.await_args.args[0], '👋')
