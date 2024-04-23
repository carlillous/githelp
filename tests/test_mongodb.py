from graphqlapi.graphql_client import GraphQLClient
from mongodb.mongo_client import MongoDBClient
import json

if __name__ == "__main__":
    token = "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"  # Token should ideally be handled more securely
    graphql = GraphQLClient(token)

    query = """
    {
      search(query: "chatgpt OR CHATGPT OR GPT OR gpt in:readme in:description in:name language:Python stars:>10000", type: REPOSITORY, first: 5) {
        edges {
          node {
            ... on Repository {
              name
              owner {
                login
              }
              stargazers {
                totalCount
              }
            }
          }
        }
      }
    }
    """

    try:
        result = graphql.run_query(query)
        print(json.dumps(result, indent=4))
        mongo = MongoDBClient("data","test","root","admin")
        mongo.insert_elements(result)
    except Exception as e:
        print(e)