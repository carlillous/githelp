# mongodb_to_neo4j.py
from dotenv import load_dotenv

from mongodb.mongo_client import MongoDBClient
from neo4j_integration.neo4j_loader import *
import os

def main():
    load_dotenv()
    mongo_username = os.getenv('MONGO_USER')
    mongo_password = os.getenv('MONGO_PASSWORD')
    mongo_db = "github_data"
    mongo_client = MongoDBClient(mongo_db, username=mongo_username, password=mongo_password)

    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_pass = os.getenv('NEO4J_PASSWORD')

    loader = Neo4JLoader(neo4j_user, neo4j_pass, mongo_client)
    loader.transfer_repositories()
    loader.transfer_users()
    #loader.transfer_user_network()


if __name__ == "__main__":
    main()
