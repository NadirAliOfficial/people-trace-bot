# People Trace Bot

Telegram bot for community-driven person search and tracing. Allows users to submit and query missing person reports.

## Features
- Submit missing person reports
- Search by name or location
- Admin moderation panel

## Requirements
```
pip install python-telegram-bot
```

```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file with these variables (values are your own):
- `TOKEN` - Telegram bot token
- `MONGODB_URI`, `MONGODB_NAME` - MongoDB connection and database name
- `OWNER_TELEGRAM_ID` - Telegram ID of the bot owner
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` - Twilio credentials for OTP
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` - image uploads
- `SOL_*` and `TRON_*` wallet and collect keys - Solana and Tron wallet settings

## Usage
```bash
python src/main.py
```
`python bot_runner.py` (also used by the `Procfile`) runs the same bot and restarts it when a `.py` file changes.

## Project Structure
- `src/` - bot code: `handlers/`, `services/`, `models/`, `database/`, `utils/`, `config/`
- `bot_runner.py` - auto-restart runner
- `test/` - transfer and province tests

## License
MIT
<!-- updated: 2026-06-13 -->

