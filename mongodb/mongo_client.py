import pymongo

class MongoDBClient:
    def __init__(self, db, col, username=None, password=None):
        uri = f"mongodb+srv://{username}:{password}@githelp.ftkgizk.mongodb.net/?retryWrites=true&w=majority&appName=githelp"
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[db]
        self.collection = self.database[col]

    def insert_repositories(self, data_json, keyword, language):
        """Inserta repositorios en la colección desde un JSON, añadiendo información sobre la keyword y language."""
        try:
            documents = [
                {
                    "name": edge["node"]["name"],
                    "owner": edge["node"]["owner"]["login"],
                    "stargazers": edge["node"]["stargazers"]["totalCount"],
                    "issues": edge["node"]["issues"]["totalCount"],
                    "forks": edge["node"]["forks"]["totalCount"],
                    "keyword": keyword,
                    "language": language
                }
                for edge in data_json["data"]["search"]["edges"]
            ]
            self.collection.insert_many(documents)
        except Exception as e:
            print(f"Error al insertar repositorios: {e}")

    def insert_users(self, data_json):
        """Inserta usuarios en la colección desde un JSON, añadiendo información sobre la keyword."""
        try:
            documents = [
                {
                    "login": edge["node"]["login"],
                    "name": edge["node"].get("name"),
                    "company": edge["node"].get("company"),
                    "following": edge["node"]["following"]["totalCount"],
                    "followers": edge["node"]["followers"]["totalCount"],
                    "repositories": edge["node"]["repositories"]["totalCount"],
                }
                for edge in data_json["data"]["search"]["edges"]
            ]
            self.collection.insert_many(documents)
        except Exception as e:
            print(f"Error al insertar usuarios: {e}")

    def insert_user_network(self, data_json, username):
        """Inserta la red de seguidores y seguidos de un usuario en la colección desde un JSON."""
        try:
            following = [
                edge["node"]["login"]
                for edge in data_json["data"]["user"]["following"]["edges"]
            ]
            followers = [
                edge["node"]["login"]
                for edge in data_json["data"]["user"]["followers"]["edges"]
            ]

            document = {
                "username": username,
                "following": following,
                "followers": followers
            }

            self.collection.update_one(
                {"username": username},
                {"$set": document},
                upsert=True
            )
        except Exception as e:
            print(f"Error al insertar la red de usuarios: {e}")

    def find_documents(self, languages=None, keywords=None, min_stars=None):
        """Busca documentos en la colección utilizando un filtro específico."""
        try:
            filter = {}
            if languages:
                filter['language'] = {'$in': languages}
            if keywords:
                filter['keyword'] = {'$in': keywords}
            if min_stars is not None:
                filter['stargazers'] = {'$gte': min_stars}
            return list(self.collection.find(filter))
        except Exception as e:
            print(f"Error al buscar documentos: {e}")
            return []
