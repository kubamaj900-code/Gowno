import os
import logging
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store for access codes: {code: {'user_id': int, 'username': str, 'created_at': datetime, 'used': bool}}
access_codes: Dict[str, dict] = {}

def generate_access_code(length: int = 8) -> str:
    """Generate a random access code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def cleanup_expired_codes():
    """Remove expired codes from storage."""
    now = datetime.now()
    expired_codes = [
        code for code, data in access_codes.items()
        if now - data['created_at'] > timedelta(minutes=10)
    ]
    for code in expired_codes:
        del access_codes[code]
        logger.info(f"Removed expired code: {code}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    cleanup_expired_codes()
    
    keyboard = [
        [InlineKeyboardButton("🔑 Bramka", callback_data='bramka')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    user = update.effective_user
    await update.message.reply_text(
        f"Witaj {user.first_name}! 👋\n\n"
        f"Wybierz opcję z menu poniżej:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'bramka':
        await handle_bramka(query, context)

async def handle_bramka(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the Bramka button - generate access code."""
    cleanup_expired_codes()
    
    user = query.from_user
    code = generate_access_code()
    
    # Store the access code
    access_codes[code] = {
        'user_id': user.id,
        'username': user.username or user.first_name,
        'created_at': datetime.now(),
        'used': False
    }
    
    # Log the code generation
    logger.info(f"Generated code {code} for user {user.id} ({user.username or user.first_name})")
    
    # Get the web server URL from environment or use default
    web_url = os.getenv('WEB_URL', 'http://localhost:5000')
    
    await query.edit_message_text(
        f"🔑 Twój kod dostępu: `{code}`\n\n"
        f"Kod jest ważny przez 10 minut.\n\n"
        f"Link do strony: {web_url}/access/{code}\n\n"
        f"Wygenerowano: {datetime.now().strftime('%H:%M:%S')}",
        parse_mode='Markdown'
    )
    
    # Schedule expiration notification
    context.job_queue.run_once(
        notify_expiration,
        when=600,  # 10 minutes
        data={'code': code, 'user_id': user.id, 'chat_id': query.message.chat_id}
    )

async def notify_expiration(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Notify user when their code expires."""
    job_data = context.job.data
    code = job_data['code']
    chat_id = job_data['chat_id']
    
    # Check if code still exists and wasn't used
    if code in access_codes and not access_codes[code]['used']:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⏰ Kod `{code}` wygasł po 10 minutach.",
            parse_mode='Markdown'
        )
        logger.info(f"Code {code} expired")
        # Remove from storage
        if code in access_codes:
            del access_codes[code]

def mark_code_as_used(code: str) -> Optional[dict]:
    """Mark a code as used and return user data."""
    cleanup_expired_codes()
    
    if code not in access_codes:
        return None
    
    code_data = access_codes[code]
    
    # Check if expired
    if datetime.now() - code_data['created_at'] > timedelta(minutes=10):
        del access_codes[code]
        return None
    
    # Check if already used
    if code_data['used']:
        return None
    
    # Mark as used
    code_data['used'] = True
    logger.info(f"Code {code} used by user {code_data['user_id']}")
    
    return code_data

async def notify_login_success(application: Application, user_id: int, code: str) -> None:
    """Notify user of successful login."""
    try:
        await application.bot.send_message(
            chat_id=user_id,
            text=f"✅ Login successful!\n\nKod `{code}` został użyty pomyślnie.",
            parse_mode='Markdown'
        )
        logger.info(f"Sent login success notification to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send notification to user {user_id}: {e}")

def get_code_status(code: str) -> dict:
    """Get the status of an access code."""
    cleanup_expired_codes()
    
    if code not in access_codes:
        return {'status': 'invalid', 'message': 'Kod nie istnieje lub wygasł'}
    
    code_data = access_codes[code]
    
    # Check if expired
    time_left = timedelta(minutes=10) - (datetime.now() - code_data['created_at'])
    if time_left.total_seconds() <= 0:
        del access_codes[code]
        return {'status': 'expired', 'message': 'Kod wygasł'}
    
    if code_data['used']:
        return {'status': 'used', 'message': 'Kod został już użyty'}
    
    return {
        'status': 'valid',
        'message': 'Kod jest aktywny',
        'username': code_data['username'],
        'time_left': int(time_left.total_seconds()),
        'created_at': code_data['created_at'].strftime('%H:%M:%S')
    }

def main() -> None:
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
