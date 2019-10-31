from pymongo import MongoClient

connection  = MongoClient("mongodb+srv://mm260:UlChjqXiYBzRkJVb@driver-analysis-1hurl.mongodb.net/test?retryWrites=true")
db = connection.test

db.inventory.insert_one(
    {"item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {"h": 28, "w": 35.5, "uom": "cm"}})
