"""
Поиск координат по адресу
"""


import configparser
import googlemaps


class Geolocation:
    """
    Работа с данными карт google
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("/home/Flexer/UncleSlava/config/mainconfig.cfg")
        key = config.get("keys", "GOOGLE_KEY")
        self.gmaps = googlemaps.Client(key=key)

    def get_coord_by_name(self, plase):
        """
        Поиск координат места по его имени

        :param plase: название места, для которого ищутся координаты
        :type plase: str
        :return: координаты в виде lat, lng
        :except: ValueError когда для переданного места невозможно найти координаты
        """
        geocode_result = self.gmaps.geocode(plase)

        try:
            return geocode_result[0]["geometry"]["location"]["lat"], geocode_result[0]["geometry"]["location"]["lng"]
        except IndexError:
            raise ValueError("Для {} координаты не найдены".format(plase))


if __name__ == '__main__':
    maps = Geolocation()

    lat, lon = maps.get_coord_by_name("Нью Йорк")

    print("lat " + str(lat) + " lon " + str(lon))
