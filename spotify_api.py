# Code to mine the metadata from spotify API

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_isrc(uri: str) -> str:
    try:
        track = sp.track(uri)
        return track['external_ids']['isrc']
    except spotipy.client.SpotifyException as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

def get_track_audio_analysis(uri: str) -> dict:
    try:
        audio_analysis = sp.audio_analysis(uri)
        return audio_analysis
    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return 404
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

def get_track_metadata(isrc: str) -> dict:
    try:
        metadata = sp.track(isrc)
        return metadata
    except spotipy.client.SpotifyException as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None