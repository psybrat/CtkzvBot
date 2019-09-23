# -*- coding: utf-8 -*-

from vedis import Vedis
import config


def get_current_state(user_id):
    '''
    Проверяем текущее состояние из базы. Если отсутствует, записываем в базу состояние NEW
    '''
    with Vedis(config.DATABASE_STATE) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            if set_state(user_id, config.States.NEW.value):
                return config.States.NEW.value
            else:
                print('Какая-то херня с базой состояний')


def set_state(user_id, value):
    """
    Записываем в базу состояний для пользователя user_id состояние value
    #TODO Написать обработку исключений
    """
    with Vedis(config.DATABASE_STATE) as db:
        try:
            db[user_id] = value
            return True
        except Exception:
            return False


def is_member(user_id):
    """
    Проверяем, зарегистрирован ли пользователь? Возвращаем True/False
    """
    state = get_current_state(user_id)
    print(f'{user_id}|{state[:1]} - {bool(int(state[:1]))}')
    return bool(int(state[:1]))


if __name__ == "__main__":
    sys.exit(_test())
