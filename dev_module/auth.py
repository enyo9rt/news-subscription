import bcrypt
import jwt
from flask import request, Flask, render_template, make_response
from flask_restx import Resource, Namespace
from pymongo import MongoClient

import constants as cst
# MongoDB 관련 설정
from DB_ADMIN import account

client = MongoClient(account.API_KEY)
db = client.Haromony
#

app = Flask(__name__)

# restx 파일 분리에 사용되는 Namespace, BluePrint 와 같은거라고 보면 됩니다.
Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

@Auth.route('/register')
class AuthRegister(Resource):
    """회원 가입을 위한 클래스 입니다."""
    '''
     @Auth.expect, @Auth.doc 는 스웨거에 세부적으로 설정하기 위해서 사용하는 어노테이션입니다. 
    '''

    @Auth.doc(responses={200: cst.REGISTER_SUCCESS_MSG})
    @Auth.doc(responses={409: cst.REGISTER_FAILED_MSG})
    def get(self):
        return make_response(render_template("auth/register.html"))

    """회원 가입 로직"""

    def post(self):
        name = request.form['name_give']
        email = request.form['email_give']
        password = request.form['password_give']
        # bcrypt 라이브러리로 입력받은 비밀번호를 암호화합니다.
        encrypted_password = bcrypt.hashpw(password.encode(cst.UTF_8), bcrypt.gensalt())

        # DB에 저장
        doc = {
            "name": name,
            "email": email,
            "password": encrypted_password
        }

        db.users.insert_one(doc)
        # 회원 가입이 완료되면 생성된 JWT 토큰을 리턴합니다.
        return {
                   cst.AUTHORIZATION: jwt.encode({cst.USER_EMAIL: email}, cst.SECRET_KEY,
                                                 algorithm=cst.JWT_ENCRYPT_ALGORITHM)
               }, 200


@Auth.route('/login')
class AuthLogin(Resource):
    """로그인을 위한 클래스 입니다."""

    @Auth.doc(responses={200: cst.LOGIN_SUCCESS_MSG})
    @Auth.doc(responses={404: cst.USER_NOT_FOUND_MSG})
    @Auth.doc(responses={500: cst.AUTH_FAILED_MSG})
    def get(self):
        return make_response(render_template("auth/login.html"))

    """로그인 요청 로직"""

    def post(self):
        email = request.form['email_give']
        password = request.form['password_give']

        user_list = list(db.users.find({}, {'_id': False}))

        """유저DB에서 일치하는 이메일이 있는지 확인합니다."""
        for user in user_list:
            if user['email'] == email:
                # 입력한 비밀번호와 저장된 비밀번호를 비교해서 일치 하는지 확인합니다.
                if not bcrypt.checkpw(password.encode(cst.UTF_8), user['password']):
                    return {
                               cst.DEFAULT_MSG: cst.AUTH_FAILED_MSG
                           }, 401
                else:
                    # 일치한다면 생성된 토큰을 리턴합니다.
                    return {
                               cst.AUTHORIZATION: jwt.encode({cst.USER_EMAIL: email}, cst.SECRET_KEY,
                                                             algorithm=cst.JWT_ENCRYPT_ALGORITHM)
                           }, 200

        return {
                   cst.DEFAULT_MSG: "로그인 실패"
               }, 404


@Auth.route('/register/email-check')
class AuthEmailCheck(Resource):
    """이메일 중복 검사 클래스"""

    @Auth.doc(responses={200: "이메일 사용 가능"})
    @Auth.doc(responses={400: "사용 불가"})
    def post(self):
        """DB에 회원 정보에 같은 이메일이 있는 확인하고 결과를 리턴합니다."""
        email = request.form['email_give']

        user_list = list(db.users.find({}, {'_id': False}))

        for user in user_list:
            if user[cst.USER_EMAIL] == email:
                return {cst.DEFAULT_MSG: "400 Failed"}, 409

        return {cst.DEFAULT_MSG: "200 OK"}, 200
