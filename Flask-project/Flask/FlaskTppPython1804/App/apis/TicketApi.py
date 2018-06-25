from flask import request
from flask_restful import Resource, abort

from App import models
from App.ext import cache
from App.models import User


def login_required(fun):

    def f(*args, **kwargs):

        u_token = request.args.get("u_token")

        if u_token:

            user_id = cache.get(u_token)

            if user_id:

                return fun(*args, **kwargs)
            else:
                abort(401, message="用户状态失效")
        else:
            abort(401, message="用户未登录")
    return f


def check_permission(permission):

    def check(fun):

        def f(*args, **kwargs):

            u_token = request.form.get("u_token")

            if not u_token:
                abort(401, message="用户未登录")
            else:
                user_id = cache.get(u_token)
                if not user_id:
                    abort(401, message="用户状态失效")
                else:
                    user = User.query.get(user_id)

                    if not user:
                        abort(401, message="用户状态失效哈哈")
                    else:

                        if user.check_permission(permission):
                            return fun(*args, **kwargs)
                        else:
                            abort(403, message="你没有权限操作本模块")
        return f
    return check


class TicketResource(Resource):

    @login_required
    def get(self):

        return {"msg": "ticket ok"}

    @check_permission(models.PERMISSION_MODIFICATION)
    def post(self):

        # u_token = request.form.get("u_token")
        #
        # if not u_token:
        #     abort(401, message="用户未登录")
        # else:
        #     user_id = cache.get(u_token)
        #
        #     if not user_id:
        #         abort(401, message="登录状态失效")
        #     else:
        #         user = User.query.get(user_id)
        #
        #         if user.u_permission & models.PERMISSION_MODIFICATION == models.PERMISSION_MODIFICATION:
        #
        #             # 逻辑 逻辑 逻辑
        #
        #             return {"msg": "ticket post ok"}
        #         else:
        #             abort(403, message="您没有权限操作此模块")

        # 进到这里面来的，就满足全部条件了， 这里面直接做操作就行了

        return {"msg": "ticket post ok"}
