from flask_restful import Resource, fields, marshal_with, reqparse

from App.models import Movie

movie_fields = {
    "id": fields.Integer,
    "showname": fields.String,
    "shownameen": fields.String,
    "director": fields.String,
    "leadingRole": fields.String,
    "type": fields.String,
    "country": fields.String,
    "language": fields.String,
    "duration": fields.Integer,
    "screeningmodel": fields.String,
    "openday": fields.DateTime,
    "backgroundpicture": fields.String,
    "flag": fields.Integer,
    "isdelete": fields.Boolean
}

result_fields = {
    "returnCode": fields.String,
    "returnValue": fields.List(fields.Nested(movie_fields))
}

parse = reqparse.RequestParser()
parse.add_argument("flag", type=int, help="请提供具体类型")


HOT = 1

FEATURE = 2


class MovieResource(Resource):

    @marshal_with(result_fields)
    def get(self):

        parser = parse.parse_args()

        flag = parser.get("flag")

        if flag == HOT:
            movies = Movie.query.filter(Movie.flag == flag)
        elif flag == FEATURE:
            movies = Movie.query.filter(Movie.flag == flag)
        else:
            movies = Movie.query.all()

        data = {
            "returnCode": "0",
            "returnValue": movies
        }

        return data
