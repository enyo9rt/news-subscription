import bcrypt
import jwt
from flask import request, Flask, render_template, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from pymongo import MongoClient

import constants as cst

users = {}

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
    @Auth.doc(responses={500: cst.REGISTER_FAILED_MSG})
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
            "password": encrypted_password.decode(cst.UTF_8)
        }

        if email in users:
            return {cst.DEFAULT_MSG: cst.REGISTER_FAILED_MSG}, 500
        else:
            users[email] = encrypted_password
            db.users.insert_one(doc)
            print(users)
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
        name = request.form[cst.USER_NAME]
        password = request.form[cst.USER_PW]
        if name not in users:
            return {
                       cst.DEFAULT_MSG: cst.USER_NOT_FOUND_MSG
                   }, 404
        elif not bcrypt.checkpw(password.encode(cst.UTF_8), users[name]):  # 비밀 번호 일치 확인
            return {
                       cst.DEFAULT_MSG: cst.AUTH_FAILED_MSG
                   }, 500
        else:
            return {
                       # str 으로 반환 하여 return
                       cst.AUTHORIZATION: jwt.encode({cst.USER_NAME: name}, cst.SECRET_KEY,
                                                     algorithm=cst.JWT_ENCRYPT_ALGORITHM)
                   }, 200


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
    @Auth.doc(responses={200: "200 OK"})
    @Auth.doc(responses={404: "404 ERROR"})
    @Auth.doc(responses={500: "500 ERROR"})
    def post(self):
        email = request.form['email_give']
        print(f'전달 받은 이메일 값 : {email}')
        return jsonify({'msg': email})