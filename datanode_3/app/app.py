from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf
import time
import logging
import psutil
import os

log_path = "/tmp/spark_app.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)

def log_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    logging.info(f"Current memory usage: {mem:.2f} MB")

def main():
    log4j_path = "/home/jovyan/app/log4j.properties"
    os.environ["SPARK_SUBMIT_OPTS"] = f"-Dlog4j.configuration=file:{log4j_path}"
    logging.info("Starting Spark session")

    spark = SparkSession.builder \
        .appName("SpotifyApp") \
        .getOrCreate() \
    
    spark.sparkContext.setLogLevel("ERROR")

    log_memory_usage()
    logging.info("Reading data from HDFS")

    df = spark.read.option("header", True).parquet("hdfs://namenode:9000/data.parquet")
    df = df.repartition(8)
    start_time = time.time()


    log_memory_usage()
    logging.info("Performing transformations")
    df_explicit = df.filter(F.col("Explicit") == "Yes")
    df_non_explicit = df.filter(F.col("Explicit") == "No")

    logging.info("Top most haved songs artist with explicit")
    df_explicit.groupBy("artist").count().orderBy("count", ascending=False).show(10)
    logging.info("Top most haved songs artist without explicit")
    df_non_explicit.groupBy("artist").count().orderBy("count", ascending=False).show(10)

    df.count()
    df_explicit.count()
    df_non_explicit.count()
    logging.info("Average Popularity for explicit songs")
    df_explicit.groupBy("artist") \
        .agg(F.avg("Popularity").alias("avg_popularity")) \
        .orderBy("avg_popularity", ascending=False) \
        .show(10)

    logging.info("Average Popularity for non-explicit songs")
    df_non_explicit.groupBy("artist") \
        .agg(F.avg("Popularity").alias("avg_popularity")) \
        .orderBy("avg_popularity", ascending=False) \
        .show(10)

    logging.info("Most popular explicit songs")
    df_explicit.select("song", "artist", "Popularity") \
        .orderBy(F.col("Popularity").desc()) \
        .show(10)

    logging.info("Least popular non-explicit songs")
    df_non_explicit.select("song", "artist", "Popularity") \
        .orderBy(F.col("Popularity").asc()) \
        .show(10)
    top_artists = df.groupBy("artist").count().orderBy("count", ascending=False).limit(10)

    logging.info("Show top artists:")
    top_artists.show()

    log_memory_usage()
    logging.info("Job completed")

    elapsed = time.time() - start_time
    logging.info(f"Execution time: {elapsed:.2f} seconds")
    with open("/logs/time.txt", "w+") as f:
        print(elapsed, file=f)
    spark.stop()

if __name__ == "__main__":
    main()
