#!/usr/bin/env python3
"""
Runner script to start both the Telegram bot and Flask web server.
"""
import os
import sys
import subprocess
import time
import signal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_token():
    """Check if Telegram bot token is configured."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token or token == 'your_bot_token_here':
        print("ERROR: TELEGRAM_BOT_TOKEN not configured in .env file")
        print("Please copy .env.example to .env and add your bot token")
        return False
    return True

def main():
    """Start both bot and web server."""
    if not check_token():
        sys.exit(1)
    
    processes = []
    
    try:
        print("Starting Flask web server...")
        web_process = subprocess.Popen([sys.executable, 'web_server.py'])
        processes.append(web_process)
        
        # Give web server time to start
        time.sleep(2)
        
        print("Starting Telegram bot...")
        bot_process = subprocess.Popen([sys.executable, 'bot.py'])
        processes.append(bot_process)
        
        print("\n" + "="*50)
        print("Bramka system is running!")
        print("="*50)
        print(f"Web interface: {os.getenv('WEB_URL', 'http://localhost:5000')}")
        print("Telegram bot: Active")
        print("\nPress Ctrl+C to stop")
        print("="*50 + "\n")
        
        # Wait for processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\nStopping services...")
        for process in processes:
            process.send_signal(signal.SIGTERM)
            process.wait()
        print("Services stopped.")
        
    except Exception as e:
        print(f"Error: {e}")
        for process in processes:
            process.kill()
        sys.exit(1)

if __name__ == '__main__':
    main()
