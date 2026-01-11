# 🔑 Bramka - Telegram Access Code Bot

Telegram bot that generates time-limited access codes for secure authentication. Includes a professional web interface for code verification and user notifications.

## Features

- **🔑 Time-Limited Access Codes**: Generate unique codes valid for 10 minutes
- **📱 Telegram Integration**: Easy code generation through Telegram bot
- **🌐 Professional Web Interface**: Clean, responsive webpage for code verification
- **🔔 Real-time Notifications**: Users receive instant updates on login success and code expiration
- **📊 Login Logging**: All login attempts are logged for security
- **🚀 Future Ready**: Designed for integration with Allegro and OLX platforms

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kubamaj900-code/Gowno.git
cd Gowno
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Telegram bot token and username:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username
WEB_URL=http://localhost:5000
FLASK_PORT=5000
```

## Usage

### Running the Bot

Start the Telegram bot:
```bash
python bot.py
```

### Running the Web Server

In a separate terminal, start the Flask web server:
```bash
python web_server.py
```

The web interface will be available at `http://localhost:5000`

### Using the Bot

1. Start a conversation with your bot on Telegram
2. Send `/start` command
3. Click the "🔑 Bramka" button
4. You'll receive a unique access code and a link to the web interface
5. Open the link to view your code status
6. Click "Use access code" on the webpage to authenticate
7. You'll receive a notification in Telegram when the code is used
8. Codes expire after 10 minutes with an expiration notification

## Project Structure

```
.
├── bot.py              # Telegram bot implementation
├── web_server.py       # Flask web server
├── templates/          # HTML templates
│   ├── index.html     # Home page
│   └── access.html    # Access code page
├── static/            # Static files
│   └── css/
│       └── style.css  # Styling
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## How It Works

1. **Code Generation**: When a user clicks "🔑 Bramka" in Telegram, a unique 8-character code is generated
2. **Code Storage**: The code is stored in memory with user information and timestamp
3. **Web Access**: Users can access the code via a unique URL
4. **Verification**: The web interface checks code validity (not expired, not used)
5. **Usage**: When a code is used, the bot sends a notification to the user
6. **Expiration**: After 10 minutes, unused codes expire and users are notified

## Security Features

- Unique, randomly generated codes using secure random generation
- Time-limited validity (10 minutes)
- Single-use codes (cannot be reused)
- Automatic cleanup of expired codes
- Login attempt logging

## Future Integrations

The system is designed to support future integrations with:
- **Allegro**: Marketplace management
- **OLX**: Classified ads management

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather (required)
- `TELEGRAM_BOT_USERNAME`: Your Telegram bot username without @ (required)
- `WEB_URL`: Public URL where the web interface is hosted (for production)
- `FLASK_PORT`: Port for the Flask web server (default: 5000)

## Production Deployment

For production deployment:

1. Set `WEB_URL` to your public domain
2. Use a production WSGI server (e.g., Gunicorn) for Flask
3. Set up HTTPS with SSL certificates
4. Configure a reverse proxy (e.g., Nginx)
5. Use a process manager (e.g., systemd, supervisor) for the bot
6. Consider using a database instead of in-memory storage

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

## Development

The bot uses:
- `python-telegram-bot` for Telegram integration
- `Flask` for the web interface
- `python-dotenv` for environment configuration

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
