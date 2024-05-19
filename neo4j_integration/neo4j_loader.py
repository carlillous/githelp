# neo4j_integration/mongo_to_neo4j.py
from .neo4j_connection import Neo4JConnection
from .data_parser import DataParser

#TODO: REFACTOR THIS CLASS FOR NEW QUERIES
def transfer_to_neo4j(neo4j_uri, neo4j_user, neo4j_pass, documents):
    neo4j_conn = Neo4JConnection(neo4j_uri, neo4j_user, neo4j_pass)

    try:
        with neo4j_conn.driver.session() as session:
            for doc in documents:
                parsed_doc = DataParser.parse_document(doc)
                session.write_transaction(create_and_link, parsed_doc)
    finally:
        neo4j_conn.close()


def create_and_link(tx, doc):
    query = """
    MERGE (repo:Repository {name: $name})
    MERGE (user:User {login: $owner})
    MERGE (lang:Language {name: $language})
    MERGE (kw:Keyword {key_word:$keyword})
    MERGE (repo)-[:OWNED_BY]->(user)
    MERGE (user)-[:USES_LANGUAGE]->(lang)
    MERGE (user)-[:INTERESTED_IN_KEYWORD]->(kw)
    
    SET repo.stargazers = $stargazers, repo.keyword = $keyword, repo.language = $language
    """
    tx.run(query, name=doc["name"], owner=doc["owner"], stargazers=doc["stargazers"], keyword=doc["keyword"],
           language=doc["language"])
