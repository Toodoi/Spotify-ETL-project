# Spotify-ETL-project
An extract, transform, load (ETL) data project to download data from the Spotify API, modify it a bit and then save it in a database.

This was a fun project I did to play around with the SpotifyAPI and see how well cosine similarity would work using audio track features that Spotify provides to determine how similar tracks are to each other.

I created three functions to collect data from the Spotify API. Two functions pull a bunch of my recently played tracks and tracks I have in various playlists. The third function uses the track IDs of all the tracks I've downloaded to send a further request for audio features on the tracks. These features are metrics to describe the tracks and include things like: energy, danceability and tempo.

I saved all the data in CSV format using pandas and opened it in Jupyter to do some quick clean-up. I removed duplicate tracks and some audio features that did not seem very interesting based on their distributions. I also dropped some tracks where I was not receiving audio features from the API. I also took this opportunity to compare the similarity of tracks using their feature vectors and cosine similarity.

After this I saved the data in a sqlite3 database for storage.
