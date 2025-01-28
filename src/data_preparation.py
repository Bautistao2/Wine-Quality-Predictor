import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col

# Initialize Spark session
spark = SparkSession.builder.appName("DataPreparation").getOrCreate()

def load_datasets():
    """
    Load red and white wine datasets using PySpark.
    """
    red_wine_path = f"file:///{os.path.abspath('data/winequality-red.csv')}".replace("\\", "/")
    white_wine_path = f"file:///{os.path.abspath('data/winequality-white.csv')}".replace("\\", "/")
    
    red_wine = spark.read.csv(red_wine_path, sep=";", header=True, inferSchema=True)
    white_wine = spark.read.csv(white_wine_path, sep=";", header=True, inferSchema=True)

    return red_wine, white_wine

def merge_and_process_data(red_wine, white_wine):
    """
    Merge red and white wine datasets and preprocess the combined data.
    """
    red_wine = red_wine.withColumn("wine_type", when(col("quality").isNotNull(), "red"))
    white_wine = white_wine.withColumn("wine_type", when(col("quality").isNotNull(), "white"))
    
    combined_data = red_wine.union(white_wine)
    combined_data = combined_data.withColumn("wine_type", when(col("wine_type") == "red", 0).otherwise(1))
    return combined_data

if __name__ == "__main__":
    red, white = load_datasets()
    data = merge_and_process_data(red, white)
    data.show(5)
