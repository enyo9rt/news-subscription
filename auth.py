import bcrypt
import jwt
from flask import request, Flask, render_template, make_response
from flask_restx import Resource, Namespace, fields
from pymongo import MongoClient

import constants as cst

client = MongoClient('localhost', 27017)
db = client.harmonydb

app = Flask(__name__)

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="harmony")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})


@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: cst.REGISTER_SUCCESS_MSG})
    @Auth.doc(responses={409: cst.REGISTER_FAILED_MSG})
    def get(self):
        return make_response(render_template("auth/register.html"))

    def post(self):
        name = request.form['name_give']
        email = request.form['email_give']
        password = request.form['password_give']
        encrypted_password = bcrypt.hashpw(password.encode(cst.UTF_8), bcrypt.gensalt())

        doc = {
            "name": name,
            "email": email,
            "password": encrypted_password
        }

        db.users.insert_one(doc)
        return {
                   cst.AUTHORIZATION: jwt.encode({cst.USER_EMAIL: email}, cst.SECRET_KEY,
                                                 algorithm=cst.JWT_ENCRYPT_ALGORITHM)
               }, 200


@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: cst.LOGIN_SUCCESS_MSG})
    @Auth.doc(responses={404: cst.USER_NOT_FOUND_MSG})
    @Auth.doc(responses={500: cst.AUTH_FAILED_MSG})
    def get(self):
        return make_response(render_template("auth/login.html"))

    def post(self):
        email = request.form['email_give']
        password = request.form['password_give']

        print(email, password)
        user_list = list(db.users.find({}, {'_id': False}))

        for user in user_list:
            if user['email'] == email:
                if not bcrypt.checkpw(password.encode(cst.UTF_8), user['password']):  # 비밀번호 일치 확인
                    return {
                               cst.DEFAULT_MSG: cst.AUTH_FAILED_MSG
                           }, 401
                else:
                    return {
                               cst.AUTHORIZATION: jwt.encode({cst.USER_EMAIL: email}, cst.SECRET_KEY,
                                                             algorithm=cst.JWT_ENCRYPT_ALGORITHM)
                           }, 200

        return {
                   cst.DEFAULT_MSG: "로그인 실패"
               }, 404


@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: cst.LOGIN_SUCCESS_MSG})
    @Auth.doc(responses={404: cst.AUTH_FAILED_MSG})
    def get(self):
        # 헤더에 Authorization 담아 준다.
        header = request.headers.get(cst.AUTHORIZATION)
        if header is None:
            return {cst.DEFAULT_MSG: cst.PLZ_LOGIN}, 404
        data = jwt.decode(header, cst.SECRET_KEY, algorithms=cst.JWT_ENCRYPT_ALGORITHM)
        return data, 200


@Auth.route('/register/email-check')
class AuthEmailCheck(Resource):
    @Auth.doc(responses={200: "이메일 사용 가능"})
    @Auth.doc(responses={400: "사용 불가"})
    def post(self):
        email = request.form['email_give']

        user_list = list(db.users.find({}, {'_id': False}))

        for user in user_list:
            if user[cst.USER_EMAIL] == email:
                return {cst.DEFAULT_MSG: "400 Failed"}, 409

        return {cst.DEFAULT_MSG: "200 OK"}, 200
