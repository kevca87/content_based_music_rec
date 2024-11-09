import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_token():
    url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(
        str(CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii")
    )
    headers = {"Authorization": f"Basic {auth_header.decode('ascii')}"}
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)

    return response.json()['access_token']

def get_track_isrc(uri: str) -> str:
    token = get_token()
    uri = uri.replace('spotify:track:', '')
    url = f'https://api.spotify.com/v1/audio-analysis/{uri}'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    print(response.headers)
    print(response.headers['access-control-allow-headers'])
    print(response.headers['retry-after'])
    return response.json()['external_ids']['isrc']

#Example
uri = 'spotify:track:6rqhFgbbKwnb9MLmUQDhG6'
print(get_track_isrc(uri))

