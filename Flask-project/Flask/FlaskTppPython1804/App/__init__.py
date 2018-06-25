from flask import Flask

from App.apis import init_api
from App.ext import init_ext
from App.settings import envs



def create_app():

    app = Flask(__name__)
    # 初始化app
    app.config.from_object(envs.get("develop"))

    # 初始化蓝图，路由
    init_api(app)

    # 初始化第三方库
    init_ext(app)

    return app

