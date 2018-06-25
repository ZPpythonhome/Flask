from flask_restful import Api

from App.apis.CinemasApi import CinemasResource
from App.apis.CityApi import CityResource
from App.apis.HelloApi import HelloResource
from App.apis.MovieApi import MovieResource
from App.apis.OrderApi import OrderResource, HallResource
from App.apis.TicketApi import TicketResource
from App.apis.UserApi import UserResource
from App.models import Letter

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(HelloResource, "/hello/")

api.add_resource(CityResource, "/cities/", methods=["GET", "POST"])

api.add_resource(MovieResource, "/movies/")

api.add_resource(CinemasResource, "/cinemas/")

api.add_resource(UserResource, "/users/", methods=["POST", "GET"])

api.add_resource(OrderResource, "/orders/", methods=["POST"])

api.add_resource(HallResource, "/halls/", methods=["POST"])

api.add_resource(TicketResource, "/tickets/", methods=["POST", "GET"])
