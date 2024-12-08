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

        req_handler = RequestHandler("https://dataservice.accuweather.com")

        # Получаем погоду для обеих точек
        weather = req_handler.get_weather_by_coords(start_lat, start_lon)

        # Передаём данные в шаблон
        return render_template("index.html", weather=weather)

    # GET-запрос: отображаем пустую форму
    return render_template("index.html")

app.run()
