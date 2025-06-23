import os
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from gemini import run_gemini_invoice_extraction
import logging
import subprocess
import asyncio
import pytz


BOT_TOKEN = 'your token here'
BASE_DIR = 'downloads'
os.makedirs(BASE_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Function to save the document sent by the user
async def save_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        doc = update.message.document
        file_id = doc.file_id
        file_name = doc.file_name or "unnamed_file"

        today = datetime.now().strftime('%Y-%m-%d')
        folder_path = os.path.join(BASE_DIR, today)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        bot: Bot = context.bot
        telegram_file = await bot.get_file(file_id)
        await telegram_file.download_to_drive(custom_path=file_path)

        await update.message.reply_text(f"✅ Saved `{file_name}`", parse_mode="Markdown")

        # Call gemini to process the PDF after download
        if file_path.lower().endswith('.pdf'):
            await run_gemini_invoice_extraction(file_path)
    except Exception as e:
        logging.error(f"Error in save_document: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

# Optional start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a document and I’ll save it for you date-wise!")


# Scheduler to run mail.py every day at 6pm
async def daily_mail_scheduler():
    india = pytz.timezone('Asia/Kolkata')
    while True:
        now = datetime.now(india)
        target = now.replace(hour=18, minute=0, second=0, microsecond=0)
        if now >= target:
            # If already past 6pm, schedule for next day
            target = target.replace(day=now.day + 1)
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        subprocess.run(['python', 'mail.py'])

# This script is a Telegram bot that saves documents sent to it and processes PDF invoices using Gemini AI.
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Document.ALL, save_document))

    loop = asyncio.get_event_loop()
    loop.create_task(daily_mail_scheduler())

    application.run_polling()


if __name__ == '__main__':
    main()
