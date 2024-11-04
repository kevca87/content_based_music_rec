"""
    shows deep stats for the MPD

    usage:

        python deeper_stats.py path-to-mpd-data/
"""
import sys
import json
import re
import collections
import os
import argparse

total_playlists = 0
total_tracks = 0
tracks = set()
artists = set()
albums = set()
titles = set()
ntitles = set()
playlists = set()
full_title_histogram = collections.Counter()
title_histogram = collections.Counter()
artist_histogram = collections.Counter()
track_histogram = collections.Counter()

quick = False
max_files_for_quick_processing = 50


# This function read all the files of a directory and update all the global sets (more important tracks, albums and artists)
def process_mpd(path, playlist_to_process):
    count = 0
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            process_info(mpd_slice["info"])
            for playlist in mpd_slice["playlists"]:
                if total_playlists == playlist_to_process:
                    return
                playlists.add(playlist['pid'])
                process_playlist(playlist)
            count += 1
            if quick and count > max_files_for_quick_processing:
                break


def show_summary():
    print()
    print("number of playlists", total_playlists)
    print("number of tracks", total_tracks)
    print("number of unique tracks", len(tracks))
    print("number of unique albums", len(albums))
    print("number of unique artists", len(artists))
    print("number of unique titles", len(titles))
    print("number of unique normalized titles", len(ntitles))
    print("avg playlist length", float(total_tracks) / total_playlists)
    print()
    print("full playlist titles")
    for title, count in full_title_histogram.most_common():
        print("%7d %s" % (count, title))
    print()

    print("top playlist titles")
    for title, count in title_histogram.most_common():
        print("%7d %s" % (count, title))
    print()

    print("top tracks")
    for track, count in track_histogram.most_common(10000):
        print("%7d %s" % (count, track))

    print()
    print("top artists")
    for artist, count in artist_histogram.most_common(10000):
        print("%7d %s" % (count, artist))


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.,\/#!$%\^\*;:{}=\_`~()@]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def process_playlist(playlist):
    global total_playlists, total_tracks

    total_playlists += 1

    titles.add(playlist["name"])
    nname = normalize_name(playlist["name"])
    ntitles.add(nname)
    title_histogram[nname] += 1
    full_title_histogram[playlist["name"].lower()] += 1

    for track in playlist["tracks"]:
        total_tracks += 1
        albums.add(track["album_uri"])
        tracks.add(track["track_uri"])
        artists.add(track["artist_uri"])

        full_name = track["track_name"] + " by " + track["artist_name"]
        artist_histogram[track["artist_name"]] += 1
        track_histogram[full_name] += 1


def process_info(info):
    for k, v in list(info.items()):
        print("%-20s %s" % (k + ":", v))
    print()

def write_output_file(output_file_path: str, output: dict) -> None:
    with open(output_file_path, 'w') as outfile:
        json.dump(output, outfile)

if __name__ == "__main__":
    default_playlists_to_process = 1000
    default_output_filename = f"./data/unique_tracks_{default_playlists_to_process}p.json"
    default_mpd_path = "./data/sample/"

    parser = argparse.ArgumentParser(description="Shows deep stats for the MPD")
    parser.add_argument("-i", "--input", type=str, default=default_mpd_path, help="Path to the MPD data")
    parser.add_argument("-q", "--quick", action="store_true", help="Enable quick processing mode")
    parser.add_argument("-o", "--output", type=str, default=default_output_filename, help="Output file")
    parser.add_argument("-p", "--playlists", type=int, default=default_playlists_to_process, help="Number of playlists to process")
    args = parser.parse_args()

    quick = args.quick
    path = args.input
    output_file_path = args.output
    playlist_to_process = args.playlists

    process_mpd(path, playlist_to_process)
    tracks_list = list(tracks)
    processed_playlists_pids = list(playlists)
    assert len(playlists) == total_playlists
    output = {
        'numberOfUniqueTracks': len(tracks_list),
        'numberOfProcessedPlaylists': len(playlists),
        'uniqueTracks': tracks_list,
        'processedPlaylists': processed_playlists_pids,
    }
    print('Number of unique tracks:', len(tracks_list))
    print('Number of processed playlists:', len(playlists))
    write_output_file(output_file_path, output)
