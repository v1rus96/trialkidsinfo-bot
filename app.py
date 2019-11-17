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
from datetime import datetime, time
import cv2
import sys
import numpy as np
import urllib
from menu import Const

global bot
global TOKEN
TOKEN = bot_token
bot = telebot.TeleBot(token=TOKEN, threaded=False)

user_dict = {}

def isNowInTimePeriod(startTime, endTime):
    nowTime = datetime.now().time()
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

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
        self.order = 0
        self.estimation = None
        self.group = None
        self.typing = 0
        self.communication = 0
        self.response = 0
        self.energy = 0
        self.date = None
        self.photo = None
        self.session = None
        # User.counter += 1

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    print (update)
    bot.process_new_updates([update])
    return 'ok'


def generateImage(kID):
    find = MessageModel.get_one(args={'kID': kID}, filters={'_id': 0})
    kID = find['kID']
    name = find['name']
    age = find['age']
    sex = find['sex']
    brain = find['brain']
    game = find['game']
    experience = find['experience']
    interest = find['interest']
    order = find['order']
    estimation = find['estimation']
    group = find['group']
    url = find['photo']
    print(find)
    img = Image.new("RGB", (500,583), color="red")
    #x,y = img.size
    #offset = x // 12, y // 5
    background = Image.open("images/background.png")
    img.paste(background)
    genderMale = Image.open("images/male.png")
    genderFemale = Image.open("images/female.png")
    imga = detect_face(url)
    photoLoad = Image.open(BytesIO(imga))
    if sex == 'Male':
        img.paste(genderMale,(87,37), genderMale)
    else:
        img.paste(genderFemale,(87,37), genderFemale)
    img.paste(photoLoad, (49,149))
    draw = ImageDraw.Draw(img)#s
    fnt = ImageFont.truetype('images/Quicksand-Bold.ttf', 25)
    fnt1 = ImageFont.truetype('images/Quicksand-Bold.ttf', 30)
    fnt2 = ImageFont.truetype('images/Quicksand-Bold.ttf', 35)
    #width, height = draw.textsize("KIDO"+kID, fnt)
    draw.text((63,92),"KIDO"+kID,(255,255,255),font=fnt)#(500-width)/2
    draw.text((355,27),age,(255,255,255),font=fnt1)
    draw.text((121,27),name,(255,255,255),font=fnt1)
    draw.text((313,96),brain,(255,255,255),font=fnt1)
    draw.text((313,149),game,(255,255,255),font=fnt1)
    draw.text((313,201),experience,(255,255,255),font=fnt1)
    draw.text((313,253),interest,(255,255,255),font=fnt1)
    draw.text((313,306),estimation,(255,255,255),font=fnt1)
    draw.text((313,358),group,(255,255,255),font=fnt1)
    draw.text((24,9),str(order),(255,255,255),font=fnt2)
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
def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image
def detect_face(url):
    image = url_to_image(url)
    # imagePath = str(bot.get_file(message.photo[-1].file_id).file_path)
    # imagePath = downloaded_file # + str(bot.get_file(message.photo[2].file_id).file_path)
    cascPath = "haarcascade_frontalface_default.xml"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    # Read the image
    # image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray, 
        scaleFactor=1.1,
        minNeighbors=5, 
        minSize=(30, 30))

    print("Found {0} faces!".format(len(faces)))
    for (x, y, w, h) in faces:
        faceimg = image[y-120:y+h+120, x-52:x+w+52]
        lastimg = cv2.resize(faceimg, (154, 196))
        final = cv2.imencode('.jpg', lastimg)[1].tostring()
    return final

@bot.message_handler(content_types=["text"])
def echo(m):
    chat_id = m.chat.id
    if m.text == 'Add kid':
        msg = bot.send_message(chat_id, "What is kids ID?", reply_markup=types.ForceReply())
        return bot.register_next_step_handler(msg, process_name_step)
    elif m.text == 'Pin':
        pM = bot.send_message(-1001341610441, "What is kids ID?")
        bot.pin_chat_message(-1001341610441, pM.message_id)

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
        msg = bot.send_message(chat_id, 'Photo?', reply_markup=markups)
        return bot.register_next_step_handler(msg, process_photo_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_photo_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.photo = "https://api.telegram.org/file/bot880055204:AAGeIliCzZvmW6mxtUlT1N799tpwu4znpf8/"+str(bot.get_file(message.photo[-1].file_id).file_path)
            # bot.send_photo(chat_id=-1001341610441, photo=final)#djfsndkf
        print(user.photo)
        msg = bot.send_message(chat_id, 'What kids like?')
        return bot.register_next_step_handler(msg, process_interest_step)
    except Exception as e:
        bot.reply_to(message, 'oooops' + e)

def process_interest_step(message):
    try:
        chat_id = message.chat.id
        interest = message.text
        user = user_dict[chat_id]
        if (interest == 'Mobile') or (interest == 'Robotics'):
            user.interest = interest
        else:
            raise Exception()
        if int(user.age) <= 5: 
            estimation = "Square" 
            group = "Curious" 
        elif int(user.age) == 6: 
            estimation = "Hexa" 
            group = "Curious"
        elif int(user.age) == 7: 
            estimation = "Hepta"
            group = "Curious"
        elif int(user.age) == 8: 
            estimation = "Range"
            group = "Curious"
        elif int(user.age) == 9: 
            estimation = "3Square"
            group = "Explorer"
        elif int(user.age) == 10: 
            estimation = "Mono"
            group = "Explorer"
        elif int(user.age) == 11: 
            estimation = "Multi Color"
            group = "Discoverer"
        elif int(user.age) == 12: 
            estimation = "GoTo"
            group = "Discoverer"
        elif int(user.age) == 13: 
            estimation = "GoTo Rand"
            group = "Discoverer"
        elif int(user.age) >= 14: 
            estimation = "Picaso"
            group = "Inventor"
        user.estimation = estimation
        user.group = group
        session1 = isNowInTimePeriod(time(9,45), time(11,45))
        session2 = isNowInTimePeriod(time(11,45), time(13,45))
        session3 = isNowInTimePeriod(time(13,45), time(16,45))
        session4 = isNowInTimePeriod(time(16,45), time(5,45))
        if session1:
            user.session = 1
        elif session2:
            user.session = 2
        elif session3:
            user.session = 3
        elif session4:
            user.session = 4
        user.date = str(datetime.now().date())
        find = MessageModel.get_all_count(args={'date': user.date, 'session': user.session}, filters={'_id': 0, 'name': 1})
        print(find)
        user.order = find+1
        MessageModel.save_one({
            'chat_id': -1001341610441,
            'message_id': 0,
            'order': user.order,
            'kID': user.id,
            'name': user.name,
            'age': user.age,
            'sex': user.sex,
            'brain': user.brain,
            'game': user.game,
            'experience': user.experience,
            'interest': user.interest,
            'estimation': user.estimation,
            'group': user.group,
            'typing': user.typing,
            'communication': user.communication,
            'response': user.response,
            'energy': user.energy,
            'date': user.date,
            'photo': user.photo,
            'session': user.session
        })
        keyboardmain = types.InlineKeyboardMarkup(row_width=3)
        first_button = types.InlineKeyboardButton(text="Button", switch_inline_query_current_chat=user.id + " order")
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
    session1 = isNowInTimePeriod(time(9,45), time(11,45))
    session2 = isNowInTimePeriod(time(11,45), time(13,45))
    session3 = isNowInTimePeriod(time(13,45), time(16,45))
    session4 = isNowInTimePeriod(time(16,45), time(5,45))
    if session1:
        session = 1
    elif session2:
        session = 2
    elif session3:
        session = 3
    elif session4:
        session = 4
    date = str(datetime.now().date())
    find = MessageModel.get_all(args={'date': date, 'session': session}, filters={'_id': 0, 'name': 1})
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
        # for id in find:
        #     results_array.append(types.InlineQueryResultPhoto(
        #             id=id['kID'],
        #             photo_url=id['photo'],
        #             thumb_url=id['photo']
        #     ))###
        bot.answer_inline_query(query.id, results_array)
    except Exception as e:
        print(e)

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    if (query.query.find('estimate') != -1): 
        digits_pattern = re.compile(r'^[0-9]+ estimate', re.MULTILINE)
        try:
            matches = re.match(digits_pattern, query.query)
            num1, num2 = matches.group().split()
        except AttributeError as ex:
            return print(ex)
        
        tasks = ["Square","Penta","Hexa","Maybe"]
        results_array = []
        try:
            for val in tasks: #for i, val in enumerate(tasks): 
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
    elif (query.query.find('order') != -1):
        session1 = isNowInTimePeriod(time(9,45), time(11,45))
        session2 = isNowInTimePeriod(time(11,45), time(13,45))
        session3 = isNowInTimePeriod(time(13,45), time(16,45))
        session4 = isNowInTimePeriod(time(16,45), time(5,45))
        if session1:
            session = 1
        elif session2:
            session = 2
        elif session3:
            session = 3
        elif session4:
            session = 4
        date = str(datetime.now().date())
        find = MessageModel.get_all_count(args={'date': date, 'session': session}, filters={'_id': 0, 'name': 1})
        digits_pattern = re.compile(r'^[0-9]+ order', re.MULTILINE)
        try:
            matches = re.match(digits_pattern, query.query)
            num1, num2 = matches.group().split()
            print(num1)
        except AttributeError as ex:
            return print(ex)
        results=[]
        try:
            print("try1")
            for i in range(1, find+1):#for i, val in enumerate(tasks): 
                try:
                    print("try2")
                    results.append(types.InlineQueryResultArticle(
                            id=i, title=i,
                            description="Choose order",
                            input_message_content=types.InputTextMessageContent(
                            message_text="{!s} + {!s}".format(num1, num2))
                    ))
                except Exception as e:
                    print(e)
            bot.answer_inline_query(query.id, results, cache_time=0)
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
    

@bot.chosen_inline_handler(lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    kID, action = chosen_inline_result.query.split()
    order = chosen_inline_result.result_id
    find = MessageModel.get_one(args={'kID': str(kID)}, filters={'_id': 0})
    if find:
        chat_id = find['chat_id']
        message_id = find['message_id']
    if action == 'estimate':
        MessageModel.update_message(args={'kID': str(kID)}, set_query={ "$set": {'estimation': chosen_inline_result.result_id} })
        bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID=kID)),
                                chat_id=chat_id,
                                message_id=message_id)
    elif action == 'order':
        session1 = isNowInTimePeriod(time(9,45), time(11,45))
        session2 = isNowInTimePeriod(time(11,45), time(13,45))
        session3 = isNowInTimePeriod(time(13,45), time(16,45))
        session4 = isNowInTimePeriod(time(16,45), time(5,45))
        if session1:
            session = 1
        elif session2:
            session = 2
        elif session3:
            session = 3
        elif session4:
            session = 4
        date = str(datetime.now().date())
        find2 = MessageModel.get_one(args={'order': int(order), 'session': session, 'date': date}, filters={'_id': 0})
        if find2:
            message_idOrder = find2['message_id']
            print(message_idOrder)
            kIDOrder = find2['kID']
            print(kIDOrder)
            orderCurrent = find['order']
            MessageModel.update_message(args={'kID': str(kID)}, set_query={ "$set": {'order': int(chosen_inline_result.result_id), 'message_id': message_idOrder} })
            bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID=kID)),
                                    chat_id=chat_id,
                                    message_id=message_idOrder)
            MessageModel.update_message(args={'kID': str(kIDOrder)}, set_query={ "$set": {'order': int(orderCurrent), 'message_id': message_id} })
            bot.edit_message_media(media=types.InputMediaPhoto(generateImage(kID=kIDOrder)),
                                    chat_id=chat_id,
                                    message_id=message_id)
        else:
            print("Didnt work")
        
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
    for cat in ["T","C","R","E"]:
        for num in range(1,4):
            callback = cat+str(num)
            if query.data == "second" or query.data == callback:
                keyboardmain = types.InlineKeyboardMarkup(row_width=4)
                catIcons = ["T","C","R","E"]
                catVal = [3,2,3,2]
                list = ["✳","⏺","🅾"]
                icons = ["✳","⏺","🅾"]
                for category in range(4):
                    print(catIcons[category])
                    for num in range(1,4):
                        if callback == catIcons[category]+str(num):
                            catVal[category] = num
                    for index in range(len(list)):
                        if catVal[category] == index+1:
                            list[index] = "☑"
                            print(list[index])
                            # print(index+1)
                        else:
                            list[index] = icons[index]
                            print(list[index])
                    # print(index+1)
                types.InlineKeyboardButton(text="⚪ Button", callback_data="first")
                first_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="first")
                second_button = types.InlineKeyboardButton(text="🔘 Button", callback_data="second")
                third_button = types.InlineKeyboardButton(text="⚪ Button", callback_data="third")
                keyboardmain.add(first_button, second_button,third_button)
                bot.answer_callback_query(callback_query_id=query.id)
                bot.edit_message_reply_markup(
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=keyboardmain)
    if query.data == "third":
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