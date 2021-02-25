# If required to delete the DB
import sqlite3

connection = sqlite3.connect('spotify.db')

cursor = connection.cursor()

cursor.execute('DROP TABLE spotify_tracks')


connection.commit()