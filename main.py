# -*- coding: utf-8 -*-
from config import telebot_token
import telebot as tb

bot = tb.TeleBot(telebot_token)

# TODO обеспечить набор прокси
proxy_list = [""]

tb.apihelper.proxy = {'https': 'socks5://45.55.23.78:1080',
                      'https': 'socks5://107.170.41.156:52849',
                      'http': 'socks5://174.138.46.194:8080'}


def start_menu(message):
    markup = tb.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = tb.types.KeyboardButton('Личный кабинет')
    button2 = tb.types.KeyboardButton('Походы')
    markup.add(button1, button2)
    bot.send_message(message.from_user.id, 'Можете пока нажать на кнопки', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    hello_world = 'Рад приветствовать тебя, путник. Я пока ещё ничего не умею, но скоро научусь.'
    bot.send_message(message.from_user.id, hello_world)
    start_menu(message)


@bot.message_handler(content_types=['text'])
def lc_menu(message):
    if message.text == 'Личный кабинет':
        lc_buttons = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        lc_buttons.row('Регистрация', "Мои походы", "Рейтинг")
        user_name = message.from_user.first_name
        bot.send_message(message.from_user.id, f'{user_name}, добро пожаловать в личный кабинет',
                         reply_markup=lc_buttons)


@bot.message_handler(content_types=['text'])
def hike_menu(message):
    if message.text == 'Походы':
        hike_buttons = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        hike_buttons.row('Записаться в поход', "Календарь")
        user_name = message.from_user.first_name
        next_hike = '%Название% %Дата%'
        bot.send_message(message.from_user.id, f'{user_name}, ближайший поход {next_hike}',
                         reply_markup=hike_buttons)


def get_contacts(message):
    pass


# TODO написать алгоритм получения Фамилии, имени и телефона


@bot.message_handler(content_types=['text'])
def hike_reg(message):
    if message.text == 'Записаться в поход':
        get_contacts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, message.text)


bot.polling(none_stop=True, interval=1)
