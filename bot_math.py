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

@go_bot.message_handler(commands=['debug1'])
def debug(message):
        go_bot.reply_to(message, go_math.switch_debug())
@go_bot.message_handler(commands=['debug9'])
def debug(message):
        go_bot.reply_to(message, go_math.switch_debug9())


@go_bot.message_handler(func=lambda message: True)
def main(message):
    lv_text = message.text.lower()
    try:
        lt_text = lv_text.split(';')
        if lv_text.find("=") > 0:
            print("=")
            lv_x = go_math.main( "", lt_text[0], lt_text[1], lt_text[2])
            lv_response = "Уравнение " + lt_text[0] + "\n от " + lt_text[1] + " до " + lt_text[2] + "\n Найден ответ:" + str(lv_x)
            go_bot.reply_to( message, lv_response )
            return
        else:
            print("y=")
            lv_tab=go_math.tab(lt_text[0], lt_text[1], lt_text[2])
            go_bot.reply_to( message, lv_tab )
            lv_graphic=go_math.graph(lt_text[0], lt_text[1], lt_text[2])
            go_bot.send_photo(message.from_user.id, open(go_math.graph(lt_text[0], lt_text[1], lt_text[2]), 'rb'))
            return
    except:
         go_bot.reply_to( message, constant.gc_error )

go_bot.infinity_polling()
