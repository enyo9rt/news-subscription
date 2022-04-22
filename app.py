import jwt
from flask import Flask, render_template, request, jsonify
from flask_restx import Api
from pymongo import MongoClient

import constants as cst
from DB_ADMIN import account
from dev_module.auth import Auth
from dev_module import news_getter
from dev_module import weather
from DB_ADMIN import account
from dev_module.comments import comments

app = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
app.register_blueprint(weather.weather_api)
app.register_blueprint(comments)

client = MongoClient(account.API_KEY)
db = client.Haromony

'''
API 자동 문서화를 위한 작업입니다.
Swagger 관련 설정 부분입니다.
/docs로 이동하면 확인할 수 있습니다.
'''
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

# 파일 분리화를 위한 작업입니다.
# /auth URI가 들어오면 다른 파일로 넘어갈 수 있게 해줍니다.
api.add_namespace(Auth, '/auth')


@app.route('/home')
def home():
    """
    헤더에 토큰이 있는지 확인하고 접근 가능하도록 합니다.
    메인 페이지에서 토큰을 넣어주면 페이지가 이동을 안해서 토큰을 사용하는 로직은 제외했습니다.
    """
    header = request.headers.get(cst.AUTHORIZATION)
    if header is None:
        # return {cst.DEFAULT_MSG: cst.PLZ_LOGIN}, 401
        return render_template('index.html')

    data = jwt.decode(header, cst.SECRET_KEY, algorithms=cst.JWT_ENCRYPT_ALGORITHM)
    return render_template('index.html', data=data)


@app.route("/subscription", methods=["POST"])
def subscription():
    """
    뉴스 구독 정보(뉴스 종류, 전송 시간, user_email)를 subscription admin 컬렉션에 저장
    :param: None
    :return: 문자열, 함수 성공 여부
    """
    subscription_type_receive = request.form['subscription_type_give']
    delivery_time_receive = request.form['delivery_time_give']
    user_email_receive = request.form['user_email_give']

    doc = {'subscription_type': subscription_type_receive, 'delivery_time': delivery_time_receive,
           'user_email': user_email_receive}
    db.subscription_admin.insert_one(doc)
    return jsonify({'msg': '구독 완료'})


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
