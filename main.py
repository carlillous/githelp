from graphqlapi.graphql_client import GraphQLClient
from mongodb.mongo_client import MongoDBClient
import json

if __name__ == "__main__":
    # Cliente Github
    token = "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"
    graphql_client = GraphQLClient(token)

    # Cliente Mongo con autenticacion
    mongo_username = "root"
    mongo_password = "admin"
    mongo_client = MongoDBClient("github_data", "repositories", username=mongo_username, password=mongo_password)
    # Ejecutar consulta y almacenar en MongoDB
    try:
        # Realiza la consulta utilizando parámetros personalizados
        result = graphql_client.search_repositories(keyword="chatgpt", language="Python", stars=10000, first=5)
        print(json.dumps(result, indent=4))

        # Inserta los resultados en MongoDB
        mongo_client.insert_elements(result)

    except Exception as e:
        print(e)
