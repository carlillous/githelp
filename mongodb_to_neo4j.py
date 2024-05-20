# mongodb_to_neo4j.py
from mongodb.mongo_client import MongoDBClient
from neo4j_integration.neo4j_loader import *

def main():
    mongo_username = "carlosmenegg"
    mongo_password = "agcnc7SuS7f9BPou"
    mongo_db = "github_data"
    mongo_col = "repositories"
    mongo_client = MongoDBClient(mongo_db, mongo_col, username=mongo_username, password=mongo_password)

    #probar +s o +ssc: https://stackoverflow.com/questions/73025684/unable-to-retrieve-routing-information-neo4j
    neo4j_uri = "neo4j+ssc://b47768d5.databases.neo4j.io:"
    neo4j_user = "neo4j"
    neo4j_pass = "4I9XJHCkbj3zth9vf3POnpU6byO9cIjboda_aUwLC3k"

    loader = Neo4JLoader(neo4j_uri, neo4j_user, neo4j_pass, mongo_client, mongo_db)
    loader.transfer_repositories()
    loader.transfer_users()
    #loader.transfer_user_network()


if __name__ == "__main__":
    main()
