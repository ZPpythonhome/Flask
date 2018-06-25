from flask_restful import Resource, fields, marshal_with, reqparse

from App.models import Cinemas

cinemas_fields = {
    "name": fields.String,
    "city": fields.String,
    "district": fields.String,
    "address": fields.String,
    "phone": fields.String,
    "score": fields.Float,
    "hallnum": fields.Integer,
    "servicecharge": fields.Float,
    "astrict": fields.Integer,
    "flag": fields.Integer,
}

result_fields = {
    "returnCode": fields.String,
    "returnValue": fields.List(fields.Nested(cinemas_fields))
}

parse = reqparse.RequestParser()

parse.add_argument("city", type=str, required=True ,help="请选择你的城市")
parse.add_argument("district", type=str)
parse.add_argument("sortrule", type=int)

SCORE_DESC = 1
SCORE_ASC = 2
TOTAL_DESC = 3


class CinemasResource(Resource):

    @marshal_with(result_fields)
    def get(self):

        parser = parse.parse_args()

        city = parser.get("city")

        cinemas_list = Cinemas.query.filter(Cinemas.city == city)

        district = parser.get("district")

        if district:
            cinemas_list = cinemas_list.filter(Cinemas.district == district)

        sortrule = parser.get("sortrule")

        if sortrule == SCORE_DESC:
            cinemas_list = cinemas_list.order_by("-score")
        elif sortrule == SCORE_ASC:
            cinemas_list = cinemas_list.order_by("score")
        elif sortrule == TOTAL_DESC:
            pass

        data = {
            "returnCode": "0",
            "returnValue": cinemas_list
        }

        return data
