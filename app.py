from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')  # specify the template folder


# Replace this with your actual TMDb API key
TMDB_API_KEY = "ad732a2fac5925fc1e6bc5707b44483a"

# TMDb base URL
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Route to render home page
@app.route('/')
def home():
    return render_template('index2.html')
from flask import redirect, url_for


# Route to search for movies
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Make a request to TMDb API to search for movies
    response = requests.get(f'{TMDB_BASE_URL}/search/movie', params={'api_key': TMDB_API_KEY, 'query': query})
    data = response.json()['results']
    return render_template('search_results.html', movies=data)

# Replace this with your actual YouTube API key
YOUTUBE_API_KEY = "your_youtube_api_key"

# Route to get movie details and play video
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    try:
        # Make a request to TMDb API to get movie details
        movie_response = requests.get(f'{TMDB_BASE_URL}/movie/{movie_id}', params={'api_key': TMDB_API_KEY})
        movie_response.raise_for_status()  # Raise an exception for HTTP errors

        movie_data = movie_response.json()

        # Fetch video key for the trailer (assuming it's available in the response)
        video_key = None
        if 'videos' in movie_data and movie_data['videos']['results']:
            video_key = movie_data['videos']['results'][0]['key']

        # Fetch YouTube trailer URL using the YouTube API
        youtube_trailer_url = get_youtube_trailer_url(movie_data['title'])

        return render_template('movie_details.html', movie=movie_data, video_key=video_key, youtube_trailer_url=youtube_trailer_url)
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        return f"Error: Unable to fetch details for movie with ID {movie_id}. {e}"

def get_youtube_trailer_url(movie_title):
    # Use the YouTube API to search for movie trailers
    youtube_api_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': f'{movie_title} official trailer',
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 1,
    }
    response = requests.get(youtube_api_url, params=params)
    response_data = response.json()
    
    # Extract the video ID from the API response
    video_id = response_data['items'][0]['id']['videoId'] if 'items' in response_data and response_data['items'] else None

    # Construct the YouTube trailer URL
    youtube_trailer_url = f'https://www.youtube.com/watch?v={video_id}' if video_id else None

    return youtube_trailer_url

if __name__ == '__main__':
    app.run(debug=True)
