# -*- coding: utf-8 -*-
import config
import telebot as tb
import stateworker as sw
import re


class Buttons:
    profile = tb.types.InlineKeyboardButton(text='Личный кабинет', callback_data='to_lc')
    register = tb.types.InlineKeyboardButton(text='Регистрация', callback_data='to_reg')
    calendar = tb.types.InlineKeyboardButton(text='Календарь', callback_data='to_cal')
    routs = tb.types.InlineKeyboardButton(text='Мои походы', callback_data='to_my_routs')
    rating = tb.types.InlineKeyboardButton(text='Рейтинг', callback_data='to_rating')
    main = tb.types.InlineKeyboardButton(text='Х', callback_data='to_main')
    contact = tb.types.KeyboardButton(text='Телефоны совпадают. Делюсь', request_contact=True)


bot = tb.TeleBot(config.token_telebot, threaded=False)


def start_menu(message):
    """
    Отправляет пользователю сообщение с главным меню. Кнопки в инлайн режиме.
    В зависимости от того, зарегистрирован ли пользователь, меняет Личный кабинет на Регистрацию
    """
    kb = tb.types.InlineKeyboardMarkup()
    if sw.is_member(message.chat.id):
        button1 = Buttons.profile
    else:
        button1 = Buttons.register
    button2 = Buttons.calendar
    kb.add(button1, button2)
    bot.send_message(message.chat.id, 'Главное меню бота', reply_markup=kb)


@bot.message_handler(commands=['start'])
def start_message(message):
    hello_world = 'Рад приветствовать тебя, путник. Я пока ещё ничего не умею, но скоро научусь.'
    bot.send_message(message.from_user.id, hello_world)
    start_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'to_cal')
def cal_menu(call):
    # TODO изучить https://github.com/unmonoqueteclea/calendar-telegram
    res = 'Я пока хз, как здесь выводить ближайшие или прошедшие мероприятия'
    bot.send_message(call.message.chat.id, res)


@bot.callback_query_handler(func=lambda call: call.data == 'to_lc')
def profile_menu(call):
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    kb = tb.types.InlineKeyboardMarkup()
    button1 = Buttons.routs
    button2 = Buttons.rating
    button3 = Buttons.main
    kb.add(button1, button2, button3)
    user_name = call.message.chat.first_name
    user_id = call.message.chat.id
    msg = f'{user_name} ({user_id}), добро пожаловать в личный кабинет \n ' \
          f'{sw.get_current_state(user_id)} - это твой уровень доступа \n' \
          f'{call.message.from_user.id}'
    bot.send_message(call.message.chat.id, msg, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data == 'to_my_routs')
def my_routs(call):
    res = 'Тут мы будем генерировать список походов из базы'
    bot.send_message(call.message.chat.id, res)


@bot.callback_query_handler(func=lambda call: call.data == 'to_rating')
def rating(call):
    res = 'Генерируем рейтинг и выводим его'
    bot.send_message(call.message.chat.id, res)


@bot.callback_query_handler(func=lambda call: call.data == 'to_main')
def go_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'to_reg')
def reg_user(call):
    bot.send_message(call.message.chat.id, 'Представьтесь, пожалуйста')
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, reg_name)


def reg_name(message):
    user_name = message.text
    bot.send_message(message.chat.id, f'{user_name}. Я запомню тебя.')
    print(f'Здесь я зписываю в БД {user_name}')
    reg_phone(message)
    bot.register_next_step_handler_by_chat_id(message.chat.id, check_phone)


def reg_phone(message):
    kb = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = Buttons.contact
    kb.add(contact_button)
    bot.send_message(chat_id=message.from_user.id,
                     reply_markup=kb,
                     text='Нам нужен телефон для связи. Жми кнопку или введи сам')


def check_phone(message):
    # Удаляем кнопку шары телефона
    del_kb = tb.types.ReplyKeyboardRemove(message.chat.id)
    if message.contact:
        if message.from_user.id == message.contact.user_id:
            tel_number = message.contact.phone_number
            bot.send_message(message.chat.id, f'Спасибо, твой телефон {tel_number}', reply_markup=del_kb)
            print(f'Тут я записываю номер телефона {tel_number}')
        else:
            bot.send_message(message.chat.id, 'Не пытайся меня обмануть, смертный')
            reg_phone(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id, check_phone)
    else:
        if re.match(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', message.text):
            bot.send_message(message.chat.id, f'{message.text} Твой номер телефона', reply_markup=del_kb)
            print(f'Тут я записываю номер телефона {message.text}')
        else:
            bot.send_message(message.chat.id, 'Не похоже на номер телефона')
            reg_phone(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id, check_phone)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = f'Я не знаю такой командой, поэтому отвечу просто:.\n' \
          f'{message.text}'
    print(f'{message.text}')
    bot.send_message(message.from_user.id, msg)
