from mongodb.mongo_client import MongoDBClient

def main():
    # Cliente Mongo con autenticación
    mongo_username = "root"
    mongo_password = "admin"
    mongo_client = MongoDBClient("github_data", "repositories", username=mongo_username, password=mongo_password)

    # Ejemplo de consulta
    language = "Python"
    keyword = "chatgpt"
    filter = {"language": language, "keyword": keyword}

    results = mongo_client.find_documents(filter)

    # Imprime los resultados de la consulta
    for doc in results:
        print(doc)


if __name__ == "__main__":
    main()
