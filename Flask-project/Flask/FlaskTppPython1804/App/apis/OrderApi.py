from flask import request
from flask_restful import Resource, abort


class BaseResource(Resource):


    def generate_result(self):

        return {"msg": "post ok"}

    def post(self):

        u_token = request.form.get("u_token")

        if u_token:

            return self.generate_result()
        else:
            abort(401)



class OrderResource(BaseResource):

    def generate_result(self):

        print("这种方式，实现代码复用，玩起来感觉怎么样")

        print("感觉还不错")

        return {"msg" : "oh 还可以这样玩"}


class HallResource(BaseResource):

    def generate_result(self):

        return {"msg": "这是大厅"}




