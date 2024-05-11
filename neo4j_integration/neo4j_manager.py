# Filename: neo4j_manager.py
from neo4j import GraphDatabase

class Neo4JManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    def get_top_users_by_degree(self):
        query = """
        MATCH (u:User)-[r]-()
        WITH u, COUNT(r) AS degree
        RETURN u, degree
        ORDER BY degree DESC
        LIMIT 3
        """
        return self.run_query(query)

def main():
    uri = "neo4j+ssc://761fb7e4.databases.neo4j.io:"
    user = "neo4j"
    password = "bUamNfpq4UTlaV1A15xaDf0Tv0oebuQYOKhtX5O068Q"
    neo4j_manager = Neo4JManager(uri, user, password)
    try:
        results = neo4j_manager.get_top_users_by_degree()
        for result in results:
            print(f"User: {result['u']['login']}, Degree: {result['degree']}")
    finally:
        neo4j_manager.close()

if __name__ == "__main__":
    main()
