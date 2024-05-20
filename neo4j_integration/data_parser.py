# neo4j_integration/data_parser.py
class DataParser:
    @staticmethod
    def parse_repository(doc):
        """Transforma un documento de repositorio de MongoDB para ser compatible con Neo4J."""
        parsed_doc = {
            "name": doc.get("name", ""),
            "owner": doc.get("owner", ""),
            "stargazers": doc.get("stargazers", 0),
            "issues": doc.get("issues", 0),
            "forks": doc.get("forks", 0),
            "keyword": doc.get("keyword", ""),
            "language": doc.get("language", "")
        }
        return parsed_doc

    @staticmethod
    def parse_user(doc):
        """Transforma un documento de usuario de MongoDB para ser compatible con Neo4J."""
        parsed_doc = {
            "login": doc.get("login", ""),
            "name": doc.get("name", ""),
            "company": doc.get("company", ""),
            "following": doc.get("following", 0),
            "followers": doc.get("followers", 0),
            "repositories": doc.get("repositories", 0)
        }
        return parsed_doc

    @staticmethod
    def parse_network(doc):
        """Transforma un documento de red de usuarios de MongoDB para ser compatible con Neo4J."""
        parsed_doc = {
            "username": doc.get("username", ""),
            "following": doc.get("following", []),
            "followers": doc.get("followers", [])
        }
        return parsed_doc
