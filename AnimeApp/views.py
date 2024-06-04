from django.shortcuts import render, get_object_or_404
from .models import Anime, Character, AnimeImage
import requests

def home(request):
    return render(request, 'AnimeApp/base.html')

def search_anime(request):
    """
    Searches for anime based on the user's input using an external API.
    """
    if request.method == 'GET':
        search_query = request.GET.get('search')

        # Construct GraphQL query
        query = """
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                }
                description (asHtml: false)
                # Add other fields you want to retrieve
            }
        }
        """

        variables = {'search': search_query}

        # Prepare the request data
        data = {'query': query, 'variables': variables}

        # Send a POST request
        response = requests.post('https://graphql.anilist.co', json=data)
        print(f'SEARCHED_RESULTS for {search_query}',response.content)

        if response.status_code == 200:
            data = response.json()
            matched_animes = data.get('data', {}).get('Media', [])
            print('Matched animes',matched_animes)
            return render(request, 'AnimeApp/search_results.html', {'matched_animes': matched_animes, 'query': search_query})
        else:
            return render(request, 'AnimeApp/error.html', {"message": "Failed to fetch data from API"})
    else:
        return render(request, 'AnimeApp/error.html', {"message": "Invalid request"})
def fetch_anime_data(request, sort_by='POPULARITY_DESC'):
    """
    Fetches anime data from AniList GraphQL API using the provided query and variables.
    Renders the fetched data directly in the template.
    """
    import requests
    query = '''
    query ($sort: [MediaSort], $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            media (sort: $sort) {
                id
                title {
                    romaji
                }
                description
                coverImage {
                    extraLarge
                }
            }
        }
    }
    '''
    variables = {
        'sort': sort_by,
        'page': 1,
        'perPage': 50,
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json().get("data", {})
        animes_data = data.get("Page", {}).get("media", [])
        return render(request, "AnimeApp/anime_list.html", {"animes": animes_data})
    else:
        return render(request, "AnimeApp/error.html", {"message": "Failed to fetch data"})
def anime_detail(request, mal_id):
    """
    Fetches anime details from AniList GraphQL API using the provided query and variables.
    Renders the fetched data directly in the template.
    """
    query = '''
    query ($id: Int) {
        Media (id: $id) {
            title {
                romaji
            }
            description
            averageScore
            episodes
            coverImage {
                extraLarge
            }
            characters {
                nodes {
                    name {
                        full
                    }
                    image {
                        large
                    }
                    id
                }
            }
        }
    }
    '''
    variables = {
        'id': mal_id,
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    print('ANIME DETAIL RESPONSE<CONTENT: ', response.content)
    if response.status_code == 200:
        data = response.json().get("data", {})
        anime_data = data.get("Media", {})
        return render(request, "AnimeApp/anime_detail.html", {"anime": anime_data})
    else:
        return render(request, "AnimeApp/error.html", {"message": "Failed to fetch data"})

# def recommendations(request):
#     # Get user preferences (e.g., liked anime, watched anime)
#     liked_anime = Anime.objects.filter(...)  # Replace with your logic to get liked anime

#     # Create a TF-IDF matrix from anime synopses
#     tfidf = TfidfVectorizer(stop_words='english')
#     anime_synopses = Anime.objects.values_list('synopsis', flat=True)
#     tfidf_matrix = tfidf.fit_transform(anime_synopses)

#     # Compute the cosine similarity matrix
#     cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#     # Get the indices of the liked anime
#     liked_anime_indices = [anime.pk - 1 for anime in liked_anime]

#     # Calculate the similarity scores for the liked anime
#     similarity_scores = cosine_sim[liked_anime_indices].sum(axis=0) / len(liked_anime_indices)

#     # Sort the similarity scores in descending order
#     sorted_indices = similarity_scores.argsort()[::-1]

#     # Get the recommended anime based on the sorted indices
#     recommended_anime_indices = sorted_indices[len(liked_anime):]
#     recommended_animes = [Anime.objects.get(pk=index + 1) for index in recommended_anime_indices]

#     return render(request, 'AnimeApp/recommendations.html', {'recommended_animes': recommended_animes})
import requests
from django.shortcuts import render

def character_detail(request, character_id):
    url = "https://graphql.anilist.co"
    query = '''
    query ($id: Int) {
      Character(id: $id) {
        id
        name {
          full
          native
        }
        age
        gender
        dateOfBirth {
          year
          month
          day
        }
        bloodType
        image {
          large
          medium
        }
      }
    }
    '''
    variables = {'id': character_id}
    response = requests.post(url, json={"query": query, "variables": variables})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("Character", {})
        if data:
            return render(request, 'AnimeApp/character_detail.html', {'character': data})
        else:
            return render(request, "AnimeApp/error.html", {"message": "No character data found"})
    else:
        print(f"Error: {response.status_code}")
        print(response.json())  # Print the response content for debugging
        return render(request, "AnimeApp/error.html", {"message": "Failed to fetch character data"})
import requests
from django.shortcuts import render
from datetime import datetime

def get_next_season_and_year():
    now = datetime.now()
    month = now.month
    if 1 <= month <= 3:
        return 'WINTER', now.year
    elif 4 <= month <= 6:
        return 'SPRING', now.year
    elif 7 <= month <= 9:
        return 'SUMMER', now.year
    else:
        return 'FALL', now.year

def upcoming_anime(request):
    query = '''
    query ($season: MediaSeason, $seasonYear: Int, $sort: [MediaSort], $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (season: $season, seasonYear: $seasonYear, sort: $sort) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                characters(page: 1, perPage: 10) {
                    nodes {
                        id
                        name { full }
                        image { large }
                    }
                }
                coverImage {
                    extraLarge
                }
            }
        }
    }
    '''

    season, season_year = get_next_season_and_year()
    
    variables = {
        'season': season,
        'seasonYear': season_year,
        'sort': ['POPULARITY_DESC'],
        'page': 1,
        'perPage': 50,
    }

    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("Page", {}).get("media", [])
        return render(request, 'AnimeApp/upcoming_anime_list.html', {'animes': data})
    else:
        return render(request, 'AnimeApp/error.html', {'message': 'Failed to fetch data'})

def fetch_anime_by_genre(request, genre):
    """
    Fetches anime data from AniList GraphQL API based on the provided genre.
    Renders the fetched data directly in the template.
    """
    query = '''
    query ($genre: String, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            media (genre: $genre) {
                id
                title {
                    romaji
                }
                description
                coverImage {
                    extraLarge
                }
            }
        }
    }
    '''
    variables = {
        'genre': genre.upper(),
        'page': 1,
        'perPage': 50,
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    print('GENRE RESPONSE:', response.content)
    if response.status_code == 200:
        data = response.json().get("data", {})
        animes_data = data.get("Page", {}).get("media", [])
        return render(request, "AnimeApp/anime_list.html", {"animes": animes_data, "genre": genre})
    else:
        return render(request, "AnimeApp/error.html", {"message": "Failed to fetch data"})
    
def fetch_anime_by_year(request, year):
    """
    Fetches anime data from AniList GraphQL API based on the provided year.
    Renders the fetched data directly in the template.
    """
    query = '''
    query ($year: Int, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            media (seasonYear: $year) {
                id
                title {
                    romaji
                }
                description
                coverImage {
                    extraLarge
                }
            }
        }
    }
    '''
    variables = {
        'year': year,
        'page': 1,
        'perPage': 50,
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json().get("data", {})
        animes_data = data.get("Page", {}).get("media", [])
        return render(request, "AnimeApp/anime_list.html", {"animes": animes_data, "year": year})
    else:
        return render(request, "AnimeApp/error.html", {"message": "Failed to fetch data"})

     
