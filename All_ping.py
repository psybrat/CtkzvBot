# -*- coding: utf-8 -*-


def all_vk_ping(data, loc='All'):
    """
    Выводит форматированный vk-текст для пинга в личных сообщениях или на стене.
    Вход: Список участников
    Аргументы: loc (default loc='All'  - все локации) локация участника (All, Msk)
    Вывод: Строка
    Пример:
    >>> a = [{'name':'Иван', 'nick':'', 'surname':'Иванов', 'vk_id':'12088123', 'loc':'Msk'}, \
    {'name':'Петр', 'nick':'Странник', 'surname':'Петров', 'vk_id':'280133048', 'loc':'Ekb'}, {}, \
    {'name':'Семён', 'nick':'', 'surname':'', 'vk_id':'1', 'loc':'Sbp'}]
    >>> all_vk_ping(a)
    '@id12088123 (Иван), @id280133048 (Петр), @id1 (Семён)'
    >>> all_vk_ping(a, loc = 'Msk')
    '@id12088123 (Иван)'
    """

    out = []
    for el in data:
        try:
            if (el['loc'] != loc) and loc != 'All':
                continue
            out.append('@id{vk_id} ({name})'.format(**el))
        except KeyError:
            continue
    return ', '.join(out)


if __name__ == "__main__":
    import doctest
    doctest.testmod()