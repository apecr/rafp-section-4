from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)

items = []

jwt = JWT(authenticate, identity)


def get_item_by_name(name):
    return next(filter(lambda x: x['name'] == name, items), None)


class Item(Resource):
    def get(self, name):
        item = get_item_by_name(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        item = get_item_by_name(name)
        if item:
            return {'message': 'item {} already created'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5002, debug=True)
