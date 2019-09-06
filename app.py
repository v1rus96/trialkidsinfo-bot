import telegram
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])

def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print (update)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    bio = generateImage(kID=text)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='1')],
                   [InlineKeyboardButton(text='Press me', callback_data='2')],
               ])
    bot.send_photo(chat_id, photo=bio, reply_markup=keyboard)

    return 'ok'

def updateImage(bot, update):
  query = update.callback_query
  bot.editMessageMedia(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        media=generateImage(kID=123456))

def generateImage(kID):
    img = Image.new("RGB", (500,550), color="red")
    #x,y = img.size
    #offset = x // 12, y // 5
    img.paste(Image.open("images/background.png"))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('images/Quicksand-Bold.ttf', 48)
    width, height = draw.textsize(kID, fnt)
    draw.text(((500-width)/2,35),kID,(255,255,255),font=fnt)
    #img.save('final.png')
    bio = BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)