import requests
import json


class GraphQLClient:
    def __init__(self, token):
        self.token = token
        self.url = 'https://api.github.com/graphql'

    def run_query(self, query):
        # Headers including the Authorization token
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # JSON body with the GraphQL query
        request = requests.post(self.url, headers=headers, json={'query': query})

        # Check if the request was successful
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(f"Query failed with status code {request.status_code} and message: {request.text}")



if __name__ == "__main__":
    token = "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"  # Token should ideally be handled more securely
    graphql = (token)

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
    except Exception as e:
        print(e)

