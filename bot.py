import os
from flask import Flask, request
import telebot

# ✅ Get your Telegram bot token securely from environment variables
TOKEN = os.getenv("TOKEN")  # or replace with your actual token string e.g. "123456:ABC..."
if not TOKEN:
    raise ValueError("TOKEN not set. Please set it as an environment variable.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ✅ Route to receive updates from Telegram
@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# ✅ Route to set webhook
@app.route("/")
def set_webhook():
    webhook_url = f"https://telegrambot-zexm.onrender.com/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
