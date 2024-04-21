import requests
import json

# Your personal access token
token = 'YOUR_PERSONAL_ACCESS_TOKEN'

# GraphQL query as a multi-line string
query = """
query {
  user(login: "octocat") {
    name
    repositories(first: 5, privacy: PUBLIC) {
      totalCount
      nodes {
        name
        description
        url
        stargazers {
          totalCount
        }
        watchers {
          totalCount
        }
        forkCount
      }
    }
  }
}
"""

# Headers including the Authorization token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# The endpoint for the GitHub GraphQL API
url = 'https://api.github.com/graphql'

# Make a POST request to the GitHub API with the query
response = requests.post(url, headers=headers, json={'query': query})

# Check if the request was successful
if response.status_code == 200:
    # Print the formatted JSON response
    print(json.dumps(response.json(), indent=2))
else:
    # If the request failed, print the error
    print(f"Failed to execute GraphQL query: {response.status_code}")
    print(response.json())
