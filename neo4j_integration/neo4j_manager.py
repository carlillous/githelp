# Filename: neo4j_manager.py
from neo4j_integration.neo4j_connection import Neo4JConnection

class Neo4JManager:
    def __init__(self, uri, user, password):
        self.driver = Neo4JConnection(uri,user,password)

    def get_top_users_by_degree(self):
        query = """
        MATCH (u:User)-[r]-()
        WITH u, COUNT(r) AS degree
        RETURN u, degree
        ORDER BY degree DESC
        LIMIT 3
        """
        return self.driver.query(query)

