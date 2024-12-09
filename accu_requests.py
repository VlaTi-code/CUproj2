import requests


from settings import *


def bring_to_format(**kwargs):
    if "error" not in kwargs:
        loc_name = kwargs["loc_name"]
        loc_country = kwargs["loc_country"]
        weather_data = kwargs["weather_data"]
        return {
            "location": loc_name,   # Имя локации
            "country": loc_country,   # Страна
            "weather": weather_data[0]["IconPhrase"],   # Погода в целом
            "temperature": f"{int(float((weather_data[0]["Temperature"]["Value"]) - 32) * 5 / 9)}",  # Температура в Цельсиях
            "humidity": f"{weather_data[0]["RelativeHumidity"]}",  # Относительная влажность
            "wind_speed": f"{int(int(weather_data[0]["Wind"]["Speed"]["Value"]) * 1.60934)}",  # Скорость ветра в км/ч
            "wind_direction": weather_data[0]["Wind"]["Direction"]["Localized"],  # Направление ветра
            "error": ''
        }
    else:
        return {
            "error": kwargs["error"]
        }


class RequestHandler:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def get_region_key(self, lo, la) -> tuple:
        location_url = self.base_url + "/locations/v1/cities/geoposition/search"
        params = {
            "apikey": API_KEY,
            "q": f"{lo},{la}",
            "language": "ru"
        }
        response = requests.get(location_url, params=params)

        if response.status_code == 200:
            location_data = response.json()
            location_key = location_data["Key"]
            return location_key, location_data["LocalizedName"], location_data["Country"]["LocalizedName"], ''
        else:
            return '', '', '', f"Ошибка при получении данных о локации: {response.status_code}, {response.text}"

    def get_weather_by_coords(self, lo, la):
        loc_key, loc_name, loc_country, loc_error = self.get_region_key(lo, la)

        weather_url = self.base_url + f"/forecasts/v1/hourly/1hour/{loc_key}"
        params = {
            "apikey": API_KEY,
            "details": "true",
            "language": "ru"
        }
        response = requests.get(weather_url, params=params)

        if not loc_error and response.status_code == 200 and not loc_error:
            weather_data = response.json()
            return bring_to_format(weather_data=weather_data, loc_name=loc_name, loc_country=loc_country)
        elif loc_error:
            return bring_to_format(error=loc_error)
        else:
            return bring_to_format(
                error=f"Ошибка при получении данных о погоде: {response.status_code}, {response.text}"
            )
