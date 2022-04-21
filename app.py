from flask import Flask, render_template, request, jsonify
from flask_restx import Api
from pymongo import MongoClient

from auth import Auth
from dev_module import news_getter
from dev_module import weather
from DB_ADMIN import account
import constants as cst

app = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
app.register_blueprint(weather.weather_api)

client = MongoClient(account.API_KEY)
db = client.Haromony

api = Api(
    app,
    version='0.1',
    title="Harmony's API Server",
    description="Harmony's News API Server!",
    terms_url="/",
    doc='/docs',
    contact="cadqe13@gmail.com",
    base_url="/test"
)

api.add_namespace(Auth, '/auth')


@app.route('/home')
def home():
    header = request.headers.get(cst.AUTHORIZATION)
    if header is None:
        return {cst.DEFAULT_MSG: cst.PLZ_LOGIN}, 401
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
    print(doc)
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
