# import telegram
import telebot
# from PIL import ImageFont
# from PIL import ImageDraw
# from PIL import Image
# from io import BytesIO
from flask import Flask, request
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telebotic.credentials import bot_token, bot_user_name,URL
from telebotic.mastermind import get_response
#import re
from telebot import types

global bot
global TOKEN
TOKEN = bot_token
bot = telebot.TeleBot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, '(placeholder text)')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome2(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.set_webhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)