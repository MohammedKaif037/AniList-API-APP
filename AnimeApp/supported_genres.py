import requests

url = "https://graphql.anilist.co"
query = '''
query {
  GenreCollection
}
'''

response = requests.post(url, json={"query": query})
if response.status_code == 200:
    genres = response.json().get("data", {}).get("GenreCollection", [])
    print("Supported Genres:", genres)
else:
    print("Failed to fetch genres")
