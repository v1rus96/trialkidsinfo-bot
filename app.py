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
        self.id = None
        self.brain = None
        self.game = None
        self.experience = None
        self.interest = None

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    print (update)
    bot.process_new_updates([update])
    return 'ok'

def generateImage(kID):
    find = MessageModel.get_one(args={'name': kID}, filters={'_id': 0})
    if find:
        kID = find['kID']
        name = find['name']
        age = find['age']
        sex = find['sex']
        brain = find['brain']
        game = find['game']
        experience = find['experience']
        interest = find['interest']
    img = Image.new("RGB", (500,550), color="red")
    #x,y = img.size
    #offset = x // 12, y // 5
    img.paste(Image.open("images/background.png"))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('images/Quicksand-Bold.ttf', 48)
    fnt1 = ImageFont.truetype('images/Quicksand-Bold.ttf', 18)
    width, height = draw.textsize(kID, fnt)
    draw.text(((500-width)/2,35),"KIDO"+kID,(255,255,255),font=fnt)
    draw.text(60,152,name+", "+age,(255,255,255),font=fnt1)
	# imagettftext($imagecontainer, 35, 0, 135, 84, $foreground, $font, 'KIDO'.$kid); 
	# imagettftext($imagecontainer, 18, 0, 60, 152, $foreground, $font, $kidinfo); 
	# imagettftext($imagecontainer, 22, 0, 329, 195, $foreground, $font, $artscience); 
	# imagettftext($imagecontainer, 22, 0, 329, 248, $foreground, $font, $game); 
	# imagettftext($imagecontainer, 22, 0, 329, 300, $foreground, $font, $experience); 
	# imagettftext($imagecontainer, 22, 0, 329, 352, $foreground, $font, $interest);
	# imagettftext($imagecontainer, 22, 0, 329, 404, $foreground, $font, $estimation);
	# imagettftext($imagecontainer, 22, 0, 329, 457, $foreground, $font, $group);
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
        chat_id = m.chat.id
        MessageModel.update_message(args={'name': '364884'}, set_query={ "$set": {'age': '66'} })
        find = MessageModel.get_one(args={'name': '364884'}, filters={'_id': 0})
        find2 = MessageModel.get_all(args={}, filters={'_id': 0, 'name': 1})
        print(find2)
        if find:
            c_name = find['name']
            c_age = find['age']
            c_sex = find['sex']
            ct = u'Name: {name}\nAge: {age}\nSex: {sex}'.format(name=c_name, age=c_age, sex=c_sex)
        print (ct)
        msg = bot.send_message(chat_id, "What is kids ID?", reply_markup=types.ForceReply())
        return bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    print("name")
    try:
        print("try name")
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, "How old?", reply_markup=types.ForceReply())
        return bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_age_step(message):
    print("age")
    try:
        print("try age")
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.send_message(chat_id,"Age Number pls", reply_markup=types.ForceReply())
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markups = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markups.add('Male', 'Female')
        msg = bot.send_message(chat_id, 'What is your gender', reply_markup=markups)
        return bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_sex_step(message):
    print("sex")
    try:
        print("try sex")
        chat_id = message.chat.id
        message_id = message.message_id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == 'Male') or (sex == 'Female'):
            user.sex = sex
            msg = bot.send_message(chat_id, "kids ID?", reply_markup=types.ForceReply())
            return bot.register_next_step_handler(msg, process_id_step)
        else:
            raise Exception()
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_id_step(message):
    try:
        chat_id = message.chat.id
        id = message.text
        user = user_dict[chat_id]
        user.id = id
        markups = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markups.add('Art', 'Science')
        msg = bot.send_message(chat_id, 'What kids like?', reply_markup=markups)
        return bot.register_next_step_handler(msg, process_brain_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_brain_step(message):
    try:
        chat_id = message.chat.id
        message_id = message.message_id
        brain = message.text
        user = user_dict[chat_id]
        if (brain == 'Art') or (brain == 'Science'):
            user.brain = brain
            markups = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True, resize_keyboard=True)
            markups.add('Minecraft', 'Roblox', 'Both')
            msg = bot.send_message(chat_id, "Game?", reply_markup=markups)
            return bot.register_next_step_handler(msg, process_game_step)
        else:
            raise Exception()
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_game_step(message):
    try:
        chat_id = message.chat.id
        message_id = message.message_id
        game = message.text
        user = user_dict[chat_id]
        if (game == 'Minecraft') or (game == 'Roblox') or (game == 'Both'):
            user.game = game
            msg = bot.send_message(chat_id, "Experience?", reply_markup=types.ForceReply())
            return bot.register_next_step_handler(msg, process_experience_step)
        else:
            raise Exception()
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_experience_step(message):
    try:
        chat_id = message.chat.id
        experience = message.text
        user = user_dict[chat_id]
        user.experience = experience
        markups = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markups.add('Mobile', 'Robotics')
        msg = bot.send_message(chat_id, 'What kids like?', reply_markup=markups)
        return bot.register_next_step_handler(msg, process_interest_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_interest_step(message):
    try:
        chat_id = message.chat.id
        message_id = message.message_id
        interest = message.text
        user = user_dict[chat_id]
        if (interest == 'Mobile') or (interest == 'Robotics'):
            user.interest = interest
        else:
            raise Exception()
        MessageModel.save_one({
            'chat_id': -1001341610441,
            'message_id': 0,
            'kID': user.id,
            'name': user.name,
            'age': user.age,
            'sex': user.sex,
            'brain': user.brain,
            'game': user.game,
            'experience': user.experience,
            'interest': user.interest
        })
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="Button", switch_inline_query_current_chat="Check")
        second_button = types.InlineKeyboardButton(text="Button", callback_data="second")
        third_button = types.InlineKeyboardButton(text="Button", callback_data="third")
        keyboardmain.add(first_button, second_button,third_button)
        sent = bot.send_photo(chat_id=-1001341610441, photo=generateImage(kID=user.id), reply_markup=keyboardmain)
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex,reply_markup=keyboard())
        MessageModel.update_message(args={'kID': user.id}, set_query={ "$set": {'message_id': sent.message_id} })
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.add('Add kid')
	return markup 

@bot.inline_handler(lambda query: len(query.query) is 0)
def empty_query(query):
    find = MessageModel.get_all(args={}, filters={'_id': 0, 'name': 1})
    print(find)
    hint = "Введите ровно 2 числа и получите результат!"
    results_array = []
    try:
        for id in find:
            results_array.append(types.InlineQueryResultArticle(
                    id=id['name'],
                    title=id['name'],
                    description=hint,
                    input_message_content=types.InputTextMessageContent(
                    message_text="Эх, зря я не ввёл 2 числа :(")
            ))
        bot.answer_inline_query(query.id, results_array)
    except Exception as e:
        print(e)

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    digits_pattern = re.compile(r'^[0-9]+ estimate', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, query.query)
        num1, num2 = matches.group().split()
    except AttributeError as ex:
        return
    
    tasks = ["Mono","Square","Penta"]
    results_array = []
    try:
        for i, val in enumerate(tasks): 
            print(val)
            try:
                results_array.append(types.InlineQueryResultArticle(
                        id=val, title=val,
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

@bot.chosen_inline_handler(lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    kID, estimate = chosen_inline_result.query.split()
    find = MessageModel.get_one(args={'name': str(kID)}, filters={'_id': 0})
    if find:
        chat_id = find['chat_id']
        message_id = find['message_id']
        name = find['name']
        ct = u'Name: {name}\nAge: {age}\nSex: {sex}'.format(name=chat_id, age=message_id, sex=name)
    print (ct)
    MessageModel.update_message(args={'name': str(kID)}, set_query={ "$set": {'name': chosen_inline_result.result_id} })
    bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID=chosen_inline_result.result_id)),
                            chat_id=chat_id,
                            message_id=message_id)
    print(chosen_inline_result.query + chosen_inline_result.result_id)


@bot.callback_query_handler(lambda query: True)
def process_callback(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    print(query.message.message_id)
    # if query.data == "first":
    #     keyboardmain = types.InlineKeyboardMarkup(row_width=3)
    #     first_button = types.InlineKeyboardButton(text="🔘 Button", callback_data="first")
    #     second_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="second")
    #     third_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="third")
    #     keyboardmain.add(first_button, second_button,third_button)
    #     bot.answer_callback_query(callback_query_id=query.id)
    #     bot.edit_message_reply_markup(
    #                         chat_id=chat_id,
    #                         message_id=message_id,
    #                         reply_markup=keyboardmain)
    if query.data == "second":
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
    app.run()