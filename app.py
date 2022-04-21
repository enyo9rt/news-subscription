from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dev_module import news_getter
from DB_ADMIN import account
import requests
import json

app = Flask(__name__)

client = MongoClient(account.API_KEY)
db = client.real

OPENWEATHER_API_KEY = "87e3a3b8ff90e9ceb2e9297d20722b2d"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/subscription", methods=["POST"])
def subscription():
    """
    뉴스 구독 정보(뉴스 종류, 전송 시간, user_email)를 subscription_admin 컬렉션에 저장
    :param: None
    :return: 문자열, 함수 성공 여부
    """
    subscription_type_receive = request.form['subscription_type_give']
    delivery_time_receive = request.form['delivery_time_give']
    user_email_receive = request.form['user_email_give']

    doc = {'subscription_type': subscription_type_receive, 'delivery_time': delivery_time_receive,
           'user_email': user_email_receive}
    db.subscription_admin.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


@app.route("/news", methods=["GET"])
def news_get():
    """
    DB의 news_log 컬렉션에서 뉴스 정보를 가져오기
    :param: None
    :return: 문자열 리스트, 뉴스 정보
    """
    news_list = news_getter.get_news()
    return jsonify({'news_list': news_list})


@app.route("/weather", methods=['GET'])
def weather_get():
    # Google geolocation API로부터 lat 과 lng 데이터 가져오기
    g_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDpRifMguxQNS9mb9g0wgF-4OnZPTikIfM'

    google_location_result = requests.post(g_url)
    google_data = google_location_result.text
    google_json_data = json.loads(google_data)

    lat = google_json_data['location']['lat']
    lng = google_json_data['location']['lng']

    # Openweathermap API로부터 화면에 넣어줄 데이터 가져오기
    w_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OPENWEATHER_API_KEY}&units=metric'

    weather_result = requests.get(w_url)
    weather_data = weather_result.text
    weather_json_data = json.loads(weather_data)

    # weather_json_data 에서 화면에 보여줄 데이터만 가져오기
    location = weather_json_data['name']
    weather = weather_json_data['weather'][0]['main']
    temp = weather_json_data['main']['temp']

    # 받아온 데이터 datas list에 넣기
    show_datas = [location, weather, temp]

    return jsonify({'show_datas': show_datas})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
