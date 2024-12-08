import requests

from settings import *


def bring_to_format(weather_data, loc_name, loc_country):
    return {
        "location": loc_name,   # Имя локации
        "country": loc_country,   # Страна
        "weather": weather_data[0]["WeatherText"],   # Погода в целом
        "temperature": weather_data[0]["Temperature"]["Metric"]["Value"],  # Температура
        "humidity": weather_data[0]["RelativeHumidity"],  # Влажность
        "wind_speed": weather_data[0]["Wind"]["Speed"]["Metric"]["Value"],  # Скорость ветра
        "wind_direction": weather_data[0]["Wind"]["Direction"]["Localized"],  # Направление ветра
    }


class RequestHandler:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def get_region_key(self, lo, la) -> tuple:
        location_url = self.base_url + "/locations/v1/cities/geoposition/search"
        params = {
            "apikey": API_KEY,
            "q": f"{lo},{la}"
        }
        response = requests.get(location_url, params=params)

        if response.status_code == 200:
            location_data = response.json()
            location_key = location_data["Key"]
            return location_key, location_data["LocalizedName"], location_data["Country"]["LocalizedName"]
        else:
            print(f"Error: {response.status_code}")
            exit()

    def get_weather_by_coords(self, lo, la):
        loc_key, loc_name, loc_country = self.get_region_key(lo, la)

        weather_url = self.base_url + f"/forecasts/v1/hourly/1hour/{loc_key}"
        params = {
            "apikey": API_KEY
        }
        response = requests.get(weather_url, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            return bring_to_format(weather_data, loc_name, loc_country)
