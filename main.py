import SpotifyAPI
import pandas as pd

# Call the functions in SpotifyAPI script to download playlist and recent tracks
recent_tracks = SpotifyAPI.pull_recent_tracks()
playlist_tracks = SpotifyAPI.pull_playlist_tracks()

# Merge the dictionaries returned from the function calls and create a pandas df
merged_dict = {key: recent_tracks[key] + playlist_tracks[key] for key in recent_tracks}
df = pd.DataFrame(merged_dict)

# Spotify only allows you to pull audio features for 100 tracks at a time
# The loops below check the length of df and create batches of track IDs to send to the Spotify API within its limit
id_batches = []
for start_idx in range(0, len(df), 100):
    id_lst = []
    end_idx = start_idx + 99 if start_idx + 99 < len(df) else len(df)
    id_series = df.loc[start_idx:end_idx, 'ids']

    for id in id_series:
        id_lst.append(id)
    batch = ','.join(id_series)
    id_batches.append(batch)

features = SpotifyAPI.pull_track_features(id_batches) # Send API request for features using batches

# Save audio features in separate columns and create a vector of audio features in final column
# I use the vectors to determine how similar tracks are to each other using cosine similarity in jupyter notebook
feature_types = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

for index, type in enumerate(feature_types):
    df[type] = df['ids'].map(lambda x: features.get(x)[index] if features.get(x) != None else None)
df['feature_vector'] = df['ids'].map(features)

# Save the df to a csv for some quick clean-up and visualisation in jupyter notebook
df.to_csv('spotify_df', index=False)



