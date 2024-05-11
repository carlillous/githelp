from neo4j import GraphDatabase

class Neo4JConnection:
    def __init__(self, uri, username, password):
        """Initialize a connection to the Neo4j database using the provided URI and credentials."""
        self.driver = None
        try:
            # Create a driver instance
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
        except Exception as e:
            print(f"Failed to create a Neo4J driver: {e}")

    def close(self):
        """Close the Neo4j driver connection."""
        if self.driver is not None:
            self.driver.close()

    def session(self):
        """Provide a context-managed Neo4j session."""
        return self.driver.session()
