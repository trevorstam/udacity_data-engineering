import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
        staging_event_id  int IDENTITY(0,1) NOT NULL,
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender VARCHAR,
        itemInSession int,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration FLOAT,
        sessionId int NOT NULL,
        song VARCHAR,
        status int,
        ts BIGINT,
        userAgent VARCHAR,
        userId int      
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
        num_songs int,
        artist_id VARCHAR NOT NULL,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR NOT NULL,
        title VARCHAR,
        duration FLOAT,
        year int
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id int IDENTITY(0, 1) PRIMARY KEY, 
        start_time date NOT NULL, 
        user_id int NOT NULL, 
        level VARCHAR, 
        song_id varchar, 
        artist_id varchar, 
        session_id int, 
        location varchar, 
        user_agent varchar
    )   DISTSTYLE KEY
        DISTKEY ( start_time )
        SORTKEY ( start_time );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
        user_id int PRIMARY KEY, 
        first_name varchar, 
        last_name varchar, 
        gender varchar, 
        level varchar NOT NULL
    ) SORTKEY(user_id);
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
        song_id varchar PRIMARY KEY, 
        title varchar, 
        artist_id varchar, 
        year int, 
        duration float
    ) SORTKEY(song_id);
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
        artist_id varchar, 
        name varchar, 
        location varchar, 
        latitude numeric, 
        longitude numeric
    ) SORTKEY(artist_id);
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time(
        start_time date PRIMARY KEY, 
        hour int, 
        day int, 
        week int, 
        month int, 
        year int, 
        weekday int
    ) diststyle all;
""")

# STAGING TABLES

# variables for staging tables .format
log_data = config.get('S3', 'LOG_DATA')
song_data = config.get('S3', 'SONG_DATA')
iam_role_credentials = config.get('CLUSTER', 'DWH_IAM_ARN')
json_logs = config.get('S3', 'LOG_JSONPATH')

staging_events_copy = ("""
    COPY staging_events
    FROM {}
    credentials 'aws_iam_role={}'
    FORMAT as json {}
""").format(log_data, iam_role_credentials, json_logs)

staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    credentials 'aws_iam_role={}'
    FORMAT as json 'auto'
""").format(song_data, iam_role_credentials)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' as start_time,
                    se.userId as user_id,
                    se.level as level,
                    ss.song_id as song_id,
                    ss.artist_id as artist_id,
                    se.sessionId as session_id,
                    se.location as location,
                    se.userAgent as user_agent
    FROM staging_events as se
    JOIN staging_songs as ss
    ON (se.artist = ss.artist_name)
    WHERE se.page = 'NextSong'
""")


user_table_insert = ("""
    INSERT INTO users(user_id, first_name, last_name, gender, level)
    SELECT DISTINCT se.userId as user_id,
                    se.firstName as first_name,
                    se.lastName as last_name,
                    se.gender as gender,
                    se.level as level
    FROM staging_events as se
    WHERE se.page = 'NextSong'
""")

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration)
    SELECT DISTINCT ss.song_id as song_id,
                    ss.title as title,
                    ss.artist_id as artist_id,
                    ss.year as year,
                    ss.duration as duration
    FROM staging_songs as ss
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT ss.artist_id as artist_id,
                    ss.artist_name as name,
                    ss.artist_location as location,
                    ss.artist_latitude as latitude,
                    ss.artist_longitude as longitude
    FROM staging_songs as ss;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' as start_time,
                    EXTRACT(hour FROM start_time) as hour,
                    EXTRACT(day FROM start_time) as day,
                    EXTRACT(week FROM start_time) as week,
                    EXTRACT(month FROM start_time) as month,
                    EXTRACT(year FROM start_time) as year,
                    EXTRACT(week FROM start_time) as weekday
    FROM staging_events as se
    WHERE se.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
