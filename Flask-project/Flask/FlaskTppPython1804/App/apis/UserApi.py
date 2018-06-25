import uuid

from flask import render_template
from flask_mail import Message
from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash

from App import ModelUtil
from App.ext import mail, cache
from App.models import User

parse = reqparse.RequestParser()
parse.add_argument("action", type=str, required=True, help="请声明具体操作")
parse.add_argument("u_token")

parse_get = parse.copy()

parse.add_argument("upassword", type=str, required=True, help="请设置密码")

parse_post_login = parse.copy()

parse_post_login.add_argument("uname", type=str, required=True, help="请提供用户名")

parse_post_register = parse.copy()

parse_post_register.add_argument("uname", type=str, required=True, help="请提供用户名")
parse_post_register.add_argument("uemail", type=str, required=True, help="请系统邮箱")


user_fields = {
    "id": fields.Integer,
    "u_name": fields.String,
    "u_email": fields.String
}

result_fields = {
    "returnCode": fields.String,
    "returnMsg": fields.String,
    "u_token": fields.String,
    "returnValue": fields.Nested(user_fields)
}


class UserResource(Resource):

    @marshal_with(result_fields)
    def post(self):

        parse_common = parse.parse_args()

        action = parse_common.get("action")

        if action == "register":

            parser = parse_post_register.parse_args()

            u_name = parser.get("uname")
            u_email = parser.get("uemail")
            u_password = parser.get("upassword")

            user = User()
            user.u_name = u_name
            user.u_email = u_email
            # user.u_password = generate_password_hash(u_password)
            user.set_password(u_password)

        # db.session.add(user)
        # db.session.commit()

            save_result = user.save()

            if save_result == ModelUtil.SUCCESS:

                subject = "淘票票用户激活"

                u_token = str(uuid.uuid4())

                cache.set(u_token, user.id, timeout=60 * 60 * 24)

                msg = Message(subject, recipients=[user.u_email], sender="rongjiawei1204@163.com")

                html = render_template('user_activate.html', username=u_name,
                                       activate_url="http://localhost:5000/users/?action=activate&u_token=%s" % u_token)

                msg.html = html

                mail.send(msg)

                data = {
                    "returnCode": "0",
                    "returnMsg": "注册成功",
                    "returnValue": user
                }

                return data

            else:

                data = {
                    "returnCode": "801",
                    "returnMsg": "注册失败"
                }

                return data
        elif action == "login":

            parser = parse_post_login.parse_args()

            u_name = parser.get("uname")
            u_password = parser.get("upassword")

            users = User.query.filter(User.u_name == u_name)

            data = {

            }

            if users.count() == 0:
                data["returnCode"] = "803"
                data["returnMsg"] = "用户名或密码错误"
                return data
            else:
                user = users.first()

                # if check_password_hash(user.u_password, u_password):
                if user.verify_password(u_password):
                    u_token = str(uuid.uuid4())
                    cache.set(u_token, user.id)
                    data["u_token"] = u_token
                    data["returnCode"] = "0"
                    data["returnMsg"] = "登录成功"
                    data["returnValue"] = user
                    return data
                else:
                    data["returnCode"] = "803"
                    data["returnMsg"] = "用户名或密码错误"
                    return data

    def get(self):

        parser = parse_get.parse_args()

        action = parser.get("action")

        data = {}

        if action == "activate":
            u_token = parser.get("u_token")

            user_id = cache.get(u_token)

            cache.delete(u_token)

            if user_id:

                user = User.query.get(user_id)

                user.is_activate = True

                user.save()

                data["returnMsg"] = "激活成功"
                data["returnCode"] = "0"

                return data
            else:

                data["returnMsg"] = "邮件已过期，请重新激活"
                data["returnCode"] = "802"

                return data

        return {"msg": "send ok"}
