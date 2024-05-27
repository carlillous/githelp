import requests
import json

class GraphQLClient:
    def __init__(self, token):
        """Initializes the GraphQL client with the provided GitHub token."""
        self.token = token
        self.url = 'https://api.github.com/graphql'

    def run_query(self, query):
        """Executes a GraphQL query against the GitHub API."""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        request = requests.post(self.url, headers=headers, json={'query': query})

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(f"Query failed with status code {request.status_code} and message: {request.text}")

    def search_repositories(self, keyword, language='Python', stars=10000, first=5):
        """Searches repositories based on a keyword and other criteria."""
        query = f"""
        {{
          search(query: "{keyword} in:readme in:description in:name language:{language} stars:>{stars}", type: REPOSITORY, first: {first}) {{
            edges {{
              node {{
                ... on Repository {{
                  name
                  owner {{
                    login
                  }}
                  stargazers {{
                    totalCount
                  }}
                  issues {{
                    totalCount
                  }}
                  forks {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        return self.run_query(query)

    def search_user(self, username):
        """Searches a user based on a username."""
        query = f"""
        {{
          search(query: "{username} in:login", type: USER, first: 1) {{
            edges {{
              node {{
                ... on User {{
                  login
                  name
                  company
                  following {{
                    totalCount
                  }}
                  followers {{
                    totalCount
                  }}
                  repositories {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        return self.run_query(query)

    def get_user_network(self, username):
        """Gets the network of following and followers of a user, with pagination to fetch all."""
        following = []
        followers = []
        has_next_following = True
        has_next_followers = True
        end_cursor_following = None
        end_cursor_followers = None

        while has_next_following or has_next_followers:
            query = f"""
            {{
              user(login: "{username}") {{
                following(first: 100, after: {json.dumps(end_cursor_following)}) {{
                  totalCount
                  pageInfo {{
                    hasNextPage
                    endCursor
                  }}
                  edges {{
                    node {{
                      login
                    }}
                  }}
                }}
                followers(first: 100, after: {json.dumps(end_cursor_followers)}) {{
                  totalCount
                  pageInfo {{
                    hasNextPage
                    endCursor
                  }}
                  edges {{
                    node {{
                      login
                    }}
                  }}
                }}
              }}
            }}
            """
            result = self.run_query(query)
            user_data = result["data"]["user"]

            # Process following
            if has_next_following:
                following_edges = user_data["following"]["edges"]
                following.extend([edge["node"]["login"] for edge in following_edges])
                has_next_following = user_data["following"]["pageInfo"]["hasNextPage"]
                end_cursor_following = user_data["following"]["pageInfo"]["endCursor"]

            # Process followers
            if has_next_followers:
                followers_edges = user_data["followers"]["edges"]
                followers.extend([edge["node"]["login"] for edge in followers_edges])
                has_next_followers = user_data["followers"]["pageInfo"]["hasNextPage"]
                end_cursor_followers = user_data["followers"]["pageInfo"]["endCursor"]

        return {"username": username, "following": following, "followers": followers}


