from neo4j_integration.neo4j_manager import Neo4JManager

uri = ""
user = ""
password = ""
neo4j_manager = Neo4JManager(uri, user, password)
try:
    results = neo4j_manager.get_top_users_by_degree()
    for result in results:
        print(f"User: {result['u']['login']}, Degree: {result['degree']}")
finally:
        neo4j_manager.driver.close()