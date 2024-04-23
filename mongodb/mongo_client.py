import pymongo
import json

class MongoDBClient:
    def __init__(self, db, col, username=None, password=None):
        if username and password:
            uri = f"mongodb://{username}:{password}@localhost:27017/"
            self.client = pymongo.MongoClient(uri)
        else:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client[db]
        self.collection = self.database[col]

    def insert_elements(self,data_json):
        #data = json.loads(data_json)

        # Iterar sobre los elementos y insertarlos en la colección
        for edge in data_json["data"]["search"]["edges"]:
            node = edge["node"]
            self.collection.insert_one({
                "name": node["name"],
                "owner": node["owner"]["login"],
                "stargazers": node["stargazers"]["totalCount"]
            })





