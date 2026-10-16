
import os
from pyspark.sql import SparkSession

DATA_DIR = r"C:\AirQualityAnalysis\data"

spark = (
    SparkSession.builder
    .appName("AirQualityDataInspection")
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

for filename in files:
    filepath = os.path.join(DATA_DIR, filename)

    print("\n" + "=" * 60)
    print("FILE:", filename)
    print("=" * 60)

    if not os.path.exists(filepath):
        print("ERROR: File not found!")
        continue

    try:
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(filepath)
        )

        print("Columns:", df.columns)
        print("Schema:")
        df.printSchema()

        print("Total records:", df.count())
        print("First 5 rows:")
        df.show(5, truncate=False)

    except Exception as e:
        print("ERROR:", str(e))

spark.stop()
