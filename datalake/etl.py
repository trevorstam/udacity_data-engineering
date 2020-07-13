import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    
    """
    This function extracts song data from S3 bucket,
    creates songs and artist tables and
    writes them to S3 bucket as parquet files
    """
    # get filepath to song data file
    song_data = f"{input_data}song_data/*/*/*/*.json"
    
    # read song data file
    df = spark.read.json(song_data)
    df.printSchema()
    
    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id', 'year', 'duration').dropDuplicates(['song_id'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_data + 'songs/', mode = 'overwrite', partitionBy = ['year', 'artist_id'])

    # extract columns to create artists table
    artists_table = df.select("artist_id","artist_name","artist_location","artist_latitude","artist_longitude").drop_duplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists/', mode = 'overwrite')


def process_log_data(spark, input_data, output_data):
    
    """
    This function extracts log data, filters for song plays,
    creates user and time tables
    and writes these to S3 buckets as parquet files
    """
    # get filepath to log data file
    log_data = os.path.join(input_data, "log-data/")

    # read log data file
    df = spark.read.json(log_data, mode = 'PERMISSIVE').drop_duplicates()
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select("userId","firstName","lastName","gender","level").drop_duplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users/'),  mode = 'overwrite')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x : datetime.utcfromtimestamp(int(x)/1000), TimestampType())
    df = df.withColumn("start_time", get_timestamp("ts"))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x / 1000.0).strftime('%Y-%m-%d %H:%M:%S'))
    df = df.withColumn("start_time", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.selectExpr("start_time as start_time", \
                               "hour(start_time) as hour", \
                               "dayofmonth(start_time) as day", \
                               "weekofyear(start_time) as week", \
                               "month(start_time) as month", \
                               "year(start_time) as year", \
                               "dayofweek(start_time) as weekday").drop_duplicates()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(os.path.join(output_data, "time_table/"), mode='overwrite', partitionBy=["year","month"])

    # read in song data to use for songplays table
    song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
    df_song = spark.read.json(song_data).drop_duplicates() 

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = df.join(df_song, [df.artist == df_song.artist_name, df.song == df_song.title], 'left') \
                .select(df.start_time, df.userId, df.level, df_song.song_id, df_song.artist_id, df.sessionId, df.location, df.userAgent) \
                .drop_duplicates()


    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(os.path.join(output_data, "songplays/"), mode="overwrite", partitionBy=["year","month"])


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = config['AWS']['AWS_S3']
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
