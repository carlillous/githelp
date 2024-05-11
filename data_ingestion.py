from graphqlapi.graphql_client import GraphQLClient
from mongodb.mongo_client import MongoDBClient
import json
from tqdm import tqdm

def main():
    # Cliente Github
    token = "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"
    graphql_client = GraphQLClient(token)

    # Cliente Mongo con autenticación
    mongo_username = "root"
    mongo_password = "admin"
    mongo_client = MongoDBClient("github_data", "repositories", username=mongo_username, password=mongo_password)

    # Definición de keywords y lenguajes
    keywords = [
        "chatgpt", "databases", "scrum", "kaggle", "machine learning", "neural network",
        "parallelization", "big data", "blockchain", "cybersecurity", "deep learning",
        "quantum computing", "cloud computing", "IoT", "augmented reality", "virtual reality",
        "API", "e-commerce", "microservices", "DevOps", "react", "node.js", "docker",
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
                # Realiza la consulta utilizando parámetros personalizados
                result = graphql_client.search_repositories(keyword=keyword, language=language, stars=100, first=25)
                # Inserta los resultados en MongoDB, añadiendo keyword y language
                mongo_client.insert_elements(result, keyword, language)

            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
