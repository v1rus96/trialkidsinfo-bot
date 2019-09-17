import telebot
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telebotic.credentials import bot_token, bot_user_name,URL
from telebot import types
from models.save import MessageModel

global bot
global TOKEN
TOKEN = bot_token
bot = telebot.TeleBot(token=TOKEN, threaded=False)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None

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


# Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     msg = bot.reply_to(message, """\
# Hi there, I am Example bot.
# What's your name?
# """)
#     bot.register_next_step_handler(msg, process_name_step)

@bot.message_handler(content_types=["text"])
def echo(m):
    if m.text == 'Add kid':
        # keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        # first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        # second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        # keyboardmain.add(first_button, second_button)
        # bot.send_photo(m.chat.id, photo=generateImage(kID=m.text))
        find = MessageModel.get_one(args={'name': '364884'}, filters={'_id': 0})
        if find:
            for c in find:
                c_name = find['name']
                c_age = find['age']
                c_sex = find['sex']
                ct = u'Name: {name}\nAge: {age}\nSex: {sex}'.format(name=c_name, age=c_age, sex=c_sex)
        print (ct)
        msg = bot.reply_to(m, "What is kids ID?")
        return bot.register_next_step_handler(msg, process_name_step)#, reply_markup=keyboardmain)
    # else:
    #     bot.send_message(m.chat.id, "Hey there :)",reply_markup=keyboard())

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        return bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markups = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markups.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markups)
        return bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == 'Male') or (sex == 'Female'):
            user.sex = sex
        else:
            raise Exception()
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.send_photo(chat_id=-1001341610441, photo=generateImage(kID=user.name), reply_markup=keyboardmain)
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex,reply_markup=keyboard())
        MessageModel.save_one({
            'name': user.name,
            'age': user.age,
            'sex': user.sex
        })
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.add('Add kid')
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