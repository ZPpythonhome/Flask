from flask_restful import Resource, fields, marshal_with, marshal

from App.models import Letter, City

city_fields = {
    "id": fields.Integer,
    "regionName": fields.String,
    "cityCode": fields.Integer,
    "pinYin": fields.String
}

city_list_fields = {
    "A": fields.List(fields.Nested(city_fields)),
    "B": fields.List(fields.Nested(city_fields)),
    "C": fields.List(fields.Nested(city_fields)),
    "D": fields.List(fields.Nested(city_fields)),
    "E": fields.List(fields.Nested(city_fields)),
    "F": fields.List(fields.Nested(city_fields)),
    "G": fields.List(fields.Nested(city_fields)),
    "H": fields.List(fields.Nested(city_fields)),
    "J": fields.List(fields.Nested(city_fields)),
    "K": fields.List(fields.Nested(city_fields)),
    "L": fields.List(fields.Nested(city_fields)),
    "M": fields.List(fields.Nested(city_fields)),
    "N": fields.List(fields.Nested(city_fields)),
    "P": fields.List(fields.Nested(city_fields)),
    "Q": fields.List(fields.Nested(city_fields)),
    "R": fields.List(fields.Nested(city_fields)),
    "S": fields.List(fields.Nested(city_fields)),
    "T": fields.List(fields.Nested(city_fields)),
    "W": fields.List(fields.Nested(city_fields)),
    "X": fields.List(fields.Nested(city_fields)),
    "Y": fields.List(fields.Nested(city_fields)),
    "Z": fields.List(fields.Nested(city_fields))
}

return_fields = {
    "returnCode": fields.String,
    "returnValue": fields.Nested(city_list_fields)
}


class CityResource(Resource):

    def get(self):

        returnValue = {}

        letters = Letter.query.order_by("letter").all()

        # print(letters)
        city_list_fields_dynamic = {}

        for letter in letters:
            cities = City.query.filter(City.c_letter == letter.id).all()

            returnValue[letter.letter] = cities

            city_list_fields_dynamic[letter.letter] = fields.List(fields.Nested(city_fields))

        return_fields_dyncmic = {
            "returnCode": fields.String,
            "returnValue": fields.Nested(city_list_fields_dynamic)
        }

        data = {
            "returnCode": "0",
            "returnValue": returnValue
        }

        result = marshal(data, return_fields_dyncmic)

        return result

    @marshal_with(return_fields)
    def post(self):

        returnValue = {}

        letters = Letter.query.order_by("letter").all()

        print(letters)

        for letter in letters:

            cities = City.query.filter(City.c_letter == letter.id).all()

            returnValue[letter.letter] = cities


        data = {
            "returnCode": "0",
            "returnValue": returnValue
        }

        return data
