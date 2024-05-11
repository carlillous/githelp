# neo4j_integration/data_parser.py

class DataParser:
    @staticmethod
    def parse_document(doc):
        """Transforma un documento de MongoDB para ser compatible con Neo4J."""
        # Preparar el documento para Neo4J, eliminando o transformando campos no deseados
        parsed_doc = {
            "name": doc.get("name", ""),
            "owner": doc.get("owner", ""),
            "stargazers": doc.get("stargazers", 0),
            "keyword": doc.get("keyword", ""),
            "language": doc.get("language", "")
        }
        return parsed_doc