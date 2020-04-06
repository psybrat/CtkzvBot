# -*- coding: utf-8 -*-

from vedis import Vedis
import config


def get_current_role(user_id):
    """
    Проверяем текущее состояние из базы. Если отсутствует, записываем в базу состояние GUEST
    >>> test_id = '12345'
    >>> get_current_role(test_id)
    0
    """
    with Vedis(config.DATABASE_ROLES) as db:
        try:
            return int(db[user_id].decode())
        except KeyError:
            if set_role(user_id, config.Roles.GUEST.value):
                return int(config.Roles.GUEST.value)
            else:
                print('Какая-то херня с базой состояний')


def set_role(user_id, value):
    """
    Записываем в базу состояний для пользователя user_id состояние value
    #TODO Написать обработку исключений
    >>> test_id = '999999'
    >>> get_current_role(test_id)
    0
    >>> set_role(test_id, config.Roles.USER.value)
    True
    >>> set_role(test_id, config.Roles.GUEST.value)
    True
    """
    with Vedis(config.DATABASE_ROLES) as db:
        try:
            db[user_id] = value
            return True
        except Exception:
            return False


def is_member(user_id):
    """
    Проверяем, зарегистрирован ли пользователь? Возвращаем True/False
    >>> test_id = '11111'
    >>> set_role(test_id, config.Roles.GUEST.value)
    True
    >>> is_member(test_id)
    False
    >>> set_role(test_id, config.Roles.USER.value)
    True
    >>> is_member(test_id)
    True
    """
    state = get_current_role(user_id)
    return bool(state)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
