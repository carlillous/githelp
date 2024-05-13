from neo4j_integration.neo4j_manager import Neo4JManager

uri = "neo4j+ssc://761fb7e4.databases.neo4j.io:"
user = "neo4j"
password = "bUamNfpq4UTlaV1A15xaDf0Tv0oebuQYOKhtX5O068Q"
neo4j_manager = Neo4JManager(uri, user, password)
try:
    results = neo4j_manager.get_top_users_by_degree()
    for result in results:
        print(f"User: {result['u']['login']}, Degree: {result['degree']}")
finally:
        neo4j_manager.driver.close()