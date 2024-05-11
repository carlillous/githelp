from graphqlapi.graphql_client import GraphQLClient
from mongodb.mongo_client import MongoDBClient
import json

def main():
    # Cliente Github
    token = "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"
    graphql_client = GraphQLClient(token)

    # Cliente Mongo con autenticación
    mongo_username = "root"
    mongo_password = "admin"
    mongo_client = MongoDBClient("github_data", "repositories", username=mongo_username, password=mongo_password)

    # Definición de keywords y lenguajes
    keywords = ["chatgpt", "databases", "scrum", "kaggle", "machine learning", "neural network"]
    languages = ["Python", "Java", "C", "C++", "Javascript"]

    # Ejecución de consultas y almacenamiento en MongoDB
    for keyword in keywords:
        for language in languages:
            print("Searching for", keyword, "and language", language)
            try:
                # Realiza la consulta utilizando parámetros personalizados
                result = graphql_client.search_repositories(keyword=keyword, language=language, stars=1000, first=5)
                print(json.dumps(result, indent=4))

                # Inserta los resultados en MongoDB, añadiendo keyword y language
                mongo_client.insert_elements(result, keyword, language)

            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
