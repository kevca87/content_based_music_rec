from spotify_api import get_track_isrc
from musixmatch_api import get_lyrics, get_track_metadata
import json
from tqdm import tqdm
from time import sleep
from exceptions import RequestLimitException
import argparse
import os

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File not found: {file_path}")

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# def get_playlists(file_path):
#     data = read_json_file(file_path)
#     return data['playlists']

def get_tracks(file_path):
    data = read_json_file(file_path)
    return data['uniqueTracks']

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)
    
def get_tracks_data(uris):
    global last_index_scraped
    first_index_scraped = last_index_scraped
    tracks_dataset = {}
    unable_to_get_isrc = []
    unable_to_get_lyric = []
    tracks_metadata = []
    tracks_lyrics = []
    for uri in tqdm(uris):    
        isrc = get_track_isrc(uri)
        try:
            if isrc != None:
                tracks_dataset[uri] = { 'unique_tracks_idx': last_index_scraped }
                track_metadata = get_track_metadata(isrc)
                if track_metadata != None and track_metadata['has_lyrics'] == 1:
                    tracks_dataset[uri]['metadata'] = track_metadata
                    tracks_metadata.append(track_metadata)
                    lyrics = get_lyrics(isrc)
                    if lyrics != None:
                        tracks_lyrics.append(lyrics)
                        tracks_dataset[uri]['lyrics'] = lyrics
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
            print(f'\n{e}')
        save_json_file(f'{default_output_dir}/tracks_dataset_{first_index_scraped}_{last_index_scraped}.json', tracks_dataset)
        if first_index_scraped < last_index_scraped:
            remove_file(f'{default_output_dir}/tracks_dataset_{first_index_scraped}_{last_index_scraped-1}.json')
        last_index_scraped += 1
        save_json_file(f'{default_output_dir}/unable_to_get_isrc.json', unable_to_get_isrc)
        save_json_file(f'{default_output_dir}/unable_to_get_lyric.json', unable_to_get_lyric)
        save_json_file(f'{default_output_dir}/tracks_metadata.json', tracks_metadata)
        save_json_file(f'{default_output_dir}/tracks_lyrics.json', tracks_lyrics)
    return tracks_dataset

# def get_lyrics_for_tracks(tracks):
#     lyrics = []
#     for track in tracks:
#         isrc = track['isrc']
#         lyrics.append(get_lyrics(isrc))
#     return lyrics

if __name__ == '__main__':
    default_unique_tracks_file = './data/unique_tracks_1000p.json'
    default_output_dir = './data_ignored/tracks_dataset'
    parser = argparse.ArgumentParser(description='Scrap the dataset from Spotify and Musixmatch')
    parser.add_argument('-t', '--unique_tracks_file', default=default_unique_tracks_file, type=str, help='The path to the unique tracks file')
    parser.add_argument('-o', '--output', default=default_output_dir, type=str, help='The path to the output file')
    parser.add_argument('-s', '--start', type=int, help='The start index of the tracks')
    parser.add_argument('-e', '--end', type=int, help='The end index of the tracks')
    args = parser.parse_args()

    track_uris = get_tracks(args.unique_tracks_file)

    print(f'Start [{args.start}]: {track_uris[args.start]}')
    print(f'End [{args.end}]: {track_uris[args.end]}')
    assert args.start < len(track_uris) and args.end < len(track_uris)
    assert args.start < args.end

    track_uris_to_scrap = track_uris[args.start:args.end+1]

    print(f'Tracks to scrap: {len(track_uris_to_scrap)}')
    
    last_index_scraped = args.start
    get_tracks_data(track_uris_to_scrap)
    print(f'Next to scrap [{last_index_scraped}]:', track_uris[last_index_scraped])
    if last_index_scraped > args.end:
        print('Completed successfully!')


# 100 playlist --> 5178 tracks
# 1000 playlist --> 34443 tracks
