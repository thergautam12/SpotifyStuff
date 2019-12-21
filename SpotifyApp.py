import os
import sys

import spotipy
import spotipy.util as util
import json

import pandas as pd
import numpy as np

# User ID: 1283831837
# Owen ID: 121413914
# username = sys.argv[1]

# user_info = json.dumps(spotify.me(), sort_keys=True, indent=4)
# devices = json.dumps(spotify.devices(), sort_keys=True, indent=4)

# user_info = spotify.me()
# devices = spotify.devices()

def common_entries(*dicts):
    for i in set(dicts[0]).intersection(*dicts[1:]):
        yield (i,) + tuple(d[i] for d in dicts)

def createSpotifyObject(username):
    scope = 'user-read-private user-read-email user-read-playback-state user-modify-playback-state user-top-read'
    scope += ' playlist-read-private playlist-read-collaborative'

    try:
        token = util.prompt_for_user_token(username, scope)
    except:
        os.remove(f'.cache-{username}')
        token = util.prompt_for_user_token(username, scope)

    return spotipy.Spotify(auth=token)

def getTopTracksInfo(spotify, time_range='long_term', limit=50):
    top_tracks = spotify.current_user_top_tracks(limit=limit, time_range=time_range)['items']

    track_names = []
    ids = []
    popularity = []

    for track in top_tracks:
        track_names += [track['name']]
        ids += [track['id']]
        popularity += [track['popularity']]

    return pd.DataFrame({'track': track_names, 'id': ids, 'popularity': popularity})

def featuresDF(features):
    features = list(common_entries(*features))
    return pd.DataFrame({name: data for name, *data in features})

def main():
    spotify = createSpotifyObject(sys.argv[1])
    # devices = spotify.devices()['devices']
    # device_id = devices[0]['id']
    # spotify.start_playback(device_id=device_id)
    top_tracks = getTopTracksInfo(spotify)

    features = spotify.audio_features(list(top_tracks['id']))

    features = featuresDF(features)
    user_info = json.dumps(spotify.me(), sort_keys=True, indent=4)
    print(features.head())
    print(user_info)


if __name__ == '__main__':
    main()





