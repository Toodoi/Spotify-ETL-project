import sqlite3
import sqlalchemy
import pandas as pd
import auth

engine = sqlalchemy.create_engine(auth.DATABASE_LOCATION, echo=True)
connection = engine.connect()

# I made some modifications in jupyter and saved the df back to CSV
# Now I load the data into sqlite DB for storage
df = pd.read_csv('spotify_df_mod')
df.to_sql('spotify_tracks', connection, if_exists='append')

connection.close()
