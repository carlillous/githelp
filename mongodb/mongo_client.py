import pymongo

class MongoDBClient:
    def __init__(self, db, col, username=None, password=None):
        if username and password:
            uri = f"mongodb://{username}:{password}@localhost:27017/"
            self.client = pymongo.MongoClient(uri)
        else:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client[db]
        self.collection = self.database[col]

    def insert_elements(self, data_json, keyword, language):
        """Inserta elementos en la colección desde un JSON, añadiendo información sobre la keyword y language."""
        try:
            documents = [
                {
                    "name": edge["node"]["name"],
                    "owner": edge["node"]["owner"]["login"],
                    "stargazers": edge["node"]["stargazers"]["totalCount"],
                    "keyword": keyword,  # Añade el keyword al documento
                    "language": language  # Añade el lenguaje al documento
                }
                for edge in data_json["data"]["search"]["edges"]
            ]
            self.collection.insert_many(documents)
        except Exception as e:
            print(f"Error al insertar elementos: {e}")

