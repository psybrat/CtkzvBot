# -*- coding: utf-8 -*-
from enum import Enum
import tokens

token_telebot = tokens.telebot
DATABASE_STATE = 'state.vdb'
DATABASE_USERS = 'users.db'
DATABASE_ROLES = 'role.vdb'


class Roles(Enum):
    """
    Состояния регламентируются тремя цифрами. Первая цифра показывает уровень доступа
    0 - гость, 1 - зарегистрировавшийся, 2 - админ
    Вторая цифра устанавливает текущее положение в меню бота
    0 - главное меню, 1 - процесс регистрации, 2 - личный кабинет, 3 - календарь
    Третья цифра резервная
    """
    # Гость
    GUEST = 0
    # Юзер
    USER = 1
    # Admin
    ADMIN = 2


