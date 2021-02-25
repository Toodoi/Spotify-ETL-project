import spotipy.util as util
import requests
import auth
import datetime

def get_headers(token):
    # Generate headers for API request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=token)
    }
    return headers

def get_token(scope):
    # Generate token for API request (scope changes for different requests)
    token = util.prompt_for_user_token(username=auth.USER_ID,
                                       scope=scope,
                                       client_id=auth.CLIENT_ID,
                                       client_secret=auth.CLIENT_SECRET,
                                       redirect_uri='http://localhost:7777/callback')
    return token

def pull_recent_tracks():
    store_data = []
    token = get_token('user-read-recently-played')
    headers = get_headers(token)
    today = datetime.datetime.now()

    for day in range(1):
        before_time = today - datetime.timedelta(days=day)
        before_unix = int(before_time.timestamp()) * 1000

        response = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=49&before={before}".format(before=before_unix), headers=headers)
        data = response.json()
        store_data.append(data)

    tracks = []
    artists = []
    ids = []

    for batch in store_data:
        for key in batch['items']:
            tracks.append(key['track']['name'])
            artists.append(key['track']['album']['artists'][0]['name'])
            ids.append(key['track']['id'])

    recent_tracks_dict = {
        'tracks' : tracks,
        'artists' : artists,
        'ids' : ids
    }

    return recent_tracks_dict

def pull_playlist_tracks(limit=12):
    # Pulls all tracks from a defined amount of user playlists (default 5). Returns a dict of track & artist names
    limit = limit
    token = get_token('playlist-read-private')
    headers = get_headers(token)
    response = 	requests.get("https://api.spotify.com/v1/me/playlists?limit={}".format(limit), headers=headers)
    data = response.json() # This response contains playlist data, tracklist IDs must be extracted and a new request is sent to receive them

    tracks = []
    artists = []
    ids = []

    playlist_tracks = [item['tracks']['href'] for item in data['items']]
    for tracklist in playlist_tracks:
        response = requests.get(tracklist, headers=headers)
        tracklist_data = response.json()

        for key in tracklist_data['items']:
            tracks.append(key['track']['name'])
            artists.append(key['track']['album']['artists'][0]['name'])
            ids.append(key['track']['id'])

    playlist_track_dict = {
        'artists' : artists,
        'tracks' : tracks,
        'ids' : ids
    }

    return playlist_track_dict

def pull_track_features(ids_list):
    # Pulls audio features for each track. Maximum is 100 tracks per request, so batches are sent
    token = get_token('user-read-recently-played') # This request can take any scope
    headers = get_headers(token)

    test_dict = {}
    for id_string in ids_list:
        response = requests.get("https://api.spotify.com/v1/audio-features?ids={}".format(id_string), headers=headers)
        data = response.json()

        for track_features in data['audio_features']:
            test_dict[track_features['id']] = [track_features['danceability'], track_features['energy'], track_features['key'], track_features['loudness'],
                                               track_features['mode'], track_features['speechiness'], track_features['acousticness'],
                                               track_features['instrumentalness'], track_features['liveness'], track_features['valence'], track_features['tempo']]

    return test_dict