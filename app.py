import telegram
import telebot
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telebotic.credentials import bot_token, bot_user_name,URL
from telebotic.mastermind import get_response
import re
from telebot import types

global bot
global TOKEN
TOKEN = bot_token
bot = telebot.TeleBot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
    second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, "testing kb", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == "mainmenu":

        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="menu",reply_markup=keyboardmain)

    if call.data == "first":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="1t", callback_data="1")
        rele2 = types.InlineKeyboardButton(text="2t", callback_data="2")
        rele3 = types.InlineKeyboardButton(text="3t", callback_data="3")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1, rele2, rele3, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

    elif call.data == "second":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

    elif call.data == "1" or call.data == "2" or call.data == "3":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
        keyboard3 = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
        keyboard3.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="last layer",reply_markup=keyboard3)

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