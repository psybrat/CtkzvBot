# -*- coding: utf-8 -*-
from config import telebot_token
import telebot as tb

bot = tb.TeleBot(telebot_token)

# TODO обеспечить набор прокси
proxy_list = [""]

tb.apihelper.proxy = {'https': 'socks5://45.55.23.78:1080',
                      'https': 'socks5://107.170.41.156:52849',
                      'http': 'socks5://174.138.46.194:8080',
                      'http': 'socks5://165.227.80.227:3128'}


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


@bot.message_handler(regexp='Личный кабинет')
def lc_menu(message):
    lc_buttons = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lc_buttons.row('Регистрация', "Мои походы", "Рейтинг")
    user_name = message.from_user.first_name
    msg = f'{user_name}, добро пожаловать в личный кабинет'
    bot.send_message(message.from_user.id, msg, reply_markup=lc_buttons)


@bot.message_handler(regexp='Походы')
def hike_menu(message):
    hike_buttons = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    hike_buttons.row('Записаться в поход', "Календарь")
    user_name = message.from_user.first_name
    next_hike = 'Название Дата'
    msg = f'{user_name}, ближайший поход {next_hike}'
    bot.send_message(message.from_user.id, msg, reply_markup=hike_buttons)


def get_contacts(message):
    user_dict = {}

    class User:
        def __init__(self, name):
            self.name = name
            self.surname = None
            self.phone_number = None

    def process_name_start(message):
        msg = 'Назовите своё имя'
        bot.send_message(message.from_user.id, msg)
        bot.register_next_step_handler(message, process_name_step)

    def process_name_step(message):
        try:
            chat_id = message.from_user.id
            name = message.text
            user = User(name)
            user_dict[chat_id] = user
            msg = f'Я запомню тебя, {name}\n' \
                  f'Напиши мне свой телефон для связи'
            bot.send_message(message.from_user.id, msg)
            bot.register_next_step_handler(message, process_phone_number)
        except Exception as e:
            bot.reply_to(message, 'Ты втираешь мне дичь')

    def process_phone_number(message):
        try:
            chat_id = message.from_user.id
            phone_number = message.text
            user = user_dict[chat_id]
            user.phone_number = phone_number
            msg = f'{user.name}, я запомню твой номер телефона\n' \
                  f'tel: {user.phone_number}'
            bot.send_message(message.from_user.id, msg)
        except Exception as e:
            bot.reply_to(message, 'Ты втираешь мне дичь')

    process_name_start(message)


@bot.message_handler(regexp='Записаться в поход')
def hike_reg(message):
    get_contacts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = f'Я не знаю такой командой, поэтому отвечу просто:.\n' \
          f'{message.text}'
    bot.send_message(message.from_user.id, msg)


bot.polling(none_stop=True, interval=1, timeout=20)
