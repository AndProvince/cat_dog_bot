# -*- coding: utf-8 -*-
# Cat and dog bot
TOKEN = ''

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import re
import logging
from random import choice

'''
Logging mode
'''
logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

updater = None

'''
Start-bot message
Приветствие бота при старте
'''
def start(update, context):
    s = "Welcome and be ready! Your life has now changed forever."
    update.message.reply_text(s)
    update.message.reply_text(start_menu_message(),
                              reply_markup=start_menu_keyboard())

'''
Choise-menu
Подстказка меню для следующей фото
'''
def show_menu(update, context):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id,
        main_menu_message(),
        reply_markup=main_menu_keyboard())

'''
Page url with dog picture
Получение страницы с картинкой собаки
'''
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

'''
Dog picture url
Получаем ссылку на картинку с собакой
'''
def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

'''
Post dog picture in chat
Направление в чат сообщения с картинкой собаки
'''
def dog(update, context):
    url = get_image_url()
    chat_id = update.effective_message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    if context.user_data[menu]:
        show_menu(update, context)

'''
Cat picture url
Получаем ссылку на картинку с кошкой
'''
def get_cat_url():
    return requests.get('http://aws.random.cat/meow').json()['file']

'''
Post cat picture in chat
Направление в чат сообщения с картинкой кошкой
'''
def cat(update, context):
    url = get_cat_url()
    chat_id = update.effective_message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    if context.user_data[menu]:
        show_menu(update, context)

'''
Post dog or cat picture in chat. Answer for key (/dog or /cat) and any message.
Направление в чат сообщения с картинкой собаки или кошки в ответ на ключи (/dog или /cat) или другие сообещиня
'''
def handle_text(update, context):
    message = update.message.text
    if "/dog" in message:
        dog(update, context)
    elif "/cat" in message:
        cat(update, context)
    else:
        if choice([True, False]):
            dog(update, context)
        else:
            cat(update, context)

'''
Activate choise menu
Активация показа меню выбора следующей картинки
'''
def main_m_y(update, context):
    context.user_data[menu] = True
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id,
        "Choise menu actiavated")
    show_menu(update, context)

'''
Deactivate choise menu
Деактивация показа меню выбора следующей картинки
'''
def main_m_n(update, context):
    context.user_data[menu] = False
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id,
        "Choise menu deactiavated")

'''
Turn choise menu active status throw key /menu
Переключение режима показа меню через ключ /menu
'''
def menu(update, context):
    command = context.args[0].lower()
    if ("on" == command):
        main_m_y(update, context)
    elif ("off" == command):
        main_m_n(update, context)

'''
Create start bot menu buttons
Создаем кнокки стартового меню бота
'''
def start_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Yes', callback_data='main_m_y'),
              InlineKeyboardButton('No', callback_data='main_m_n')]]
  return InlineKeyboardMarkup(keyboard)

'''
Create bot menu buttons
Создаем кнокки меню бота
'''
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Dog', callback_data='dog'),
              InlineKeyboardButton('Cat', callback_data='cat')]]
  return InlineKeyboardMarkup(keyboard)

'''
Message to start menu
Сообщение для стартового меню
'''
def start_menu_message():
  return 'Would you like to see choise menu?'

'''
Message to menu
Сообщение для меню
'''
def main_menu_message():
  return 'What next?'

'''
Bot dispatcer
Процедура работы бота
'''
def start_bot():
    global updater
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(dog, pattern='dog'))
    dispatcher.add_handler(CallbackQueryHandler(cat, pattern='cat'))
    dispatcher.add_handler(CallbackQueryHandler(main_m_y, pattern='main_m_y'))
    dispatcher.add_handler(CallbackQueryHandler(main_m_n, pattern='main_m_n'))
    dispatcher.add_handler(CommandHandler('dog', dog))
    dispatcher.add_handler(CommandHandler('cat', cat))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

    updater.start_polling()
    #updater.idle()

start_bot()