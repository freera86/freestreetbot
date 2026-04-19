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
            text=f"📩 Новая новость от {update.message.from_user.id}:\n\n{update.message.text}"
        )

    # ФОТО
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=8700346291,
            photo=photo,
            caption=f"📸 Фото от {update.message.from_user.id}"
        )

    # ВИДЕО
    elif update.message.video:
        video = update.message.video.file_id
        await context.bot.send_video(
            chat_id=8700346291,
            video=video,
            caption=f"🎥 Видео от {update.message.from_user.id}"
        )

    # ОТВЕТ ПОЛЬЗОВАТЕЛЮ
    await update.message.reply_text("✅ Спасибо! Новость отправлена.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        text = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 Ответ администратора:\n\n{text}"
        )

        await update.message.reply_text("✅ Ответ отправлен")

    except:
        await update.message.reply_text("❌ Используй: /reply user_id текст")

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.add_handler(CommandHandler("reply", reply))

print("Бот запущен...")
app.run_polling()
    # ОТВЕТ ПОЛЬЗОВАТЕЛЮ
    await update.message.reply_text("✅ Спасибо! Новость отправлена.")

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Бот запущен...")
app.run_polling()
