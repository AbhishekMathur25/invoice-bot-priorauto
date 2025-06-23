# invoice-bot-priorauto
An AI-powered Telegram bot for automated invoice extraction, Excel reporting, and daily email delivery — built for Prior Auto Accessories using Google Gemini, Python, and async architecture.


# Automated Invoice Extraction and Reporting Bot

This project is an end-to-end solution for automated invoice management using Telegram, Google Gemini AI, and Excel reporting.

## Features
- **Telegram Bot**: Receive PDF invoices via Telegram and save them in date-wise folders.
- **AI Extraction**: Use Google Gemini AI to extract structured data from PDF invoices.
- **Excel Reporting**: Store extracted data in organized Excel files for each day.
- **Daily Email**: Automatically email the daily Excel report at 6pm India time.
- **API Key Rotation**: Supports multiple Gemini API keys for uninterrupted extraction.

## How It Works
1. **Send Invoice**: Send a PDF invoice to the Telegram bot.
2. **Extraction**: The bot saves the PDF and processes it with Gemini AI.
3. **Excel Storage**: Extracted data is appended to a daily Excel file in the `invoices/` folder.
4. **Daily Report**: At 6pm IST, the bot sends the day's Excel file to your email.

## Setup
1. **Clone the repository** and install dependencies:
   ```sh
   pip install -r req.txt
   ```
2. **Configure environment variables** in `.env`:
   ```env
   GEMINI_API_KEYS=your_gemini_api_key1,your_gemini_api_key2
   ```
3. **Set up your Telegram bot** with BotFather and update `BOT_TOKEN` in `tel.py`.
4. **Set up email credentials** in `mail.py`.

## Running the Project
- Start the Telegram bot:
  ```sh
  python tel.py
  ```
- The bot will listen for PDF uploads and process them automatically.
- At 6pm IST, the daily Excel report will be emailed.

## File Structure
- `tel.py` — Telegram bot and scheduler
- `gemini.py` — Gemini AI extraction logic
- `excel.py` — Excel file handling
- `mail.py` — Email sending script
- `req.txt` — Python dependencies
- `.env` — Environment variables (API keys)
