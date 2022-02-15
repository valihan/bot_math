#!/usr/bin/python
import telebot
import config
import constant
from db import cl_db
from class_math import cl_math

go_bot = telebot.TeleBot(config.API_TOKEN)
go_db = cl_db("bot_math.db") 
go_math = cl_math()

gv_cmd = ""
gv_equation  = ""

# Handle '/start'
@go_bot.message_handler(commands=['start'])
def start(message):
    if(not go_db.user_exists(message.from_user.id)):
        go_db.add_user(message.from_user.id, message.from_user.first_name)

    print("start:"+message.from_user.first_name)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(go_math.gc_cmd_linear_equation, go_math.gc_cmd_quadratic_equation)
    go_bot.reply_to(message, constant.gc_welcome)#, reply_markup=keyboard)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@go_bot.message_handler(func=lambda message: True)
def echo_message(message):
    lv_text = message.text.lower()
    try:
        print(message.from_user.first_name,lv_text)
        lt_text = lv_text.split(';')
        # lv_graphic=go_math.graph(lt_text[0], lt_text[1], lt_text[2])
        # go_bot.reply_to( message, lv_graphic )
        #go_bot.send_photo(message.from_user.id, open(go_math.graph(lt_text[0], lt_text[1], lt_text[2]), 'rb'));
        lv_x = go_math.main( "", lt_text[0], lt_text[1], lt_text[2])
        lv_response = "Уравнение " + lt_text[0] + "\n от " + lt_text[1] + " до " + lt_text[2] + "\n Найден ответ:" + str(lv_x)
        go_bot.reply_to( message, lv_response )
    except:
        go_bot.reply_to( message, constant.gc_error )

go_bot.infinity_polling()
