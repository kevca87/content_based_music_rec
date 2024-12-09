from spotify_api import get_track_features
import json
from tqdm import tqdm
from time import sleep
import os
import argparse

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File not found: {file_path}")

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_tracks(file_path):
    data = read_json_file(file_path)
    return data['uniqueTracks']

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)
    
def get_tracks_data(uris, default_output_dir, section = -1):
    if not os.path.exists(default_output_dir):
        os.makedirs(default_output_dir)

    files = os.listdir(default_output_dir)

    omited = 0
    omited_uris = []

    if section != -1:
        uris = uris[section*5000:(section+1)*5000]
    
    temp_data = []
    limit = 100

    for uri in tqdm(uris):
        name = uri.replace('spotify:track:', '')
        if f'{name}.json' in files:
            continue
        if name in temp_data:
            continue
        
        temp_data.append(name)
        if len(temp_data) == limit:
            while True:
                track_info = get_track_features(temp_data)
                if track_info is not None:
                    break
                sleep(1800)
            sleep(5)

            for info, name in zip(track_info, temp_data):
                file_name = f'{name}.json'
                if info == 404:
                    omited += 1
                    omited_uris.append(uri)
                    if os.path.exists(os.path.join(default_output_dir, file_name)):
                        remove_file(os.path.join(default_output_dir, file_name))
                else:
                    save_json_file(os.path.join(default_output_dir, file_name), info)
                files.append(file_name)
            temp_data = []
    
    if len(temp_data) > 0:
        while True:
            track_info = get_track_features(temp_data)
            if track_info is not None:
                break
            sleep(1800)
        sleep(5)

        for info, name in zip(track_info, temp_data):
            file_name = f'{name}.json'
            if info == 404:
                omited += 1
                omited_uris.append(uri)
                if os.path.exists(os.path.join(default_output_dir, file_name)):
                    remove_file(os.path.join(default_output_dir, file_name))
            else:
                save_json_file(os.path.join(default_output_dir, file_name), info)
            files.append(file_name)
        temp_data = []

if __name__ == '__main__':
    default_unique_tracks_file = './data/unique_tracks_1000p.json'
    default_output_dir = './data_ignored/tracks_dataset_spotify_audio_features'

    parser = argparse.ArgumentParser(description='Scrap the dataset from Spotify API.')
    parser.add_argument('-s', '--section', type=int, default=-1, help='Section of the dataset to scrap.')

    args = parser.parse_args()
    section = args.section
    

    track_uris_to_scrap = get_tracks(default_unique_tracks_file)

    get_tracks_data(track_uris_to_scrap, default_output_dir, section)
    print('Completed successfully!')
