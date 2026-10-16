"""
Air Quality Analysis Dashboard
Interactive Streamlit Web UI with Plotly Visualizations
Dataset: Historical Air Quality across 5 Indian Cities (PySpark cleaned)
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Hide Streamlit Top Bar, Deploy Button, Menu, and Decoration Line */
    #MainMenu {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stDeployButton {display: none !important;}
    #manage-app-button {display: none !important;}
    .block-container {
        padding-top: 1.5rem !important;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
    }
    .kpi-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    .footer-note {
        font-size: 0.85rem;
        color: #64748B;
        border-top: 1px solid #E2E8F0;
        padding-top: 1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Path to processed CSV
DATA_PATH = os.path.join(r"C:\AirQualityAnalysis", "output", "cleaned_air_quality.csv")

@st.cache_data
def load_data(path: str):
    """Load cleaned air quality dataset and add temporal features."""
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "City"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    return df

# Load Dataset
data = load_data(DATA_PATH)

# Handle Missing Data Gracefully
if data is None or data.empty:
    st.error("⚠️ **Cleaned Dataset Not Found!**")
    st.info(
        f"Expected path: `{DATA_PATH}`\n\n"
        "Please run the PySpark data cleaning pipeline first by executing in PowerShell:\n"
        "```powershell\n"
        "cd C:\\AirQualityAnalysis\n"
        "python clean_data.py\n"
        "```"
    )
    st.stop()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.title("🎛️ Filter Controls")
st.sidebar.markdown("Filter observations across cities and dates.")

all_cities = sorted(data["City"].unique().tolist())

# City Selection
selected_cities_input = st.sidebar.multiselect(
    "Select City / Cities:",
    options=["All Cities"] + all_cities,
    default=["All Cities"]
)

if "All Cities" in selected_cities_input or len(selected_cities_input) == 0:
    active_cities = all_cities
else:
    active_cities = [c for c in selected_cities_input if c != "All Cities"]

# Date Range Selection
min_date = data["Date"].min().date()
max_date = data["Date"].max().date()

date_selection = st.sidebar.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Parse Date Range safely
if isinstance(date_selection, tuple) and len(date_selection) == 2:
    start_date, end_date = date_selection
elif isinstance(date_selection, tuple) and len(date_selection) == 1:
    start_date = end_date = date_selection[0]
else:
    start_date, end_date = min_date, max_date

# Optional Pollutant Filter for charts
pollutants_list = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
selected_pollutant = st.sidebar.selectbox(
    "Focus Pollutant (for deep-dive):",
    options=pollutants_list,
    index=0
)

# Apply Filters
filtered_df = data[
    (data["City"].isin(active_cities)) &
    (data["Date"].dt.date >= start_date) &
    (data["Date"].dt.date <= end_date)
].copy()

# Sidebar summary badge
st.sidebar.markdown("---")
st.sidebar.caption(f"📁 Dataset Total: **{len(data):,}** rows")
st.sidebar.caption(f"🔍 Filtered Rows: **{len(filtered_df):,}** rows")
st.sidebar.caption(f"📅 Span: **{min_date}** to **{max_date}**")

# Reset Filter instructions
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# ----------------- MAIN DASHBOARD -----------------
st.markdown('<div class="main-title">Air Quality Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A Big Data analytics dashboard exploring historical Air Quality Index (AQI) '
    'and pollutant trends across five major Indian cities. Powered by Apache Spark & PySpark.</div>',
    unsafe_allow_html=True
)

# Handle Empty Filter Results
if filtered_df.empty:
    st.warning("⚠️ **No records match your selected filter criteria.** Please expand your date range or select different cities.")
    st.stop()

# ----------------- KPI METRIC ROW -----------------
total_records = len(filtered_df)
num_cities_represented = filtered_df["City"].nunique()
avg_aqi = filtered_df["AQI"].mean()
max_aqi = filtered_df["AQI"].max()
min_aqi = filtered_df["AQI"].min()
avg_pm25 = filtered_df["PM2.5"].mean()
avg_pm10 = filtered_df["PM10"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Filtered Records</div>
        <div class="kpi-value">{total_records:,}</div>
        <div class="kpi-desc">Across selected range</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Cities Represented</div>
        <div class="kpi-value">{num_cities_represented} / 5</div>
        <div class="kpi-desc">{", ".join(filtered_df['City'].unique())}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    aqi_color = "#10B981" if avg_aqi <= 50 else "#F59E0B" if avg_aqi <= 100 else "#EF4444"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average AQI</div>
        <div class="kpi-value" style="color: {aqi_color};">{avg_aqi:.1f}</div>
        <div class="kpi-desc">Min: {min_aqi:.0f} | Max: {max_aqi:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Maximum AQI</div>
        <div class="kpi-value" style="color: #991B1B;">{max_aqi:.0f}</div>
        <div class="kpi-desc">Peak observed level</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Particulate</div>
        <div class="kpi-value" style="font-size: 1.45rem;">PM2.5: {avg_pm25:.1f}</div>
        <div class="kpi-desc">PM10: {avg_pm10:.1f} µg/m³</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TABS FOR VISUALIZATION -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 City Comparison",
    "📈 Yearly & Monthly Trends",
    "🔬 Particulate & Pollutants",
    "🚨 Extreme Events (Top 10 AQI)",
    "📋 Data Explorer & Export"
])

# ----------------- TAB 1: CITY COMPARISON -----------------
with tab1:
    st.subheader("City-wise Average AQI & Distribution")
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        city_avg = (
            filtered_df.groupby("City", as_index=False)["AQI"]
            .agg(Mean_AQI="mean", Min_AQI="min", Max_AQI="max", Count="count")
            .sort_values(by="Mean_AQI", ascending=False)
        )

        fig_city_bar = px.bar(
            city_avg,
            x="City",
            y="Mean_AQI",
            text=city_avg["Mean_AQI"].round(1),
            color="Mean_AQI",
            color_continuous_scale="Reds",
            title="Average AQI by City",
            labels={"Mean_AQI": "Average AQI", "City": "City"}
        )
        fig_city_bar.update_traces(textposition="outside")
        fig_city_bar.update_layout(height=420, showlegend=False)
        st.plotly_chart(fig_city_bar, use_container_width=True)

    with col_chart2:
        fig_box = px.box(
            filtered_df,
            x="City",
            y="AQI",
            color="City",
            title="AQI Spread & Outlier Distribution by City",
            points="outliers"
        )
        fig_box.update_layout(height=420, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### Summary Statistics Table")
    st.dataframe(
        city_avg.rename(columns={
            "Mean_AQI": "Average AQI",
            "Min_AQI": "Minimum AQI",
            "Max_AQI": "Maximum AQI",
            "Count": "Total Observations"
        }).style.format({
            "Average AQI": "{:.2f}",
            "Minimum AQI": "{:.1f}",
            "Maximum AQI": "{:.1f}",
            "Total Observations": "{:,}"
        }),
        use_container_width=True
    )

# ----------------- TAB 2: YEARLY & MONTHLY TRENDS -----------------
with tab2:
    st.subheader("Historical AQI Trends Over Time")
    col_trend1, col_trend2 = st.columns([1, 1])

    with col_trend1:
        yearly_trend = (
            filtered_df.groupby(["Year", "City"], as_index=False)["AQI"]
            .mean()
            .sort_values(by=["Year", "City"])
        )

        fig_year_trend = px.line(
            yearly_trend,
            x="Year",
            y="AQI",
            color="City",
            markers=True,
            title="Yearly Average AQI Trend by City",
            labels={"AQI": "Average AQI", "Year": "Year"}
        )
        fig_year_trend.update_layout(height=420, xaxis=dict(dtick=1))
        st.plotly_chart(fig_year_trend, use_container_width=True)

    with col_trend2:
        # Monthly Seasonality Pattern
        monthly_trend = (
            filtered_df.groupby(["Month", "Month_Name", "City"], as_index=False)["AQI"]
            .mean()
            .sort_values(by="Month")
        )

        fig_month_trend = px.line(
            monthly_trend,
            x="Month_Name",
            y="AQI",
            color="City",
            markers=True,
            title="Seasonal Trend: Average AQI by Month of Year",
            labels={"AQI": "Average AQI", "Month_Name": "Month"}
        )
        fig_month_trend.update_layout(height=420)
        st.plotly_chart(fig_month_trend, use_container_width=True)

    # Granular Monthly Timeline
    st.markdown("#### Continuous Monthly Timeline")
    timeline_df = (
        filtered_df.groupby(["YearMonth", "City"], as_index=False)["AQI"]
        .mean()
        .sort_values(by="YearMonth")
    )
    fig_timeline = px.line(
        timeline_df,
        x="YearMonth",
        y="AQI",
        color="City",
        title="Continuous Monthly AQI Timeline (2018 – 2024)",
        labels={"YearMonth": "Month-Year", "AQI": "Average AQI"}
    )
    fig_timeline.update_layout(height=380, xaxis_tickangle=-45)
    st.plotly_chart(fig_timeline, use_container_width=True)

# ----------------- TAB 3: PARTICULATE & POLLUTANTS -----------------
with tab3:
    st.subheader("Particulate Matter (PM2.5 vs PM10) & Multi-Pollutant Profiles")
    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        # PM2.5 vs PM10 Correlation Scatter Plot
        fig_pm_scatter = px.scatter(
            filtered_df,
            x="PM10",
            y="PM2.5",
            color="City",
            hover_data=["Date", "AQI"],
            title="PM2.5 vs PM10 Particulate Matter Correlation",
            opacity=0.65,
            labels={"PM10": "PM10 (µg/m³)", "PM2.5": "PM2.5 (µg/m³)"}
        )
        fig_pm_scatter.update_layout(height=440)
        st.plotly_chart(fig_pm_scatter, use_container_width=True)

    with col_p2:
        # Average Pollutant Profile by City
        pollutant_cols = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
        pollutant_means = filtered_df.groupby("City")[pollutant_cols].mean().reset_index()
        pollutant_melted = pollutant_means.melt(id_vars="City", var_name="Pollutant", value_name="Concentration")

        fig_pollutants = px.bar(
            pollutant_melted,
            x="Pollutant",
            y="Concentration",
            color="City",
            barmode="group",
            title="Multi-Pollutant Average Comparison Across Cities",
            labels={"Concentration": "Average Concentration (µg/m³)", "Pollutant": "Pollutant"}
        )
        fig_pollutants.update_layout(height=440)
        st.plotly_chart(fig_pollutants, use_container_width=True)

    # Single Pollutant Deep Dive
    st.markdown(f"#### Deep-Dive: {selected_pollutant} Distribution Across Cities")
    fig_hist = px.histogram(
        filtered_df,
        x=selected_pollutant,
        color="City",
        barmode="overlay",
        marginal="box",
        title=f"Histogram and Density Distribution for {selected_pollutant}",
        opacity=0.6
    )
    fig_hist.update_layout(height=380)
    st.plotly_chart(fig_hist, use_container_width=True)

# ----------------- TAB 4: EXTREME EVENTS -----------------
with tab4:
    st.subheader("Top 10 Highest AQI Observations (Most Severe Events)")
    st.markdown("Identifies the single highest pollution days recorded in the dataset.")

    top_10_df = filtered_df.sort_values(by="AQI", ascending=False).head(10).reset_index(drop=True)
    top_10_df["Rank"] = range(1, len(top_10_df) + 1)
    top_10_df["Date_Str"] = top_10_df["Date"].dt.strftime("%Y-%m-%d")

    fig_top10 = px.bar(
        top_10_df,
        x="AQI",
        y="Date_Str",
        color="City",
        orientation="h",
        text="AQI",
        title="Top 10 Peak AQI Days",
        labels={"Date_Str": "Date", "AQI": "AQI Level"}
    )
    fig_top10.update_layout(yaxis=dict(autorange="reversed"), height=420)
    fig_top10.update_traces(textposition="outside")
    st.plotly_chart(fig_top10, use_container_width=True)

    display_cols = ["Rank", "City", "Date_Str", "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    st.dataframe(
        top_10_df[display_cols].rename(columns={"Date_Str": "Date"}),
        use_container_width=True
    )

# ----------------- TAB 5: DATA EXPLORER & EXPORT -----------------
with tab5:
    st.subheader("Filtered Dataset Preview & Export")
    st.markdown(f"Displaying **{len(filtered_df):,}** records matching current filter criteria.")

    table_cols = ["City", "Date", "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    preview_df = filtered_df[table_cols].copy()
    preview_df["Date"] = preview_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(preview_df.head(100), use_container_width=True)

    # Download Filtered CSV
    csv_bytes = preview_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_air_quality.csv",
        mime="text/csv"
    )

# ----------------- FOOTER & DISCLAIMER -----------------
st.markdown("""
<div class="footer-note">
    <strong>Dataset Source & Data-Quality Limitations:</strong><br>
    • This dashboard presents <em>historical dataset analysis</em> across 2018–2024 for five Indian cities 
      (Bengaluru, Chennai, Delhi, Hyderabad, and Mumbai).<br>
    • Data has been cleaned using Apache Spark / PySpark with per-city median imputation for missing pollutant values.<br>
    • <strong>Disclaimer:</strong> This application is for academic and educational analysis. It does NOT provide live or real-time 
      air quality monitoring and must not be used as medical advice or authoritative regulatory health categorization.
</div>
""", unsafe_allow_html=True)
