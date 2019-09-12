import telebot
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telebotic.credentials import bot_token, bot_user_name,URL
from telebot import types

global bot
global TOKEN
TOKEN = bot_token
bot = telebot.TeleBot(token=TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    print (update)
    bot.process_new_updates([update])
    return 'ok'

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

@bot.message_handler(commands=['start'])
def start(message):
  sent = bot.send_message(message.chat.id, 'Please describe your problem.')
  bot.register_next_step_handler(sent, hello)

def hello(message):
    open('problem.txt', 'w').write(message.chat.id + ' | ' + message.text + '||')
    bot.send_message(message.chat.id, 'Thank you!')

@bot.message_handler(content_types=["text"])
def echo(m):
    if m.text == 'Add kid':
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.send_photo(m.chat.id, photo=generateImage(kID=m.text), reply_markup=keyboardmain)
    else:
        bot.send_message(m.chat.id, "Hey there :)",reply_markup=keyboard())

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	btn1 = types.KeyboardButton('Add kid')
	markup.add(btn1)
	return markup 

@bot.callback_query_handler(lambda query: True)
def process_callback(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    if query.data == "first":
        bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID='FIRST')),
                            chat_id=chat_id,
                            message_id=message_id)
    elif query.data == "second":
        bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID='SECOND')),
                            chat_id=chat_id,
                            message_id=message_id)


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