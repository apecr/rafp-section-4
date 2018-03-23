from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


def get_item_by_name(name):
    item = [item for item in items if item['name'] == name]
    if item:
        return item[0]
    return None


class Item(Resource):
    def get(self, name):
        item = get_item_by_name(name)
        if item:
            return item
        return {'item': None}, 404

    def post(self, name):
        item = get_item_by_name(name)
        if not item:
            data = request.get_json()
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201
        return {'message': 'item {} already created'.format(name)}, 400


class Items(Resource):
    def get(self):
        return items


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5002, debug=True)
