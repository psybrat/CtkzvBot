# TODO посмотреть MTProto бота https://docs.telethon.dev/en/latest/concepts/asyncio.html
from bot import bot
import telebot as tb
import time
import proxy_changer


ip_port = proxy_changer.read_proxy()
tb.apihelper.proxy = {'https': 'https://{}'.format(ip_port)}

if __name__ == '__main__':
    i = 0
    while True:
        try:
            bot.polling(none_stop=False, timeout=3, interval=3)
        except OSError:
            print('Останавливаем бота')
            bot.stop_polling()
            time.sleep(5)
            proxy = proxy_changer.get_proxy()
            ip_port = proxy['ip_port']
            tb.apihelper.proxy = {'https': 'https://{}'.format(ip_port)}
            proxy_changer.write_proxy(ip_port)

        except Exception as e:
            print(f'Ошибка номер {i}')
            print(e)
            i += 1
            time.sleep(5)