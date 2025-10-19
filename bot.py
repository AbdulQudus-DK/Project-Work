import telebot
import os
from flask import Flask
import threading

TOKEN = os.getenv("8307131116:AAHGda4orY9XTxyowo19X-5eHO5S3ztJci0")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is alive!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hi! I’m alive on Render!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
