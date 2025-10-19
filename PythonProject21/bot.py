
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # We'll set this on Render
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hi! I’m alive on Render!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()
