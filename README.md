# 📱 Result Notifier Bot

Automatically get **Telegram notifications with sound** when your result page changes. Runs 24/7 on the cloud for **FREE** ✨

## ⚡ Features

- ✅ Automatic page monitoring every 5 minutes (configurable)
- ✅ Instant Telegram notifications with sound
- ✅ Runs 24/7 on Render's free tier
- ✅ SHA256 hashing to detect even minor changes
- ✅ Error handling & automatic retries
- ✅ Beautiful formatted messages with timestamps
- ✅ Health check endpoint (keeps service alive)
- ✅ 100% FREE - no credit card needed

---

## 🧱 Step 1: Create a Telegram Bot

1. **Open Telegram** and search for **@BotFather**
2. Send `/start` then `/newbot`
3. Give it a name (e.g., "Result Notifier Bot")
4. Give it a username (e.g., `ResultNotifyBot`)
5. **BotFather** will give you a **TOKEN** that looks like:
   ```
   123456789:ABCDefGhijKLMnoPQRstuVWxyz
   ```
6. **Save this token safely** ✅

---

## 🧾 Step 2: Get Your Chat ID

1. In Telegram, search for **@userinfobot**
2. Send `/start`
3. It will show:
   ```
   Your chat ID: 987654321
   ```
4. **Copy this number** ✅

---

## 🚀 Step 3: Deploy on Render (Easy Mode)

### Option A: Using GitHub (Recommended)

1. **Fork this repository** (click "Fork" button on GitHub)
   
2. Go to [render.com](https://render.com)
   - Sign up with GitHub
   
3. Click **"New +"** → **"Web Service"**
   
4. Select this repository and deploy
   
5. When asked for "Start Command", enter:
   ```
   pip install -r requirements.txt && python main.py
   ```

6. In Render dashboard, go to **Settings** → **Environment Variables** and add:
   ```
   RESULT_URL = https://your-result-page.edu/results
   BOT_TOKEN = 123456789:ABCDefGhijKLMnoPQRstuVWxyz
   CHAT_ID = 987654321
   CHECK_INTERVAL = 300
   ```

7. Click **"Deploy"** ✨

---

## 🔋 Step 4: Keep Service Alive (FREE!)

Render's free tier spins down services after 15 minutes of inactivity. Here's how to prevent that:

### Option A: GitHub Actions (Easiest - Built-in!)

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `RENDER_SERVICE_NAME`
4. Value: Your Render service name (from the URL, e.g., if your URL is `result-notifier.onrender.com`, use `result-notifier`)
5. Click **"Add secret"** ✅

**The GitHub Actions workflow (in `.github/workflows/keep-alive.yml`) will automatically:**
- ✅ Run every 14 minutes
- ✅ Ping your service to keep it awake
- ✅ Cost: **FREE** (GitHub gives 2000 free Actions minutes/month)

### Option B: Manual Cron Service

If you prefer an external service like `cron-job.org`:
```bash
curl https://your-service.onrender.com/health
```
Run this every 10-15 minutes to keep the service alive.

---

## 📁 File Structure

```
notifyer/
├── main.py                           # Main script (monitoring + Flask server)
├── requirements.txt                  # Python dependencies
├── Procfile                          # Render deployment config
├── runtime.txt                       # Python version
├── keep_alive.py                     # Manual keep-alive script
├── .env.example                      # Config template
├── .gitignore                        # Ignore sensitive files
├── .github/workflows/keep-alive.yml  # GitHub Actions workflow
└── README.md                         # This file
```

---

## ⚙️ Configuration

Edit **Environment Variables** in Render:

| Variable | Example | Purpose |
|----------|---------|---------|
| `RESULT_URL` | `https://college.edu/results` | Your result page URL |
| `BOT_TOKEN` | `123456789:ABCDefGhijKLM...` | Telegram bot token |
| `CHAT_ID` | `987654321` | Your Telegram chat ID |
| `CHECK_INTERVAL` | `300` | Seconds between checks (300 = 5 min) |
| `PORT` | `5000` | (Auto-set) Flask server port |

**Quick intervals:**
- `60` = Check every 1 minute
- `120` = Check every 2 minutes
- `300` = Check every 5 minutes (default)
- `900` = Check every 15 minutes

---

## 📱 What You'll Get

Once the result page changes, you'll receive:

```
🎉 Result page updated!

🔗 Check now 👉
https://your-result-page.edu/results

⏰ 2025-11-03 14:32:45
```

✨ **With sound notification!**

---

## 🔧 Troubleshooting

### ❌ Service keeps spinning down

- Make sure GitHub Actions secret is set correctly
- Check that your secret name matches your service name
- GitHub Actions workflow runs every 14 minutes automatically

### ❌ "No change detected" (but page actually changed)

- The page might have **JavaScript loading** content
- Try increasing `CHECK_INTERVAL` (ads/tracking scripts update often)
- Check if the page requires **authentication**

### ❌ Not getting Telegram messages

- Verify `BOT_TOKEN` is correct (no spaces)
- Verify `CHAT_ID` is correct
- Check Render logs for errors
- Make sure you sent `/start` to the bot first

### ❌ Script crashes on Render

- Check **Logs** in Render dashboard
- Verify environment variables are set correctly
- Ensure your `RESULT_URL` is valid

### ✅ Check if running

In Render dashboard:
- Go to **Logs**
- You should see: `✓ No change - HH:MM:SS` messages
- Also check: `Listening on 0.0.0.0:5000` (Flask running)

---

## 🎯 Advanced: Monitor Multiple Pages

Edit `main.py` to monitor multiple URLs:

```python
URLS = [
    "https://college1.edu/results",
    "https://college2.edu/results",
]

# Then in main loop:
for url in URLS:
    # Check each URL
    # Send separate notifications
```

---

## 💡 Pro Tips

- **Faster detection?** Set `CHECK_INTERVAL = 120` (2 minutes)
- **Quieter logs?** Remove `print()` statements in main.py
- **Custom message?** Edit the message in `send_telegram()` function
- **Multiple result pages?** Deploy this multiple times (different repos)
- **Test locally?** Run `python main.py` with `.env` file

---

## ⚠️ Important Notes

- **NEVER** commit `.env` to GitHub (it's in `.gitignore`)
- Only add credentials via Render's **Environment Variables** dashboard
- GitHub Actions workflow keeps your service alive for free
- Render's free tier is perfect for this use case
- Flask server runs on port 5000 (auto-detected by Render)

---

## 📞 Support

If something breaks:

1. Check **Render logs** for error messages
2. Verify all **environment variables** are set
3. Test with a simple URL first (like `https://example.com`)
4. Make sure your internet connection is stable
5. Check GitHub Actions workflow status

---

## 📜 License

This project is open source and free to use.

---

**Happy notifying! 🚀**

