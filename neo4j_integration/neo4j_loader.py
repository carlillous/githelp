from pymongo import MongoClient
from .neo4j_connection import Neo4JConnection
from .data_parser import DataParser

class Neo4JLoader:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_pass, mongo_client, mongo_db):
        self.neo4j_conn = Neo4JConnection(neo4j_uri, neo4j_user, neo4j_pass)
        self.mongo_client = mongo_client
        self.mongo_db = self.mongo_client[mongo_db]

    def transfer_repositories(self):
        """Transfiere repositorios de MongoDB a Neo4J."""
        documents = self.mongo_db.repositories.find()
        try:
            with self.neo4j_conn.driver.session() as session:
                for doc in documents:
                    parsed_doc = DataParser.parse_repository(doc)
                    session.write_transaction(self.create_and_link_repo, parsed_doc)
        finally:
            self.neo4j_conn.close()

    def transfer_users(self):
        """Transfiere usuarios de MongoDB a Neo4J."""
        documents = self.mongo_db.users.find()
        try:
            with self.neo4j_conn.driver.session() as session:
                for doc in documents:
                    parsed_doc = DataParser.parse_user(doc)
                    session.write_transaction(self.create_user, parsed_doc)
        finally:
            self.neo4j_conn.close()

    def transfer_user_network(self):
        """Transfiere la red de seguidores y seguidos de MongoDB a Neo4J."""
        documents = self.mongo_db.network.find()
        try:
            with self.neo4j_conn.driver.session() as session:
                for doc in documents:
                    parsed_doc = DataParser.parse_network(doc)
                    session.write_transaction(self.create_and_link_network, parsed_doc)
        finally:
            self.neo4j_conn.close()

    @staticmethod
    def create_and_link_repo(tx, doc):
        query = """
        MERGE (repo:Repository {name: $name})
        MERGE (user:User {login: $owner})
        MERGE (lang:Language {name: $language})
        MERGE (kw:Keyword {key_word:$keyword})
        MERGE (repo)-[:OWNED_BY]->(user)
        MERGE (repo)-[:USES_LANGUAGE]->(lang)
        MERGE (repo)-[:HAS_KEYWORD]->(kw)
        SET repo.stargazers = $stargazers, repo.issues = $issues, repo.forks = $forks
        """
        tx.run(query, name=doc["name"], owner=doc["owner"], stargazers=doc["stargazers"],
               issues=doc["issues"], forks=doc["forks"], keyword=doc["keyword"], language=doc["language"])

    @staticmethod
    def create_user(tx, doc):
        query = """
        MERGE (user:User {login: $login})
        SET user.name = $name, user.company = $company, user.following_count = $following, 
            user.followers_count = $followers, user.repositories_count = $repositories
        """
        tx.run(query, login=doc["login"], name=doc.get("name"), company=doc.get("company"),
               following=doc["following"], followers=doc["followers"], repositories=doc["repositories"])

    @staticmethod
    def create_and_link_network(tx, doc):
        username = doc["username"]
        following = doc["following"]
        followers = doc["followers"]

        for follow in following:
            query = """
            MERGE (user:User {login: $username})
            MERGE (follow:User {login: $follow})
            MERGE (user)-[:FOLLOWS]->(follow)
            """
            tx.run(query, username=username, follow=follow)

        for follower in followers:
            query = """
            MERGE (user:User {login: $username})
            MERGE (follower:User {login: $follower})
            MERGE (follower)-[:FOLLOWS]->(user)
            """
            tx.run(query, username=username, follower=follower)
