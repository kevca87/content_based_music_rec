import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
API_KEY = os.getenv('MUSIXMATCH_API_KEY')

# Define the API endpoint
API_URL = 'https://api.musixmatch.com/ws/1.1'
API_GET_LYRICS_ENDPOINT = f'{API_URL}/track.lyrics.get'
API_GET_TRACK_ENDPOINT = f'{API_URL}/track.get'


def get_lyrics(track_isrc):
    # Define the parameters for the API request
    params = {
        'apikey': API_KEY,
        'track_isrc': track_isrc
    }
    # Make the API request
    response = requests.get(API_GET_LYRICS_ENDPOINT, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        lyrics = data['message']['body']['lyrics']
        # remove '\n******* This Lyrics is NOT for Commercial use *******'
        lyrics_body = lyrics['lyrics_body'][0:-54]
        lyrics_id = lyrics['lyrics_id']
        return {'track_isrc': track_isrc, 'lyrics_id': lyrics_id, 'lyrics_body': lyrics_body}
    else:
        print(f"Error: {response.status_code}")

def get_track_metadata(track_isrc):
    # Define the parameters for the API request
    params = {
        'apikey': API_KEY,
        'track_isrc': track_isrc
    }
    # Make the API request
    response = requests.get(API_GET_TRACK_ENDPOINT, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        track = data['message']['body']['track']
        return {'track_isrc': track_isrc, 'has_lyrics':track['has_lyrics'], 'instrumental':track['instrumental'], 'explicit':track['explicit'], 'genres': track['primary_genres']}
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    # Example usage
    track_isrc = 'USUM71703861'
    lyrics = get_lyrics(track_isrc)
    print(lyrics)
    metadata = get_track_metadata(track_isrc)
    print(metadata)