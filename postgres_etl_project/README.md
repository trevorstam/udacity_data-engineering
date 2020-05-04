### Business Case
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. 

### Objectives
- Model data with PostgreSQL
- Build the ETL pipelines with Python
- Build schemas using star schema with fact and dimension tables
- Implement full CRUD functionality

### Datasets
**Songs Dataset**: is a subset of the Million Song dataset

**Log Dataset**: log data created by Event Simulator

### Schema Design
#### Fact Table
**songplays**: created the fact table song plays.** These are records in the log data associated with songplays.
```
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
```

#### Dimension tables
**users**: user data of the Sparkify users
```
user_id, first_name, last_name, gender, level
```
**songs**: songs, titles, year, duration, and id's
```
song_id, title, artist_id, year, duration
```
**artists**: name and location of artists
```
artist_id, name, location, latitude, longitude
```
**time**: timestamp of records in songplays broken down in various time units
```
start_time, hour, day, week, month, year, weekday
```

### Database and Pipeline Design
The schema design following the star schema is very well suited for the data necessary for this project.
The number of tables is fairly limited and this makes for easy querying and occasional joins of denormalized tables.
The joins are never very complicated and therefore performant.

The pipeline design is pretty straight forward as song and log JSON data is read into Pandas, transformed where necessary and stored in PostgreSQL.

### Project Files
**sql_queries.py**: file that contains SQL queries to create and drop tables. Also has queries to insert records into tables

**create_tables.py**: file that contains code that creates the sparkify database and creates all tables mentioned in schema design

**etl.py**: file that processes the log and song data

**etl.ipynb**: Jupyter notebook in which log and song data is analyzed

**test.ipynb**: Jupyter notebook in which connection to postgres database is made and loaded data is validated and tested

### Project Environment
Python 3.7 and above
PostgreSQL 9.5 and above
psycopg2: PostgreSQL database adapter for Python

### Getting Started with this project
1. Make sure Python, PostgreSQL and psycopg2 are properly installed on your computer
2. Open terminal of choice and run `python create_tables.py` to create tables
3. Run the cells in etl.ipynb
4. Run `python etl.py`
5. Run test.ipynb to verify the database is up to date and loaded proper data


