import requests
import hashlib
import time
import os
from datetime import datetime
from flask import Flask
import threading
import subprocess
import sys

# ====== CONFIG ======
URL = os.getenv("RESULT_URL", "https://yourcollege.edu/results")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))  # seconds between checks
PORT = int(os.getenv("PORT", 5000))
# =====================

# Flask app for keep-alive
app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint to keep the app alive"""
    return {"status": "✅ Result Notifier is running"}, 200

@app.route('/health')
def health():
    """Alternative health endpoint"""
    return {"status": "alive"}, 200

def setup_playwright():
    """Install Playwright browsers on first run"""
    try:
        print("📦 Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                      check=True, capture_output=True, timeout=300)
        print("✅ Playwright browsers installed")
    except Exception as e:
        print(f"⚠️  Could not install Playwright: {e}")

def send_telegram(msg):
    """Send a notification message to Telegram"""
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Bot token or chat ID not set!")
        print(f"   BOT_TOKEN: {BOT_TOKEN[:20] if BOT_TOKEN else 'EMPTY'}...")
        print(f"   CHAT_ID: {CHAT_ID}")
        return False
    
    try:
        print(f"📤 Attempting to send Telegram message...")
        api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        }
        print(f"   API: {api[:50]}...")
        print(f"   Chat ID: {CHAT_ID}")
        response = requests.get(api, params=params, timeout=10)
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Message sent successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print(f"❌ Failed to send message!")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_page_hash():
    """Fetch the page and return SHA256 hash of its content"""
    try:
        print(f"🔍 Fetching page: {URL}")
        
        # Try with Playwright for JavaScript rendering
        try:
            from playwright.sync_api import sync_playwright
            print("   Using Playwright (JavaScript rendering)")
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(URL, wait_until="networkidle", timeout=20000)
                content = page.content()
                browser.close()
        except Exception as e:
            print(f"   ⚠️  Playwright failed: {e}, falling back to requests")
            # Fallback to simple requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(URL, headers=headers, timeout=20)
            response.raise_for_status()
            content = response.text
        
        # Take only text to ignore ads/css/js noise
        content = content.strip()
        page_hash = hashlib.sha256(content.encode()).hexdigest()
        print(f"   Page size: {len(content)} bytes")
        print(f"   Hash: {page_hash}")
        return page_hash
    except Exception as e:
        print(f"❌ Error fetching page: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main monitoring loop"""
    print("=" * 50)
    print("🚀 Result Notifier Started!")
    print("=" * 50)
    print(f"📍 Monitoring: {URL}")
    print(f"⏱️  Check interval: {INTERVAL} seconds")
    print(f"🤖 Bot Token: {'✅ Set' if BOT_TOKEN else '❌ NOT SET'}")
    print(f"💬 Chat ID: {'✅ Set' if CHAT_ID else '❌ NOT SET'}")
    print("=" * 50)
    
    old_hash = ""
    error_count = 0
    max_errors = 5
    
    while True:
        try:
            new_hash = get_page_hash()
            
            if new_hash is None:
                error_count += 1
                if error_count >= max_errors:
                    print(f"⚠️  Too many errors ({error_count}). Check your internet or URL.")
                print(f"Retrying in 60 seconds... (Error #{error_count})")
                time.sleep(60)
                continue
            
            error_count = 0  # Reset error counter on success
            
            if old_hash == "":
                print(f"📋 Initial hash captured: {new_hash[:12]}...")
                print(f"   Waiting for changes...")
            elif new_hash != old_hash:
                print(f"🎯 CHANGE DETECTED!")
                print(f"   Old hash: {old_hash[:12]}...")
                print(f"   New hash: {new_hash[:12]}...")
                msg = f"🎉 <b>Result page updated!</b>\n\n🔗 Check now 👉\n{URL}\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                send_telegram(msg)
                print(f"✅ Change detected & notification sent!")
            else:
                print(f"✓ No change - {datetime.now().strftime('%H:%M:%S')}")
            
            old_hash = new_hash
            time.sleep(INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Notifier stopped by user.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Setup Playwright on first run
    setup_playwright()
    
    # Run Flask in a background thread
    flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, debug=False), daemon=True)
    flask_thread.start()
    
    # Run the main monitoring loop in the main thread
    main()
