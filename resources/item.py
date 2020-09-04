from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name): # excepts get method
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'mesage': 'Item not found'}, 404 

    def post(self, name):
        if ItemModel.find_by_name(name): # protoze find_by_name je classmethod je mozne to napsat take jako Item.find_by_item, v tomto pripade je to jedno
            return {'message': f"An item with name {name} already exists"}, 400

        data = Item.parser.parse_args()  #request.get_json(silent=True) silent=True returns None if the data are in bad format or are not there. Mozno take pouzit force=True menas we dont need content type header. It will look at the data and guess the data type
        item = ItemModel(name, data['price'], data['store_id']) # data['price'], data['store_id'] muzu zapsat jako **data
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # internal server error

        return item.json(), 201 # 201 status code for created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])

        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #mozne zapsat jako list(map(lambda x: x.json(), ItemModel.query.all())) map vezme funkci lambda a aplikuje ji na kazdy prvek z query.all(), list pak ze vseho udela list