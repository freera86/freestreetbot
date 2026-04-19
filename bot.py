from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

TOKEN = "8746379343:AAG3I8Zuhok5Gs3LEvUO30kfFz87dvLQA_M"
ADMIN_ID = 8700346291

# память для ответа
user_to_reply = {}

# команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать!\n\n📩 Присылай свою новость (текст, фото или видео)\n\n🔒 Анонимность гарантирована — мы не публикуем и не передаём данные отправителя."
    )

# обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("reply_"):
        user_id = int(data.split("_")[1])
        user_to_reply[query.from_user.id] = user_id

        await query.message.reply_text("✏️ Напиши ответ пользователю:")

# обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # если админ отвечает
    if update.message.from_user.id in user_to_reply:
        target_id = user_to_reply[update.message.from_user.id]

        await context.bot.send_message(
            chat_id=target_id,
            text=f"💬 Ответ администратора:\n\n{update.message.text}"
        )

        await update.message.reply_text("✅ Ответ отправлен")
        del user_to_reply[update.message.from_user.id]
        return

    user_id = update.message.from_user.id

    # кнопка
    keyboard = [
        [InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ТЕКСТ
    if update.message.text:
        await context.bot.send_message(
            chat_id=8700346291,
            text=f"📩 Новая новость от {user_id}:\n\n{update.message.text}",
            reply_markup=reply_markup
        )

    # ФОТО
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=8700346291,
            photo=photo,
            caption=f"📸 Фото от {user_id}",
            reply_markup=reply_markup
        )

    # ВИДЕО
    elif update.message.video:
        video = update.message.video.file_id
        await context.bot.send_video(
            chat_id=8700346291,
            video=video,
            caption=f"🎥 Видео от {user_id}",
            reply_markup=reply_markup
        )

    await update.message.reply_text("✅ Спасибо! Новость отправлена.")

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Бот запущен...")
app.run_polling()
