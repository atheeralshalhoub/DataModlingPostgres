import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):

    # open song file
    # Read the song file and view the data
    df = pd.read_json(filepath, lines=True)
    
    # Select columns for song ID, title, artist ID, year, and duration
    song_data = df[['song_id','title','artist_id','year','duration']]
    
   # Index to select the first (only) record in the dataframe
   # Convert the array to a list and set it to `song_data`
    song_data = song_data.values[0].tolist()
    
    # insert song record
    cur.execute(song_table_insert, song_data)
    
    # Select columns for artist ID, name, location, latitude, and longitude
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    
    # Index to select the first (only) record in the dataframe
    # Convert the array to a list and set it to artist_data
    artist_data = artist_data.values[0].tolist()
    # insert artist record
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    # Read the log file and view the data
    df = pd.read_json(filepath, lines=True)

    # Filter records by `NextSong` action
    # Extract the timestamp, hour, day, week of year, month, year, and weekday from the `ts` column and set df_time data into its labels. 
    
    # Convert the `ts` timestamp column to datetime
    df_time = pd.to_datetime(df.ts,unit='ms').to_frame()
    # Extract year from the `ts` column into Year lable 
    df_time['Year'] = df_time.ts.dt.year
    # Extract month from the `ts` column into Month lable 
    df_time['Month'] = df_time.ts.dt.month
    # Extract day from the `ts` column into Day lable 
    df_time['Day'] = df_time.ts.dt.day
    # Extract hour from the `ts` column into Hour lable 
    df_time['Hour'] = df_time.ts.dt.hour
    # Extract weekday from the `ts` column into WeekDay lable 
    df_time['WeekDay'] = df_time.ts.dt.weekday
    # Extract weekofyear from the `ts` column into WeekOfYear lable 
    df_time['WeekOfYear'] = df_time.ts.dt.weekofyear
    
     # insert time records
    for i, row in df_time.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    # Select columns for user ID, first name, last name, gender and level and set to `user_df`
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        # Select the timestamp, user ID, level, song ID, artist ID, session ID, location, and user agent and set to `songplay_data`
            
        cur.execute(song_select, (row.song, row.artist, str(row.length)))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

'''
    Get songid and artistid from song and artist tables

            SELECT statment:
                    songid (int): From songs table .
                    artistid (int): From artists table .

            Based on :
                    based on the title, artist name, and duration of a song.
'''

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()