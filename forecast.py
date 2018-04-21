"""
Получение данных о погоде по координатам местности
"""


import configparser
import pydarksky
import pendulum


class Forecast:
    """
    Получение погодных данных
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("/home/Flexer/UncleSlava/config/mainconfig.cfg")
        pendulum.set_formatter("alternative")
        self.forecast = pydarksky.DarkSky(config.get("keys", "DARK_SKY"))
        self.forecast.lang = "ru"
        self.forecast.units = "si"
        self.forecast.exclude = "currently"

    def get_weather_data(self, lat, lon):
        """
        Получить строку с данными о погоде на сегодня и завтра

        :param lat: широта
        :type lat: double
        :param lon: долгота
        :type lon: double
        :return: list of str список данных о погоде в заданных координатах
        """
        weather = self.forecast.weather(lat, lon)

        if weather.has_daily():
            days = list()
            days.append(weather.daily[0])
            days.append(weather.daily[1])

            data = list()

            for day in days:
                date = pendulum.from_timestamp(day.time, tz=weather.timezone)
                try:
                    temph = day.temperatureHigh
                    templ = day.temperatureLow
                    summary = day.summary

                    if temph > 0:
                        stemph = "+" + str(round(temph))
                    else:
                        stemph = str(round(temph))

                    if templ > 0:
                        stempl = "+" + str(round(templ))
                    else:
                        stempl = str(round(templ))

                    data.append("Днем: {}, ночью: {} {}".format(stemph, stempl, summary))
                except pydarksky.NoDataError:
                    data = "Для данной местности не удалось получить погодные данные"

            return data


if __name__ == '__main__':
    forecast = Forecast()
    print(forecast.get_weather_data(55.75600, 37.60005))

