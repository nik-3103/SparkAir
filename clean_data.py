
import os
from functools import reduce
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType
)

schema = StructType([
    StructField("City", StringType(), True),
    StructField("Date", StringType(), True),
    StructField("AQI", DoubleType(), True),
    StructField("PM2.5", DoubleType(), True),
    StructField("PM10", DoubleType(), True),
    StructField("NO2", DoubleType(), True),
    StructField("SO2", DoubleType(), True),
    StructField("CO", DoubleType(), True),
    StructField("O3", DoubleType(), True)
])

BASE_DIR = r"C:\AirQualityAnalysis"
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

spark = (
    SparkSession.builder
    .appName("AirQualityDataCleaning")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

files = [
    "Bangalore_AQI_Dataset.csv",
    "Chennai_AQI_Dataset.csv",
    "Delhi_AQI_Dataset.csv",
    "Hyderabad_AQI_Dataset.csv",
    "Mumbai_AQI_Dataset.csv",
]

dataframes = []


for filename in files:
    path = os.path.join(DATA_DIR, filename)

    df = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(path)
    )

    # Standardize city names.
    df = df.withColumn(
        "City",
        F.when(
            F.lower(F.trim(F.col("City"))) == "bangalore",
            F.lit("Bengaluru")
        ).otherwise(F.trim(F.col("City")))
    )

    dataframes.append(df)


# Combine all cities.
combined = reduce(
    lambda left, right: left.unionByName(right),
    dataframes
)

print("Records before cleaning:", combined.count())

# Convert dates from the dataset's day/month/year format.
combined = combined.withColumn(
    "Date",
    F.coalesce(
        F.to_date("Date", "dd/MM/yy"),
        F.to_date("Date", "dd/MM/yyyy"),
        F.to_date("Date", "yyyy-MM-dd")
    )
)

# Remove exact duplicate rows.
combined = combined.dropDuplicates()

# Remove rows without essential identifiers.
combined = combined.filter(
    F.col("City").isNotNull() &
    F.col("Date").isNotNull()
)

# Convert AQI and pollutant measurements to numeric types.
numeric_columns = [
    "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"
]


for column in numeric_columns:
    combined = combined.withColumn(
        column,
        F.col(f"`{column}`").cast("double")
    )


# Replace missing pollutant values with the median
# for that pollutant within the same city.

for column in numeric_columns:
    median_values = combined.groupBy("City").agg(
        F.percentile_approx(
            F.col(f"`{column}`"), 0.5
        ).alias("median_value")
    )

    combined = combined.join(
        median_values, on="City", how="left"
    )

    combined = combined.withColumn(
        column,
        F.coalesce(
            F.col(f"`{column}`"),
            F.col("median_value")
        )
    ).drop("median_value")


print("Records after cleaning:", combined.count())

print("\nCleaned schema:")
combined.printSchema()

print("\nRecords per city:")
combined.groupBy("City").count().orderBy("City").show()

print("\nSample cleaned records:")
combined.show(10, truncate=False)


# Save the cleaned dataset as a CSV file.
import pandas as pd

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_file = os.path.join(
    OUTPUT_DIR, "cleaned_air_quality.csv"
)

combined.toPandas().to_csv(output_file, index=False)

print("Cleaned dataset saved to:", output_file)

spark.stop()

