# internal representation of the what the item does and how it looks like

from db import db

class ItemModel(db.Model): #db.Model je spojeni s SQLAlchemy. Objekty teto tridy se bodou pridavat jako radky do tabulky
    __tablename__ = "items" # specifikujeme nazev tabulky, musi byt stejny jako nazev, ktery pouzivam v queries.

    id = db.Column(db.Integer, primary_key=True) # definujeme sloupce tabulky. Musi byt stejne jako nazvy properties v init. V init muzou byt i jine vlastnosti, pokud ale nejsou tady spojeny s tabulkou, tak se nebudou ukladat.
    name = db.Column(db.String(80)) # 80 omezuje delku stringu na 80 znaku
    price = db.Column(db.Float(precision=2)) # precision je pocet desetinnych mist
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # propojeni na tabulku stores, reference do ktereho store patri.
    store = db.relationship('StoreModel') # now every ItemModel has its property store, which is a StoreModel corresponding to store with the id which is same as store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1. Query a filter by je z db.Model, ze ktereho dedi ItemModel. first() vrati pouze prvni objekt.
        # vraci to ItemModel object.
    
    def save_to_db(self): # zaroven to vklada, pripadne updatuje zaznam, pokud uz je v tabulce
        db.session.add(self) # objekt pridava do databaze sebe.
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        