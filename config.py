# -*- coding: utf-8 -*-
from enum import Enum
import tokens

token_telebot = tokens.telebot
DATABASE_STATE = 'state.vdb'
DATABASE_USERS = 'users.db'


class States(Enum):
    """
    Состояния регламентируются тремя цифрами. Первая цифра показывает уровень доступа
    0 - гость, 1 - зарегистрировавшийся, 2 - админ
    Вторая цифра устанавливает текущее положение в меню бота
    0 - главное меню, 1 - процесс регистрации, 2 - личный кабинет, 3 - календарь
    Третья цифра резервная
    """
    # Гость
    NEW = '000'
    N_REG = '010'
    N_CALENDAR = '030'
    # Юзер
    U_CAB = '120'
    U_CALENDAR = '130'
    # Admin
    A_CAB = '220'
    A_CALENDAR = '230'


