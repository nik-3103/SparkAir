"""
Air Quality Analysis using Apache Spark and PySpark.
This script performs big data aggregations and historical analysis
on the cleaned air quality dataset across five Indian cities.
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType
)

BASE_DIR = r"C:\AirQualityAnalysis"
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "output", "cleaned_air_quality.csv")

def run_analysis():
    print("=" * 70)
    print("   AIR QUALITY ANALYSIS USING APACHE SPARK & PYSPARK (LOCAL MODE)")
    print("=" * 70)

    if not os.path.exists(CLEANED_DATA_PATH):
        raise FileNotFoundError(
            f"Cleaned dataset not found at: {CLEANED_DATA_PATH}\n"
            "Please ensure clean_data.py has been executed."
        )

    # Initialize PySpark Session in local mode
    spark = (
        SparkSession.builder
        .appName("AirQualitySparkAnalysis")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    # Define schema for reading cleaned CSV
    schema = StructType([
        StructField("City", StringType(), False),
        StructField("Date", StringType(), False),
        StructField("AQI", DoubleType(), True),
        StructField("PM2.5", DoubleType(), True),
        StructField("PM10", DoubleType(), True),
        StructField("NO2", DoubleType(), True),
        StructField("SO2", DoubleType(), True),
        StructField("CO", DoubleType(), True),
        StructField("O3", DoubleType(), True)
    ])

    print(f"\n[1] Loading dataset from: {CLEANED_DATA_PATH}")
    df = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(CLEANED_DATA_PATH)
    )

    # Explicitly parse Date to DateType and extract Year
    df = df.withColumn("Date", F.to_date(F.col("Date"), "yyyy-MM-dd"))
    df = df.withColumn("Year", F.year(F.col("Date")))

    # Cache dataframe for multiple aggregations
    df.cache()

    # 1. Dataset Overview & Summary
    total_records = df.count()
    distinct_cities = [row["City"] for row in df.select("City").distinct().collect()]
    date_range = df.select(
        F.min("Date").alias("start_date"),
        F.max("Date").alias("end_date")
    ).collect()[0]

    print("\n--- 1. DATASET SUMMARY ---")
    print(f"Total Records: {total_records}")
    print(f"Number of Cities: {len(distinct_cities)} ({', '.join(sorted(distinct_cities))})")
    print(f"Date Span: {date_range['start_date']} to {date_range['end_date']}")
    print(f"Schema:")
    df.printSchema()

    # 2. City-wise AQI Statistics (Average, Min, Max, Count)
    print("\n--- 2. CITY-WISE AQI STATISTICS (Average, Min, Max) ---")
    city_stats = (
        df.groupBy("City")
        .agg(
            F.count("AQI").alias("Record_Count"),
            F.round(F.avg("AQI"), 2).alias("Avg_AQI"),
            F.round(F.min("AQI"), 2).alias("Min_AQI"),
            F.round(F.max("AQI"), 2).alias("Max_AQI")
        )
        .orderBy(F.col("Avg_AQI").desc())
    )
    city_stats.show(truncate=False)

    # 3. Particulate Matter & Pollutant Analysis (Avg PM2.5, PM10, etc.)
    # Note: Use F.col("`PM2.5`") to avoid period in column name being parsed as struct field
    print("\n--- 3. PARTICULATE MATTER & POLLUTANTS ANALYSIS (Avg PM2.5, PM10, NO2, SO2, CO, O3) ---")
    pm_stats = (
        df.groupBy("City")
        .agg(
            F.round(F.avg(F.col("`PM2.5`")), 2).alias("Avg_PM2_5"),
            F.round(F.avg(F.col("`PM10`")), 2).alias("Avg_PM10"),
            F.round(F.avg(F.col("`NO2`")), 2).alias("Avg_NO2"),
            F.round(F.avg(F.col("`SO2`")), 2).alias("Avg_SO2"),
            F.round(F.avg(F.col("`CO`")), 2).alias("Avg_CO"),
            F.round(F.avg(F.col("`O3`")), 2).alias("Avg_O3")
        )
        .orderBy(F.col("Avg_PM2_5").desc())
    )
    pm_stats.show(truncate=False)

    # 4. Yearly AQI Trends Across Cities
    print("\n--- 4. YEAR-WISE AQI TRENDS ---")
    yearly_stats = (
        df.filter(F.col("Year").isNotNull())
        .groupBy("Year")
        .agg(
            F.round(F.avg("AQI"), 2).alias("Avg_AQI"),
            F.round(F.min("AQI"), 2).alias("Min_AQI"),
            F.round(F.max("AQI"), 2).alias("Max_AQI"),
            F.count("AQI").alias("Observations")
        )
        .orderBy("Year")
    )
    yearly_stats.show(truncate=False)

    # 5. City & Year Cross-Breakdown
    print("\n--- 5. CITY & YEAR AVERAGE AQI CROSS-BREAKDOWN ---")
    city_year_stats = (
        df.filter(F.col("Year").isNotNull())
        .groupBy("City", "Year")
        .agg(F.round(F.avg("AQI"), 2).alias("Avg_AQI"))
        .orderBy("City", "Year")
    )
    city_year_stats.show(50, truncate=False)

    # 6. Top 10 Highest-AQI Observations (Most Severe Events)
    print("\n--- 6. TOP 10 HIGHEST AQI RECORDS (Most Severe Events) ---")
    top_10_aqi = (
        df.select("City", "Date", "AQI", "`PM2.5`", "PM10", "NO2", "SO2", "CO", "O3")
        .orderBy(F.col("AQI").desc())
        .limit(10)
    )
    top_10_aqi.show(truncate=False)

    df.unpersist()
    spark.stop()
    print("\n[OK] PySpark Analysis completed successfully.\n")

if __name__ == "__main__":
    run_analysis()
