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
gv_equation = ""


@go_bot.message_handler(commands=['start'])
def start(message):
    if(not go_db.user_exists(message.from_user.id)):
        go_db.add_user(message.from_user.id, message.from_user.first_name)
    print("start:" + message.from_user.first_name)
    go_bot.reply_to(message, constant.gc_welcome)


@go_bot.message_handler(commands=['debug1'])
def debug(message):
        go_bot.reply_to(message, go_math.switch_debug())


@go_bot.message_handler(commands=['debug9'])
def debug(message):
        go_bot.reply_to(message, go_math.switch_debug9())


# main
@go_bot.message_handler(func=lambda message: True)
def main(message):
    lv_text = message.text.lower()
    print(message.from_user.first_name)
    try:
        lt_text = lv_text.split(';')
        if lv_text.find("=") > 0:
            print(constant.gc_msg_equation, lv_text)
            lv_x = go_math.main("", lt_text[0], lt_text[1], lt_text[2])
            lv_response = constant.gc_msg_equation + lt_text[0] + "\n" + constant.gc_msg_range + lt_text[1] + ".." + lt_text[2] + "\n" + constant.gc_msg_response + str(lv_x)
            go_bot.reply_to(message, lv_response)
            return
        else:
            # Если нет =, то вывести таблицу значений и построить график
            print(constant.gc_msg_graphic, lv_text)
            lv_tab = go_math.tab(lt_text[0], lt_text[1], lt_text[2])
            go_bot.reply_to(message, lv_tab)
            lv_graphic = go_math.graph(lt_text[0], lt_text[1], lt_text[2])
            go_bot.send_photo(message.from_user.id, open(lv_graphic, 'rb'))
            return
    except:
        go_bot.reply_to(message, constant.gc_error)

go_bot.infinity_polling()
