import requests

# The GitHub API URL for listing a user's public repositories
user = 'carlillous'
url = f'https://api.github.com/users/{user}/repos'

# Make a GET request to the GitHub API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    repositories = response.json()

    # Print the name and URL of each repository
    for repo in repositories:
        print(f"Name: {repo['name']}")
        print(f"URL: {repo['html_url']}\n")
else:
    # If the request failed, print the error
    print(f"Failed to fetch repositories: {response.status_code}")
    print(response.json())
