"""
Бот, возвращающий данные о погоде в определенном месте в мире по запросу
"""


import re
import configparser
import logging.config
import flask
import telebot
from forecast import Forecast
from geolocation import Geolocation


config = configparser.ConfigParser()
config.read("/home/Flexer/UncleSlava/config/mainconfig.cfg")
TOKEN = config.get("keys", "TELEGRAM_TOKEN")
secret = config.get("keys", "SECRET")


bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://Flexer.pythonanywhere.com/{}".format(secret))


app = flask.Flask(__name__)


logging.config.fileConfig("/home/Flexer/UncleSlava/config/loggerconfig.cfg")
logger = logging.getLogger("root")


@app.route('/')
def hello_world():
    return ''


@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


"""
@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)
"""


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я могу рассказать тебе о погоде в любой точке мира.\n" +
        "Достаточно только написать мне Погода <место> и ты получишь ответ.\n" +
        "Например\n" +
        "Погода Москва\n" +
        "Погода Берлин\n" +
        "Погода Житомир"
    )


@bot.message_handler(regexp="погода")
def handle_message(message):
    plase = re.search(r"\s.*$", message.text)

    if plase:
        try:
            forecast = Forecast()
            maps = Geolocation()
            lat, lon = maps.get_coord_by_name(plase.group(0))
            forecast_data = forecast.get_weather_data(lat, lon)
            bot.send_message(message.chat.id, "Cегодня " + forecast_data[0])
            bot.send_message(message.chat.id, "Завтра " + forecast_data[1])

            logger.debug("{} запросил погоду в {}. Запрос выполнен".format(message.from_user, plase.group(0)))
        except ValueError:
            bot.send_message(message.chat.id, "Для {} координаты не найдены".format(plase.group(0)))
            logger.error(
                "{} запросил погоду в {}. Произошла ошибка. Координаты не найдены".format(
                    message.from_user,
                    plase.group(0)
                )
            )
    else:
        bot.send_message(message.chat.id, "Неверно введена место для поиска данных о погоде")
        bot.send_message(message.chat.id, "Попробуй еще раз!")
