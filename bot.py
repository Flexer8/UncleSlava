# Простейший бот, запущеный на flask-сервере


import re
import configparser
import flask
import telebot
from forecast import Forecast
from geolocation import Geolocation


config = configparser.ConfigParser()
config.read("config/mainconfig.cfg")
TOKEN = config.get("keys", "TELEGRAM_TOKEN")
secret = config.get("keys", "SECRET")


bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://Flexer.pythonanywhere.com/{}".format(secret))

app = flask.Flask(__name__)


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


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(regexp="погода")
def handle_message(message):
    plase = re.search(r"\s.*$", message.text)

    if plase:
        try:
            forecast = Forecast()
            maps = Geolocation()
            lat, lon = maps.get_coord_by_name(plase.group(0))
            bot.send_message(message.chat.id, forecast.get_weather_data(lat, lon))
        except ValueError:
            bot.send_message(message.chat.id, "Для {} координаты не найдены".format(plase.group(0)))
    else:
        bot.send_message(message.chat.id, "Неверно введена место для поиска данных о погоде")
        bot.send_message(message.chat.id, "Попробуй еще раз!")
