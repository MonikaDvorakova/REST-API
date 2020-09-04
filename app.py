from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from db import db



from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # rika sqlalchemy, kde ma najit databazy. Misto sqlite muze byt cokoliv jineho, treba mysql, postgresql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # vypne track modification pro rest_api_sqalchemy ne pro samotnou SQLAlchemy

api = Api(app)
app.secret_key = 'jose'

@app.before_first_request # zavola se pred prvnim request, at uz je jakykoliv, a vytvori tabulky a soubor data.db
def create_tables():
    db.create_all() # vytvori pouze tabulky, ktere vidi. Pujde pres importy nahore a pres importy resources se dostane do models a tam vidi nazvy tabulek ktere ma vytvorit. Pokud by tam ty importy nebyly, tak se to nevytvori.

jwt = JWT(app, authenticate, identity)


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)