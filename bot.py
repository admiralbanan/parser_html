import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from parser import parse_news
from cache import Cache

logging.basicConfig(level=logging.INFO)
cache = Cache()

# Обработчик для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот для парсинга новостей Python Digest. Введите /help, чтобы увидеть доступные команды.")

# Обработчик для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/parse - Запустить парсер\n"
        "/view - Показать последние результаты\n"
        "/clear_cache - Очистить кэшированные данные\n"
        "/admin_parse - Запустить парсер с параметрами администратора (доступ только админу)"
    )

# Обработчик для команды /parse
async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    limit = int(context.args[0]) if context.args else 5
    news_data = parse_news(limit=limit)
    cache.save("latest_news", news_data)

    response = "\n\n".join(f"{news['title']}\n{news['link']}" for news in news_data)
    await update.message.reply_text(response)

# Обработчик для команды /view
async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    news_data = cache.load("latest_news")
    if news_data:
        response = "\n\n".join(f"{news['title']}\n{news['link']}" for news in news_data)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Нет данных в кэше. Используйте /parse для запуска парсинга.")

# Обработчик для команды /clear_cache
async def clear_cache(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cache.clear("latest_news")
    await update.message.reply_text("Кэш очищен.")

# Настройка бота
app = ApplicationBuilder().token("YOUR_TELEGRAM_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("parse", parse))
app.add_handler(CommandHandler("view", view))
app.add_handler(CommandHandler("clear_cache", clear_cache))

if __name__ == "__main__":
    app.run_polling()
