# Project Report Outline: Air Quality Analysis using Apache Spark and PySpark

## 1. Introduction
- **1.1 Background**: Urban air quality in major metropolitan cities (Bengaluru, Chennai, Delhi, Hyderabad, Mumbai) and public health implications.
- **1.2 Problem Statement**: Challenges in ingesting, cleaning, unifying, and analyzing high-volume time-series environmental data from heterogeneous sources.
- **1.3 Objectives**:
  - Implement a Big Data ETL pipeline using Apache Spark / PySpark.
  - Standardize schemas, handle inconsistent date formats, and perform statistical imputation (per-city median).
  - Compute large-scale aggregations: city-wise statistics, particulate matter distributions, temporal trends.
  - Build an interactive, filterable web application with Streamlit and Plotly.

## 2. Literature Review & Technology Stack
- **2.1 Apache Spark & PySpark**: Distributed in-memory data processing framework, resilient distributed datasets (RDDs), Spark DataFrames, Catalyst optimizer.
- **2.2 Python & Scientific Libraries**: Pandas, NumPy.
- **2.3 Visualization & UI**: Streamlit and Plotly for responsive web analytics without heavy frontend frameworks.
- **2.4 Big Data vs. Traditional Approaches**: Scalability advantages of Spark compared to single-threaded relational databases or in-memory Pandas on growing datasets.

## 3. System Architecture & Methodology
- **3.1 High-Level Architecture**: Five-stage pipeline (Data Ingestion, Spark ETL, Processed Storage, Spark Analytics, UI Presentation).
- **3.2 Ingestion & Schema Enforcement**: Defining explicit StructType schemas to protect against ragged or trailing columns.
- **3.3 Data Cleaning & Preprocessing**:
  - City naming normalization (e.g. Bangalore to Bengaluru).
  - Multi-pattern date conversion (`dd/MM/yy`, `dd/MM/yyyy`, `yyyy-MM-dd`).
  - Deduplication and record filtering.
  - Per-city median imputation using `percentile_approx`.
  - Windows-compatible CSV persistence.

## 4. Analysis, Key Findings & Insights
- **4.1 Overall Dataset Metrics**: 12,042 records across 7 calendar years (2018–2024).
- **4.2 City-wise AQI Comparison**:
  - Delhi: Highest average AQI (~208.29) and extreme peaks reaching 494.0.
  - Mumbai: Moderate-to-high average AQI (~106.78).
  - Hyderabad: Average AQI (~85.40).
  - Chennai: Average AQI (~77.33).
  - Bengaluru: Lowest average AQI (~74.32) and cleanest overall air profile.
- **4.3 Particulate Matter (PM2.5 vs PM10)**: Strong linear correlation between PM2.5 and PM10; seasonal spikes during winter months (November–January).
- **4.4 Peak Pollution Events**: Top 10 most severe pollution events all recorded in Delhi during winter crop burning and meteorological inversion periods.

## 5. User Interface & Interactive Dashboard
- **5.1 Layout & Navigation**: Responsive layout with header, KPI cards, sidebar controls, and tabbed visualizations.
- **5.2 Dynamic Filtering**: Multi-city selectors, date boundaries, pollutant drill-down.
- **5.3 Reactive KPIs & Visualizations**: Real-time recalculation of records, city representation, and AQI metrics upon filter interaction.
- **5.4 Export Capabilities**: Filtered CSV data download for offline exploration.

## 6. Challenges, Limitations & Future Scope
- **6.1 Data Limitations**: Historical data (2018–2024) rather than real-time telemetry; variable sensor station density across cities.
- **6.2 Windows Spark Environment**: Handled Windows native library dependencies (`winutils`) cleanly in local mode without requiring Hadoop clusters.
- **6.3 Future Work**:
  - Integration of machine learning models for predictive AQI forecasting (using Spark MLlib).
  - Ingestion of live IoT sensor streams using Spark Structured Streaming and Apache Kafka.
  - Geospatial GIS mapping of monitoring stations.

## 7. Conclusion
- Summary of project achievements, deliverables, and educational takeaways from deploying a big data analytics pipeline.

## 8. References & Appendix
- Central Pollution Control Board (CPCB) standards.
- Apache Spark 3.5 documentation.
