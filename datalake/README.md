## Project: Data Lake

### Introduction
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Build an ETL pipeline that extracts data from S3, process them using Spark, and load the data back into S3 as a set of dimensional tables. 

### Project Description
In this project, you'll apply what you've learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, you will need to load data from S3, process the data into analytics tables using Spark, and load them back into S3. You'll deploy this Spark process on a cluster using AWS.

### ETL Pipeline

#### Reading and loading the datasets
The song and log datasets are located in S3 buckets. You'll need to read them from
- Song data: ```s3://udacity-dend/song_data```
- Log data: ```s3://udacity-dend/log_data```

#### Processing and schema creation
The loaded data is processed using Spark. Once the data is processed and transformed in the appropriate format, the tables for the star schema are created. It consists of 1 fact table and 4 dimension tables. General schema is listed below for each table.

1. Fact table:
- songplays -->
```songplay_id, start_time, user_id, level, song_id, artsit_id, session_id, location, user_agent```

2. Dimension tables:
- users -->
```user_id, first_name, last_name, gender, level```

- songs -->
```song_id, title, artist_id, year, duration```
- artists --> 
```artist_id, name, location, latitude, longitude```
- time -->
```start_time, hour, day, week, month, year, weekday```

#### Write to AWS S3
Once the processing phase has finalized and the tables are created, all the data will be written to a S3 bucket as partitioned parquet files.

### How to run
- Make sure you have signed up for an AWS account and that you have created a proper role in IAM with AmazonS3FullAccess policy attached, in order to have access to S3 buckets.
- Create the file ```dl.cfg``` and enter the following information:
```KEY=YOUR_AWS_ACCESS_KEY```
```SECRET=YOUR_AWS_SECRET_KEY```
```AWS_S3=YOUR_AWS_OUTPUT_BUCKET```
- Execute the python file with the following command: ```python etl.py```



