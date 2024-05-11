# run_integration.py
from mongodb.mongo_client import MongoDBClient
from neo4j_integration.mongo_to_neo4j import transfer_to_neo4j

def main():
    mongo_username = "root"
    mongo_password = "admin"
    mongo_db = "github_data"
    mongo_col = "repositories"
    mongo_client = MongoDBClient(mongo_db, mongo_col, username=mongo_username, password=mongo_password)

    filter = {"language": "Python", "keyword": "chatgpt"}
    documents = mongo_client.find_documents(filter)

    neo4j_uri = "neo4j+s://b47768d5.databases.neo4j.io"
    neo4j_user = "neo4j"
    neo4j_pass = "4I9XJHCkbj3zth9vf3POnpU6byO9cIjboda_aUwLC3k"

    transfer_to_neo4j(neo4j_uri, neo4j_user, neo4j_pass, documents)

if __name__ == "__main__":
    main()
