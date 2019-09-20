import telebot
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from io import BytesIO
from flask import Flask, request
from telebotic.credentials import bot_token, bot_user_name,URL
from telebot import types
from models.save import MessageModel
import re

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
        MessageModel.update_message(args={'name': '364884'}, set_query={ "$set": {'age': '66'} })
        find = MessageModel.get_one(args={'name': '364884'}, filters={'_id': 0})
        if find:
            c_name = find['name']
            c_age = find['age']
            c_sex = find['sex']
            ct = u'Name: {name}\nAge: {age}\nSex: {sex}'.format(name=c_name, age=c_age, sex=c_sex)
        print (ct)
        msg = bot.reply_to(m, "What is kids ID?")
        return bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        return bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

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
        bot.reply_to(message, 'oooops' + e)

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == 'Male') or (sex == 'Female'):
            user.sex = sex
        else:
            raise Exception()
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="second")
        third_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="third")
        keyboardmain.add(first_button, second_button,third_button)
        bot.send_photo(chat_id=-1001341610441, photo=generateImage(kID=user.name), reply_markup=keyboardmain)
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex,reply_markup=keyboard())
        MessageModel.save_one({
            'name': user.name,
            'age': user.age,
            'sex': user.sex
        })
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.add('Add kid')
	return markup 

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    digits_pattern = re.compile(r'^[0-9]+ estimate', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, query.query)
    except AttributeError as ex:
        return print("No match")
    num1, num2 = matches.group().split()
    tasks = ["Mono","Square","Penta"]
    results_array = []
    try:
        for i, val in enumerate(tasks): 
            print(val)
            try:
                results_array.append(types.InlineQueryResultArticle(
                        id=str(i+1), title=val,
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description="Результат: {!s}".format(val),
                        input_message_content=types.InputTextMessageContent(
                        message_text="{!s} + {!s}".format(num1, num2))
                ))
            except Exception as e:
                print(e)
        bot.answer_inline_query(query.id, results_array)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))

@bot.callback_query_handler(lambda query: True)
def process_callback(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    if query.data == "first":
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="🔘 Button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="second")
        third_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="third")
        keyboardmain.add(first_button, second_button,third_button)
        bot.answer_callback_query(callback_query_id=query.id)
        bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=keyboardmain)
    elif query.data == "second":
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="🔘 Button", callback_data="second")
        third_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="third")
        keyboardmain.add(first_button, second_button,third_button)
        bot.answer_callback_query(callback_query_id=query.id)
        bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=keyboardmain)
    elif query.data == "third":
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="second")
        third_button = types.InlineKeyboardButton(text="🔘 Button", callback_data="third")
        keyboardmain.add(first_button, second_button,third_button)
        bot.answer_callback_query(callback_query_id=query.id)
        bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=keyboardmain)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

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