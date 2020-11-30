# DataModlingPostgres

# Song Play Project .. 

##### sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
##### The analytics team is particularly interested in understanding what songs users are listening to. 

### Firstly : recognize the dataset ..
##### - The first dataset is a subset of real data from the Million Song Dataset.
##### - The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above.

#### both of them wrriten as JSON format ..

### Secondly : Schema for Song Play Analysis ..
#### - **Fact Table** :
**songplays** - records in log data associated with song plays i.e. records with page NextSong.
* songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
#### - **Dimension Tables** : 
**users** - users in the app .
* user_id, first_name, last_name, gender, level
**songs** - songs in music database .
* song_id, title, artist_id, year, duration
**artists** - artists in music database .
* artist_id, name, location, latitude, longitude
**time** - timestamps of records in songplays broken down into specific units .
* start_time, hour, day, week, month, year, weekday


### Thirdly : Project Steps ..
#### Open sql_queries.py 
* Write CREATE statements to create each table.
* Check Every datatype in our dataset that suitable.
* Write DROP statements to drop each table if it exists.
* Write INSERT statements to insert values directly by calling query.
* Change create_table_queries and drop_table_queries lists order by adding songplay_table_create and songplay_table_drop in the last of list to avoid errors in SongPlay Fact Table using REFERENCES for each foreign key. *(faced issue and fixed)*

#### Open Terminal ..
* Run create_tables.py to create your database and tables.

#### open Test Note Book ..
* connect with sql and postgresql://student:student@127.0.0.1/sparkifydb to access to Our sparkifydb DataBase.
* Run SELECT statements to be sure if all our tables have created successfully with the correct columns.

#### Open etl Note Book ..
* imports all files needed (pandas as pd , sql_queries).
* Connect with Database " sparkifydb ".
* Getfiles method needed to get all files have dataset.

##### Process `song_data` ..
on the first dataset, `song_data`, to create the `songs` and `artists` dimensional tables.
- Use the `get_files` function provided above to get a list of all song JSON files in `data/song_data`
  song_files = get_files('data/song_data/')
- Select the first song in this list
  filepath = song_files[0]
- Read the song file and view the data
  df = pd.read_json(filepath, lines=True)
  df.head()
<img src="images/output1.png" width="750" height="750">

##### songs Table ..
- Select columns for song ID, title, artist ID, year, and duration
  song_data = df[['song_id','title','artist_id','year','duration']]
- Use `df.values` to select just the values from the dataframe
  song_data = **song_data.values**[0].tolist()
- Index to select the first (only) record in the dataframe
  song_data = song_data.**values[0]**.tolist()
- Convert the array to a list and set it to `song_data`
  song_data = song_data.values[0].**tolist()**
<img src="images/output2.png" width="750" height="750">

###### Insert Record into Song Table
Implement the `song_table_insert` query in `sql_queries.py`..
* cur.execute(song_table_insert, song_data)
* conn.commit()

#### open Test Note Book ..
* connect with sql and postgresql://student:student@127.0.0.1/sparkifydb to access to Our sparkifydb DataBase.
* Run SELECT statement SELECT * FROM songs LIMIT 5; to confirm insertion successfully with the correct columns.

##### artists Table ..
- Select columns for artist ID, name, location, latitude, and longitude
  artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
- Use df.values to select just the values from the dataframe
  artist_data = **artist_data.values**[0].tolist()
- Index to select the first (only) record in the dataframe
  artist_data = artist_data.**values[0]**.tolist()
- Convert the array to a list and set it to artist_data
  artist_data = artist_data.values[0]**.tolist()**

###### Insert Record into Artist Table
Implement the `artist_table_insert` query in `sql_queries.py`..
* cur.execute(artist_table_insert, artist_data)
  conn.commit()

#### open Test Note Book ..
* connect with sql and postgresql://student:student@127.0.0.1/sparkifydb to access to Our sparkifydb DataBase.
* Run SELECT statement SELECT * FROM artists LIMIT 5; to confirm insertion successfully with the correct columns.


##### Process `log_data` ..
on the second dataset, `log_data`, to create the `time` and `users` dimensional tables, as well as the `songplays` fact table.
- Use the `get_files` function provided above to get a list of all log JSON files in `data/log_data`
  log_files = get_files('data/log_data/')
- Select the first log file in this list
  filepath = log_files[0]
- Read the log file and view the data
  df = pd.read_json(filepath, lines=True)
  df.head()


##### time Table ..
- Filter records by `NextSong` action
- Convert the `ts` timestamp column to datetime
* df_time = pd.**to_datetime(df.ts,unit='ms')**.to_frame()
- Extract the timestamp, hour, day, week of year, month, year, and weekday from the `ts` column and set df_time data into its labels. 
* df_time['year'] = df_time.ts.dt.year
  df_time['month'] = df_time.ts.dt.month
  df_time['hour'] = df_time.ts.dt.hour
  df_time['day'] = df_time.ts.dt.day
  df_time['WeekDay'] = df_time.ts.dt.weekday
  df_time['WeekYear'] = df_time.ts.dt.weekofyear
  df_time.head()


###### Insert Records into Time Table
Implement the `time_table_insert` query in `sql_queries.py` ..
- df_time is a list that means insertion using for loop to insert each row.
* for i, row in df_time.iterrows():
    cur.execute(time_table_insert, list(row))
    conn.commit()

#### open Test Note Book ..
* connect with sql and postgresql://student:student@127.0.0.1/sparkifydb to access to Our sparkifydb DataBase.
* Run SELECT statement SELECT * FROM time LIMIT 5; to confirm insertion successfully with the correct columns.

##### users Table ..
- Select columns for user ID, first name, last name, gender and level and set to `user_df`
* user_df = df[['userId','firstName','lastName','gender','level']]

###### Insert Records into Users Table
Implement the `user_table_insert` query in `sql_queries.py`
- user_df is a list that means insertion using for loop to insert each row.
* for i, row in user_df.iterrows():
   cur.execute(user_table_insert, row)
   conn.commit()


##### songplays Table ..
This Table is a fact that contain information from the songs table, artists table, and original log filefor the `songplays` table. 
- Implement the `song_select` query in `sql_queries.py` to find the song ID and artist ID based on the title, artist name, and duration of a song.

* SELECT songs.song_id, artists.artist_id FROM songs JOIN artists ON 
  songs.artist_id=artists.artist_id WHERE 
  songs.title=%s AND artists.name=%s AND songs.duration=%s;

- Select the timestamp, user ID, level, song ID, artist ID, session ID, location, and user agent and set to `songplay_data`

#### Open sql_queries.py 
* Write SELECT statement to get song ID and artist ID using JOIN between songs and artists tables.

#### Open etl Note Book ..
* for index, row in df.iterrows():
  cur.execute(song_select, (row.song, row.artist, str(row.length)))
    results = cur.fetchone()
    
    if results:
        songid, artistid = results
    else:
        songid, artistid = None, None



###### Insert Records into Songplays Table
Implement the `songplay_table_insert` query  in `sql_queries.py`
* songplay_data = (pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
    cur.execute(songplay_table_insert, songplay_data)
    conn.commit()
    
- converting start time to DateTime 
  pd.to_datetime(row.ts,unit='ms')
  


#### Open etl.py 
- write all changes in etl note book 

**In Process_song_file def**

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']]
    song_data = song_data.values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    artist_data = artist_data.values[0].tolist()
    cur.execute(artist_table_insert, artist_data)
    
**In Process_log_file def**
    # open log file
    df = pd.read_json(filepath, lines=True)

   
    # hour, day, week of year, month, year, and weekday 
    df_time = pd.to_datetime(df.ts,unit='ms').to_frame()
    df_time['Year'] = df_time.ts.dt.year
    df_time['Month'] = df_time.ts.dt.month
    df_time['Day'] = df_time.ts.dt.day
    df_time['Hour'] = df_time.ts.dt.hour
    df_time['WeekDay'] = df_time.ts.dt.weekday
    df_time['WeekOfYear'] = df_time.ts.dt.weekofyear
    
    for i, row in df_time.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, str(row.length)))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


#### Lastly : Open Terminal ..
- Final output for Song_Data

- Final output for Log_Data

#### open Test Note Book ..
* connect with sql and postgresql://student:student@127.0.0.1/sparkifydb to access to Our sparkifydb DataBase.
* Run SELECT statements to confirm output for each table.
##### songplays Table Final output ..
##### users Table Final output ..
##### songs Table Final output ..
##### artists Table Final output ..
##### time Table Final output ..
