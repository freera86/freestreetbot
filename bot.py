from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8746379343:AAG3I8Zuhok5Gs3LEvUO30kfFz87dvLQA_M"
ADMIN_ID = 8700346291
# команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать!\n\n📩 Присылай свою новость (текст, фото или видео)\n\n🔒 Анонимность гарантирована — мы не публикуем и не передаём данные отправителя."
    )

# обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ТЕКСТ
    if update.message.text:
        await context.bot.send_message(
            chat_id=8700346291,
            text=f"📩 Новая новость:\n\n{update.message.text}"
        )

    # ФОТО
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=8700346291,
            photo=photo,
            caption="📸 Новое фото"
        )

    # ВИДЕО
    elif update.message.video:
        video = update.message.video.file_id
        await context.bot.send_video(
            chat_id=8700346291,
            video=video,
            caption="🎥 Новое видео"
        )

    # ОТВЕТ ПОЛЬЗОВАТЕЛЮ
    await update.message.reply_text("✅ Спасибо! Новость отправлена.")

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Бот запущен...")
app.run_polling()
