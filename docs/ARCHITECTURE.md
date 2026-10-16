# Architecture & Data Pipeline: Air Quality Analysis

## End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Data_Layer ["1. Data Layer (Source Datasets)"]
        D1["Bangalore_AQI_Dataset.csv"]
        D2["Chennai_AQI_Dataset.csv"]
        D3["Delhi_AQI_Dataset.csv"]
        D4["Hyderabad_AQI_Dataset.csv"]
        D5["Mumbai_AQI_Dataset.csv"]
    end

    subgraph Cleaning_Layer ["2. Distributed ETL Engine (Apache Spark / PySpark 3.5.6)"]
        SPARK_INIT["SparkSession (local[*])"]
        SCHEMA["Strict StructType Schema Definition (9 Columns)"]
        UNION["Dataset Union across 5 Cities (12,042 rows)"]
        STD["City Name Standardization (e.g. Bangalore -> Bengaluru)"]
        PARSE_DATE["Multi-format Date Parsing (dd/MM/yy, dd/MM/yyyy, yyyy-MM-dd)"]
        DEDUP["Deduplication & Null Identifier Filtering"]
        MEDIAN["Per-City Median Imputation (percentile_approx)"]
        EXPORT["Cleaned CSV Export via Pandas Engine (Bypasses Winutils write limitation)"]
    end

    subgraph Storage_Layer ["3. Processed Storage"]
        CSV_OUT["output/cleaned_air_quality.csv (12,042 Rows, 0 Nulls)"]
    end

    subgraph Analytics_Layer ["4. Big Data Aggregation & Analysis"]
        PYSPARK_ANALYZE["analysis.py (PySpark Aggregations)"]
        METRICS_CITY["City-wise Avg / Min / Max AQI"]
        METRICS_YEAR["Yearly & Monthly AQI Trends (2018–2024)"]
        METRICS_PM["PM2.5 vs PM10 Particulate Matter Correlations"]
        TOP10["Peak Air Pollution Event Extraction (Top 10 AQI)"]
    end

    subgraph UI_Layer ["5. Interactive Web Dashboard (Streamlit & Plotly)"]
        APP["app.py (Streamlit Application)"]
        CACHE["Streamlit In-Memory Data Caching (@st.cache_data)"]
        FILTERS["Sidebar Controls: Multi-City Selector & Dynamic Date Range"]
        KPIS["Real-time KPI Metric Cards"]
        CHART1["City Comparison (Plotly Bar & Box Plots)"]
        CHART2["Temporal Trends (Yearly & Seasonal Curves)"]
        CHART3["Particulate Correlation & Multi-Pollutant Distribution"]
        CHART4["Peak AQI Event Rankings"]
        EXPLORER["Interactive Table Preview & Filtered CSV Downloader"]
    end

    %% Pipeline Connections
    D1 & D2 & D3 & D4 & D5 --> SPARK_INIT --> SCHEMA --> UNION
    UNION --> STD --> PARSE_DATE --> DEDUP --> MEDIAN --> EXPORT --> CSV_OUT
    CSV_OUT --> PYSPARK_ANALYZE
    PYSPARK_ANALYZE --> METRICS_CITY & METRICS_YEAR & METRICS_PM & TOP10
    CSV_OUT --> CACHE --> APP
    APP --> FILTERS --> KPIS & CHART1 & CHART2 & CHART3 & CHART4 & EXPLORER
```

## Architectural Highlights
- **Engine**: Apache Spark 3.5.6 running in local multithreaded mode (`local[*]`).
- **No Hadoop / HDFS Requirement**: Fully standalone on local Windows environments without requiring `winutils.exe` or cluster daemons.
- **Resilient Pipeline**: Fixed schema ingestion isolates trailing commas/columns present in raw files.
- **Fast Caching**: Cleaned data cached in Streamlit for sub-second reactive filter updates.
