# mongodb_to_neo4j.py
from mongodb.mongo_client import MongoDBClient
from neo4j_integration.mongo_to_neo4j import transfer_to_neo4j
#TODO: MONGO INTO NEO4J WITHOUT FILTER
def main():
    mongo_username = "root"
    mongo_password = "admin"
    mongo_db = "github_data"
    mongo_col = "repositories"
    mongo_client = MongoDBClient(mongo_db, mongo_col, username=mongo_username, password=mongo_password)

    languages = ["Python", "C"]
    keywords = ["e-commerce", "machine learning"]
    min_stars = 1000
    documents = mongo_client.find_documents(languages, keywords, min_stars)

    #probar +s o +ssc: https://stackoverflow.com/questions/73025684/unable-to-retrieve-routing-information-neo4j
    neo4j_uri = "neo4j+ssc://761fb7e4.databases.neo4j.io:"
    neo4j_user = "neo4j"
    neo4j_pass = "bUamNfpq4UTlaV1A15xaDf0Tv0oebuQYOKhtX5O068Q"

    transfer_to_neo4j(neo4j_uri, neo4j_user, neo4j_pass, documents)

if __name__ == "__main__":
    main()
