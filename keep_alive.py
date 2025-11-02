#!/usr/bin/env python3
"""
Keep-Alive Script for Render Web Service
Run this periodically via an external cron service (like GitHub Actions)
to prevent Render's free tier from spinning down your service
"""

import requests
import os
from datetime import datetime

# Get your Render service URL
SERVICE_URL = os.getenv("SERVICE_URL", "https://your-service.onrender.com")

def ping_service():
    """Ping the service to keep it awake"""
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=10)
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"{status} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Service responded with {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {e}")
        return False

if __name__ == "__main__":
    ping_service()
