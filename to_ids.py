import json
from tqdm import tqdm
import argparse
import os

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def save_txt_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item[0]} {item[1]}\n")

def get_tracks(file_path):
    data = read_json_file(file_path)
    return data['uniqueTracks']

def process_mpd(path, playlist_to_process):
    global playlists_processed
    playlists = set()
    filenames = os.listdir(path)
    sequences = []
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            for playlist in mpd_slice["playlists"]:
                if playlists_processed == playlist_to_process:
                    return sequences
                playlists.add(playlist['pid']+1)
                interaction_sequence = process_playlist(playlist)
                sequences.extend(interaction_sequence)
                playlists_processed += 1
    return sequences

def process_playlist(playlist):
    global uri2idx, idx2uri, idx2name
    playlist_sequence = []
    playlist_id = playlist['pid']
    for track in playlist["tracks"]:
        track_uri = track["track_uri"]
        track_id = uri2idx[track_uri]
        idx2name[track_id] = track['track_name']
        playlist_sequence.append((playlist_id, track_id))
    return playlist_sequence

def get_playlists(file_path):
    data = read_json_file(file_path)
    return data['playlists']

if __name__ == '__main__':
    default_unique_tracks_file = './data/unique_tracks_1000p.json'
    default_output_dir = './data_ignored/tracks_dataset'
    default_playlists_to_process = 1000
    playlists_processed = 0

    parser = argparse.ArgumentParser(description='Scrap the dataset from Spotify and Musixmatch')
    parser.add_argument('-t', '--unique_tracks_file', default=default_unique_tracks_file, type=str, help='The path to the unique tracks file')
    parser.add_argument('-o', '--output', default=default_output_dir, type=str, help='The path to the output file')
    parser.add_argument("-p", "--playlists", type=int, default=default_playlists_to_process, help="Number of playlists to process")
    args = parser.parse_args()

    playlist_to_process = args.playlists

    track_uris = get_tracks(args.unique_tracks_file)
    uri2idx = {uri: idx+1 for idx, uri in enumerate(track_uris)}
    idx2uri = {idx+1: uri for idx, uri in enumerate(track_uris)}
    idx2name = {idx+1: '' for idx, uri in enumerate(track_uris)}

    save_json_file(f'{args.output}/uri2idx.json', uri2idx)
    save_json_file(f'{args.output}/idx2uri.json', idx2uri)

    sequences = process_mpd('./data/sample/', playlist_to_process)
    save_json_file(f'{args.output}/idx2name.json', idx2name)
    output_file = f'{args.output}/playlistid_itemid_{playlists_processed}p.txt'
    save_txt_file(output_file, sequences)
    print(f'Processed {playlists_processed} playlists and saved the sequences to {output_file}')