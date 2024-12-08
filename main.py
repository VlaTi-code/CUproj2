from settings import *
from accu_requests import RequestHandler
from flask import Flask, render_template, request, jsonify

app = Flask("AccuProj")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получаем координаты из формы
        start_lat = request.form.get("start_lat")
        start_lon = request.form.get("start_lon")
        end_lat = request.form.get("end_lat")
        end_lon = request.form.get("end_lon")

        req_handler = RequestHandler("https://dataservice.accuweather.com")

        # Получаем погоду для обеих точек
        start_weather = req_handler.get_weather_by_coords(start_lat, start_lon)
        end_weather = req_handler.get_weather_by_coords(end_lat, end_lon)

        # Передаём данные в шаблон
        return render_template("index.html", start_weather=start_weather, end_weather=end_weather)

    # GET-запрос: отображаем пустую форму
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def hello():
    # Получим погоду в Долгопрудном (по заданию 1)
    la, lo = 55.928910, 37.523294

    req_handler = RequestHandler("https://dataservice.accuweather.com")
    req_handler.get_weather_by_coords(la, lo)

    return "Hi"


app.run()
