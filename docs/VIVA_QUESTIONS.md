# Air Quality Analysis: Viva Voce & Technical Interview Q&A

### Q1: What is Apache Spark, and why was it chosen for this project over standard Pandas or SQL?
**A:** Apache Spark is a distributed general-purpose computing system that executes data processing in-memory. While Pandas is constrained to single-core execution and RAM limits of a single machine, Spark scales across multiple cores (or cluster nodes) through resilient distributed datasets (RDDs) and DataFrames, using a lazy evaluation execution plan with the Catalyst optimizer. For expanding time-series sensor datasets, Spark ensures horizontal scalability.

### Q2: What is the significance of using `local[*]` when creating the SparkSession?
**A:** `master("local[*]")` instructs Spark to run locally without a cluster manager (like YARN or Mesos) and automatically allocate as many worker threads as there are logical CPU cores on the local machine. This allows multi-threaded parallel computation on a single developer laptop.

### Q3: Why did you define an explicit `StructType` schema when ingesting the CSV files?
**A:** By specifying an explicit `StructType` schema instead of relying on `inferSchema=True`, we prevent full-file schema scanning passes, handle ragged/trailing empty columns present in raw CSV files, and enforce strict typing (Strings, Doubles, Dates) right at the ingestion boundary.

### Q4: How were missing pollutant values handled during data cleaning?
**A:** Missing values were imputed using the per-city median for each respective pollutant via PySpark's `percentile_approx(col, 0.5)` aggregation function. The median was selected over the mean because environmental pollutant readings often contain severe outliers (e.g., episodic smog spikes), which would bias arithmetic means. Imputing per-city preserves distinct local baseline characteristics.

### Q5: Why was `toPandas().to_csv()` used to export the final cleaned dataset instead of `spark.write.csv()`?
**A:** On native Windows installations without a full Hadoop installation or `winutils.exe` in `HADOOP_HOME`, Spark's native Hadoop FileSystem writer throws a native file permission exception (`UnsatisfiedLinkError` / `winutils.exe` not found). Exporting the consolidated partition via Pandas cleanly bypasses this OS dependency while writing a single unified CSV file.

### Q6: What is lazy evaluation in Apache Spark?
**A:** In Spark, transformations (such as `filter()`, `select()`, `groupBy()`, `withColumn()`) are not executed immediately. Instead, Spark constructs a Directed Acyclic Graph (DAG) of computations. Execution is only triggered when an action (such as `count()`, `show()`, `collect()`, `write`) is called. This allows Spark's Catalyst Optimizer to optimize query plans globally before execution.

### Q7: Why is `F.col("`PM2.5`")` wrapped in backticks in PySpark?
**A:** In PySpark SQL expressions, a period (`.`) is interpreted as a struct field delimiter (navigating nested object properties). Since `PM2.5` contains a period in its column name, backticks are mandatory to inform Spark that it refers to an exact flat column name rather than a nested field.

### Q8: What trends did the historical analysis reveal across Indian cities?
**A:**
- **Delhi** exhibited by far the highest average AQI (208.29) and extreme maximums (494.0), especially during winter months (November).
- **Mumbai** followed with moderate-to-high AQI (106.78).
- **Hyderabad** (85.40), **Chennai** (77.33), and **Bengaluru** (74.32) exhibited significantly cleaner air indices.
- **Particulate Matter (PM2.5 and PM10)** is the primary driver of high AQI across all cities.

### Q9: How is the Streamlit UI kept responsive with large datasets?
**A:** The Streamlit dashboard uses `@st.cache_data` to load the dataset once into memory on startup. Subsequent interactions with sidebar filters (city multiselect, date ranges) filter in-memory data frames and update Plotly charts in sub-second response times without reloading from disk.

### Q10: How can this system be extended for a production enterprise scenario?
**A:**
1. Ingest real-time sensor streams from CPCB / IoT sensors using Apache Kafka.
2. Process live data streams using Spark Structured Streaming.
3. Train predictive forecasting models using PySpark MLlib (e.g., Random Forest or Gradient Boosted Trees).
4. Store historical aggregates in Apache Iceberg / Delta Lake over distributed cloud object storage (AWS S3 or Google Cloud Storage).
