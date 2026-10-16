# Presentation Outline: Air Quality Analysis using Apache Spark and PySpark
*(Recommended 6–8 Slide Deck Outline for Mini-Project Review)*

---

### Slide 1: Title & Team Information
- **Title**: Air Quality Analysis across Indian Metropolitan Cities
- **Subtitle**: Distributed In-Memory Big Data Analytics using Apache Spark & PySpark
- **Presented by**: [Student / Team Name(s)]
- **Roll Number(s)**: [Roll No. / Registration ID]
- **Department**: Department of Computer Science & Engineering / Information Technology
- **Supervisor / Guide**: [Faculty Guide Name]

---

### Slide 2: Problem Statement & Motivation
- **Context**: Rapid urban growth, industrialization, and traffic lead to severe air quality fluctuations in major Indian hubs.
- **Problem**:
  - Disparate CSV records across multiple cities with uneven dates, missing measurements, and irregular formatting.
  - Traditional single-node spreadsheet or SQL tools face scaling constraints as historical observation datasets grow.
- **Goal**: Build a scalable, fault-tolerant Spark pipeline to ingest, clean, impute, and analyze multi-year air quality data, backed by an interactive web UI.

---

### Slide 3: System Architecture & Workflow
- **Pipeline Stages**:
  1. **Raw Ingestion**: 5 city datasets (Bangalore, Chennai, Delhi, Hyderabad, Mumbai).
  2. **Distributed ETL**: SparkSession in `local[*]` mode, StructType schema enforcement, Bangalore->Bengaluru normalization, multi-format date parsing (`dd/MM/yy`, `dd/MM/yyyy`, `yyyy-MM-dd`).
  3. **Statistical Imputation**: Per-city median imputation using PySpark's `percentile_approx`.
  4. **Analytics**: Spark aggregation queries (averages, minimums, maximums, yearly trends).
  5. **Presentation**: Streamlit + Plotly interactive dashboard with reactive sidebar filters.
- *Visual*: Include system architecture block diagram (from `docs/ARCHITECTURE.md`).

---

### Slide 4: Data Processing & Cleaning Challenges
- **Key Technical Challenges Solved**:
  - **Ragged Schemas**: Trailing empty columns in input CSVs solved via explicit 9-column `StructType`.
  - **Date Inconsistencies**: Handled using `F.coalesce()` with multiple date pattern parsers.
  - **Missing Pollutant Data**: Handled without dropping valid records by using per-city median imputation.
  - **Windows Compatibility**: Overcame Windows native write limitation (`winutils.exe`) by leveraging Pandas CSV writer on the aggregated/cleaned dataset.

---

### Slide 5: Key Findings & Analytical Insights
- **City-Level Comparison**:
  - **Delhi**: Highest average AQI (208.29) and severe hazard days reaching 494.0.
  - **Mumbai**: Moderate-high AQI (106.78).
  - **Hyderabad**: Moderate AQI (85.40).
  - **Chennai**: Relatively lower AQI (77.33).
  - **Bengaluru**: Cleanest air profile with average AQI (74.32).
- **Particulate Matter Dynamics**:
  - PM2.5 and PM10 exhibit strong co-variance.
  - Winter spikes (Nov–Jan) recorded across northern and central zones due to weather inversion.

---

### Slide 6: Interactive Web UI (Streamlit & Plotly)
- **Features Demonstrated**:
  - **Real-Time Dynamic KPIs**: Filtered Records, Cities Represented, Mean AQI, Max AQI, Particulate Averages.
  - **Multi-City & Date-Range Filtering**: Reactive widgets update all metrics and charts instantly.
  - **Interactive Plotly Visualizations**:
    - City-wise Average AQI Bar Chart & Box Plot Distributions.
    - Historical Yearly & Seasonal Monthly Trends.
    - PM2.5 vs PM10 Correlation Scatter Plot.
    - Multi-Pollutant Comparative Profiler.
    - Top 10 Highest-AQI Peak Event Tracker.
  - **Data Explorer & Export**: Searchable records preview and 1-click filtered CSV download.

---

### Slide 7: Limitations & Future Enhancements
- **Limitations**:
  - Historical dataset analysis (2018–2024); does not reflect live sensor streaming.
  - Imputation is static median per city; does not capture micro-climate micro-variations.
- **Future Enhancements**:
  - Streaming pipeline using Spark Structured Streaming + Apache Kafka for real-time AQI monitors.
  - Machine Learning integration with PySpark MLlib for predictive AQI forecasting (Random Forest / GBT).
  - Geospatial map visualization with Leaflet/Folium.

---

### Slide 8: Conclusion & Summary
- Successfully delivered an end-to-end Big Data mini-project:
  - 12,042 records cleaned, imputed, and processed.
  - Spark local mode executes aggregations without Hadoop/HDFS overhead.
  - Production-ready Streamlit dashboard providing immediate visual insights.
- **Thank You!** Questions & Answers.
