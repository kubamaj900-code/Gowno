# Bramka Quick Start Guide

## Setup (First Time)

1. **Create your Telegram bot**
   ```
   Message @BotFather on Telegram
   Send: /newbot
   Follow the prompts
   Save your bot token and username
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your bot token and username
   ```

4. **Run the system**
   ```bash
   python run.py
   ```

## Quick Commands

### Start both services
```bash
python run.py
```

### Start only the bot
```bash
python bot.py
```

### Start only the web server
```bash
python web_server.py
```

### Run tests
```bash
python test_bot.py
```

## File Structure

```
.
├── bot.py              # Telegram bot (handles /start, code generation)
├── web_server.py       # Flask web app (displays codes, handles usage)
├── run.py              # Convenience script to run both services
├── test_bot.py         # Unit tests for core functionality
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── templates/
│   ├── index.html      # Home page
│   └── access.html     # Access code display page
└── static/
    └── css/
        └── style.css   # Professional styling
```

## Environment Variables

Required:
- `TELEGRAM_BOT_TOKEN` - Your bot token from BotFather
- `TELEGRAM_BOT_USERNAME` - Your bot's username (without @)

Optional:
- `WEB_URL` - Public URL (default: http://localhost:5000)
- `FLASK_PORT` - Web server port (default: 5000)

## How It Works

1. User clicks "🔑 Bramka" in Telegram
2. Bot generates 8-character code (valid 10 minutes)
3. Bot sends code + web link to user
4. User opens link, sees code with countdown
5. User clicks "Use code" on webpage
6. Bot sends "Login successful" notification
7. After 10 min: Bot sends "Code expired" notification (if unused)

## Common Issues

**Bot not responding?**
- Check your bot token in .env
- Make sure bot.py is running
- Send /start to your bot first

**Web page not loading?**
- Check web_server.py is running
- Verify port 5000 is available
- Try http://localhost:5000

**No notifications?**
- Both services must be running
- Check bot token is correct
- Look for errors in terminal

## Production Deployment

For production use:
1. Set `WEB_URL` to your public domain
2. Use HTTPS (SSL certificates)
3. Use a production WSGI server (Gunicorn)
4. Use a reverse proxy (Nginx)
5. Use a process manager (systemd/supervisor)
6. Consider persistent storage instead of in-memory

Example:
```bash
# Install Gunicorn
pip install gunicorn

# Run web server with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app

# Run bot with systemd
sudo systemctl start bramka-bot
```

## Features

✅ Time-limited access codes (10 minutes)  
✅ Professional web interface  
✅ Real-time notifications  
✅ Login attempt logging  
✅ Single-use codes  
✅ Automatic expiration cleanup  
✅ Responsive design  
✅ Ready for Allegro/OLX integration
