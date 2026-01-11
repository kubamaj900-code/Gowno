from flask import Flask, render_template, jsonify
import os
import logging
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Import bot functions
import bot

# Get bot username from environment
BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME', 'your_bot_username')

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html', bot_username=BOT_USERNAME)

@app.route('/access/<code>')
def access_page(code):
    """Display access code page."""
    status = bot.get_code_status(code)
    return render_template('access.html', code=code, status=status, bot_username=BOT_USERNAME)

def send_notification_async(user_id, code):
    """Send notification in a separate thread."""
    try:
        from telegram.ext import Application
        import asyncio
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            return
            
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        application = Application.builder().token(token).build()
        loop.run_until_complete(bot.notify_login_success(application, user_id, code))
        loop.close()
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

@app.route('/api/use_code/<code>', methods=['POST'])
def use_code(code):
    """API endpoint to use a code."""
    code_data = bot.mark_code_as_used(code)
    
    if code_data is None:
        logger.warning(f"Login attempt with invalid/expired code: {code}")
        return jsonify({
            'success': False,
            'message': 'Kod jest nieprawidłowy, wygasł lub został już użyty'
        }), 400
    
    # Log successful login
    logger.info(f"Successful login: code={code}, user={code_data['user_id']} ({code_data['username']})")
    
    # Send notification in background thread to avoid blocking
    notification_thread = threading.Thread(
        target=send_notification_async,
        args=(code_data['user_id'], code)
    )
    notification_thread.daemon = True
    notification_thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Login successful!',
        'username': code_data['username']
    })

@app.route('/api/check_code/<code>')
def check_code(code):
    """API endpoint to check code status."""
    status = bot.get_code_status(code)
    return jsonify(status)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
