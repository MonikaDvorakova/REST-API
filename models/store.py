from db import db

class StoreModel(db.Model): 
    __tablename__ = "stores" 

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # uklada ty objekty ItemModel, ktere maji store_id odpovidajici id daneho store. Vrati list. lazy='dynamic means that list of items is created dynamically, proto v json() self.items je query, ktere se vzdy pta na to, jake jsou items, proto pouziji potom all(), self.items.all()
    # lazy='dynamic' zpusobi, ze pokazde kdyz pouzijeme json() pak jdeme do tabulky a to je pomalejsi. Bez toho se na zacatku vytvori list items a pak by items byl uz list a udelalo by se v json
    # list comprehension [item.json() for item in self.items]

    def __init__(self, name):
        self.name = name


    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() 
    
    def save_to_db(self): 
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()