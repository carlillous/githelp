from graphqlapi.graphql_client import GraphQLClient
from mongodb.mongo_client import MongoDBClient
import json
from tqdm import tqdm

def main():
    # Cliente Github
    token = "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"
    graphql_client = GraphQLClient(token)

    # Cliente Mongo con autenticación
    mongo_username = "carlosmenegg"
    mongo_password = "agcnc7SuS7f9BPou"
    mongo_client = MongoDBClient("github_data",  username=mongo_username, password=mongo_password)

    # Definición de keywords y lenguajes
    keywords = [
        "chatgpt", "databases", "scrum", "kaggle", "machine learning", "neural network",
        "parallelization", "big data", "blockchain", "cybersecurity", "deep learning",
        "quantum computing", "cloud computing", "IoT", "augmented reality", "virtual reality",
        "API", "e-commerce", "microservices", "DevOps", "docker",
        "kubernetes", "tensorflow", "pytorch", "data visualization", "graphic design",
        "UX/UI", "automation", "robotics", "ethical hacking"
    ]
    languages = [
        "Python", "Java", "C", "C++", "Javascript", "HTML", "CSS", "Swift", "Kotlin",
        "Go", "Rust", "Ruby", "PHP", "TypeScript", "Scala", "Perl", "Lua", "Matlab",
        "R", "SQL", "Bash", "Shell", "PowerShell", "Elixir", "Erlang", "Haskell", "Objective-C"
    ]

    # Ejecución de consultas y almacenamiento en MongoDB
    for keyword in tqdm(keywords, desc="Processing Keywords"):
        for language in tqdm(languages, desc="Languages", leave=False):
            try:
                #Repositorios
                repos_data = graphql_client.search_repositories(keyword=keyword, language=language, stars=300, first=15)
                mongo_client.insert_repositories(repos_data, keyword, language)

                owners = [edge["node"]["owner"]["login"] for edge in repos_data["data"]["search"]["edges"]]

                #Consultas a los usuarios
                for owner in owners:
                    user_data = graphql_client.search_user(owner)
                    mongo_client.insert_users(user_data)

                #Consultas a su network
                #    for user_edge in user_data["data"]["search"]["edges"]:
                #        user_login = user_edge["node"]["login"]
                #        user_network = graphql_client.get_user_network(user_login)
                #        mongo_client.insert_user_network(user_network)

            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
