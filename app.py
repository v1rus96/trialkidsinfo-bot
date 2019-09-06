import telegram
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])

def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    img = Image.new("RGB", (500,550), color="red")
    #x,y = img.size
    #offset = x // 12, y // 5
    img.paste(Image.open("images/background.png"))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('images/Quicksand-Bold.ttf', 48)
    width, height = fnt.textsize(text)
    draw.text(((500-width)/2,35),text,(255,255,255),font=fnt)
    #img.save('final.png')
    bio = BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    bot.send_photo(chat_id, photo=bio)

    return 'ok'

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