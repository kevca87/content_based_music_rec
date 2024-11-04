from spotify_api import get_track_isrc
from musixmatch_api import get_lyrics, get_track_metadata
import json
from tqdm import tqdm
from time import sleep
from exceptions import RequestLimitException

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# def get_playlists(file_path):
#     data = read_json_file(file_path)
#     return data['playlists']

def get_tracks(file_path):
    data = read_json_file(file_path)
    return data

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)
    
def get_tracks_data(uris):
    isrcs = {}
    unable_to_get_isrc = []
    unable_to_get_lyric = []
    tracks_metadata = []
    tracks_lyrics = []
    for uri in tqdm(uris):
        isrc = get_track_isrc(uri)
        try:
            if isrc != None:
                isrcs[uri] = isrc
                track_metadata = get_track_metadata(isrc)
                if track_metadata != None and track_metadata['has_lyrics'] == 1:
                    tracks_metadata.append(track_metadata)
                    lyrics = get_lyrics(isrc)
                    if lyrics != None:
                        tracks_lyrics.append(lyrics)
                    else:
                        unable_to_get_lyric.append(uri)
            else:
                unable_to_get_isrc.append(uri)
            sleep(0.5)
        except RequestLimitException as e:
            unable_to_get_lyric.append(uri)
            print(e)
            break
        except Exception as e:
            print(e)
        save_json_file('isrcs.json', isrcs)
        save_json_file('unable_to_get_isrc.json', unable_to_get_isrc)
        save_json_file('unable_to_get_lyric.json', unable_to_get_lyric)
        save_json_file('tracks_metadata.json', tracks_metadata)
        save_json_file('tracks_lyrics.json', tracks_lyrics)
    return isrcs

# def get_lyrics_for_tracks(tracks):
#     lyrics = []
#     for track in tracks:
#         isrc = track['isrc']
#         lyrics.append(get_lyrics(isrc))
#     return lyrics

if __name__ == '__main__':
    part = 1
    musixmatch_api_limit = 100
    range_start = (part - 1) * musixmatch_api_limit
    range_end = part * musixmatch_api_limit
    uris = get_tracks('tracks.json')
    print('Total tracks:', len(uris))
    get_tracks_data(uris[range_start:range_end])


# 100 playlist --> 5178 tracks
# 1000 playlist --> 34443 tracks
