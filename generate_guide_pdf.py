"""
Script to generate a professional PDF guide for presenting
the Air Quality Analysis Big Data project to the faculty guide.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (on pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Air Quality Analysis • Guide Presentation & Defense Handbook")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Confidential • Student Project Review Handbook • Apache Spark & PySpark")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    speech_style = ParagraphStyle(
        'Speech_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
    )

    callout_label = ParagraphStyle(
        'CalloutLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=2
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("PROJECT PRESENTATION & GUIDE EXPLANATION MANUAL", title_style))
    story.append(Paragraph("<b>Air Quality Analysis using Apache Spark and PySpark</b><br/>A Step-by-Step Script and Viva Defense Guide for Review with Faculty Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=12))

    # SECTION 1: THE 2-MINUTE ELEVATOR PITCH
    story.append(Paragraph("1. The 2-Minute Elevator Pitch (Opening Statement)", h1_style))
    story.append(Paragraph("When your guide asks: <i>'Give me a summary of your project and what problem it solves'</i>, deliver this exact structured response:", body_style))
    
    pitch_text = """<b>What to say verbatim:</b><br/>
    \"Respected Guide, our final-year Big Data project is titled <b>Air Quality Analysis using Apache Spark and PySpark</b>. 
    In this project, we analyze multi-year environmental time-series data across five major metropolitan Indian cities: 
    <b>Bengaluru, Chennai, Delhi, Hyderabad, and Mumbai</b>, comprising over 12,000 historical records from 2018 to 2024.<br/><br/>
    The core engineering challenge in environmental monitoring is handling <b>disparate, ragged schemas, inconsistent date formats, and missing pollutant readings</b>. 
    Rather than relying on single-threaded libraries like standard Pandas, we engineered an end-to-end distributed data pipeline using 
    <b>Apache Spark 3.5.6</b> running in multi-threaded local mode. Spark enforces strict 9-column schemas, cleans date discrepancies, and performs statistical 
    <b>per-city median imputation</b> using Spark's <code>percentile_approx</code> function.<br/><br/>
    On top of the PySpark aggregation engine, we built an interactive, reactive web dashboard using <b>Streamlit and Plotly</b>. 
    The dashboard enables dynamic multi-city filtering, date range slicing, real-time KPI scorecards, particulate correlation analysis (PM2.5 vs PM10), 
    and export of filtered subsets. Everything runs entirely locally on our laptop without needing heavy cloud credentials or a physical Hadoop cluster.\""""
    
    pitch_box = Table([[Paragraph(pitch_text, speech_style)]], colWidths=[504])
    pitch_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(pitch_box)
    story.append(Spacer(1, 10))

    # SECTION 2: 4-STAGE LIVE DEMONSTRATION WALKTHROUGH
    story.append(Paragraph("2. Step-by-Step Live Demonstration Walkthrough", h1_style))
    story.append(Paragraph("Follow these 4 chronological stages while presenting on screen:", body_style))

    # Stage 1
    story.append(Paragraph("Stage 1: Raw Data Ingestion & Challenges (data/ folder)", h2_style))
    story.append(Paragraph("• <b>Show the folder:</b> Open <code>C:\\AirQualityAnalysis\\data\\</code> containing the 5 CSVs.<br/>"
                           "• <b>Explain the challenge:</b> Mention that raw CSVs contained uneven columns, trailing commas, and mixed date styles (<code>dd/MM/yy</code> vs <code>dd/MM/yyyy</code>).<br/>"
                           "• <b>Run command:</b> <code>python inspect_data.py</code> to show Spark successfully loading schemas with <code>master('local[*]')</code>.", bullet_style))

    # Stage 2
    story.append(Paragraph("Stage 2: Distributed PySpark Data Cleaning Pipeline (clean_data.py)", h2_style))
    story.append(Paragraph("• <b>Open clean_data.py in editor:</b> Highlight the <code>StructType</code> definition for strict 9 columns (City, Date, AQI, PM2.5, PM10, NO2, SO2, CO, O3).<br/>"
                           "• <b>Highlight City Normalization:</b> Show <code>F.when(lower(trim(City)) == 'bangalore', 'Bengaluru')</code>.<br/>"
                           "• <b>Highlight Date Parsing:</b> Show <code>F.coalesce()</code> across three date format patterns.<br/>"
                           "• <b>Highlight Median Imputation:</b> Show <code>F.percentile_approx(col, 0.5)</code> grouped by City. Explain that median was chosen over mean because environmental pollution has extreme outlier events.<br/>"
                           "• <b>Explain Windows Compatibility:</b> Mention that the cleaned dataset is exported via Pandas to <code>output/cleaned_air_quality.csv</code> to bypass Windows-specific <code>winutils.exe</code> limitations while preserving Spark's distributed processing.", bullet_style))

    # Stage 3
    story.append(Paragraph("Stage 3: Spark Distributed Aggregation & Insights (analysis.py)", h2_style))
    story.append(Paragraph("• <b>Run command in terminal:</b> <code>python analysis.py</code><br/>"
                           "• <b>Point to the terminal output:</b><br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Total Records:</b> 12,042 observations across 5 cities spanning 2018 to 2024.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;- <b>City Comparison:</b> Delhi has the highest average AQI (208.29), followed by Mumbai (106.78), Hyderabad (85.40), Chennai (77.33), and Bengaluru (74.32).<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Particulate Matter:</b> Delhi averages 114.56 PM2.5 and 224.95 PM10, nearly 3x higher than Bengaluru (40.88 PM2.5).<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Top 10 Extreme Days:</b> All top 10 peak AQI days occurred in Delhi (peaking at 494.0 in Nov 2019 and Nov 2024), demonstrating intense winter seasonal smog.", bullet_style))

    # Stage 4
    story.append(Paragraph("Stage 4: Interactive Web UI (app.py at http://localhost:8501)", h2_style))
    story.append(Paragraph("• <b>Run command:</b> <code>streamlit run app.py</code> (or switch to the browser window).<br/>"
                           "• <b>Demonstrate Sidebar Filters:</b> Select 'Delhi' and 'Bengaluru' together; observe how KPI cards and charts dynamically update instantly.<br/>"
                           "• <b>Demonstrate Date Slider:</b> Filter down to year 2023–2024 to show responsive query updates.<br/>"
                           "• <b>Walk through the 5 Tabs:</b><br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;1. <i>City Comparison:</i> Bar chart of average AQI and Box plots of outlier spreads.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;2. <i>Yearly & Monthly Trends:</i> Multi-city line chart illustrating the winter smog peak (Nov–Dec).<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Particulate & Pollutants:</i> Scatter plot proving high correlation between PM2.5 and PM10.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;4. <i>Extreme Events:</i> Horizontal ranking chart of top 10 worst pollution days.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;5. <i>Data Explorer:</i> Live searchable preview with a 1-click 'Download Filtered Data as CSV' button.", bullet_style))

    story.append(PageBreak())

    # SECTION 3: KEY BIG DATA CONCEPTS TO HIGHLIGHT
    story.append(Paragraph("3. Core Big Data Concepts You Must Emphasize", h1_style))
    story.append(Paragraph("Guides look for theoretical foundation and mastery of Big Data concepts. Use these exact technical keywords:", body_style))

    concepts_data = [
        [Paragraph("<b>Concept</b>", callout_label), Paragraph("<b>How to Explain to Guide</b>", callout_label)],
        [
            Paragraph("<b>Why PySpark over Pandas?</b>", body_style),
            Paragraph("Pandas executes single-threaded on a single CPU core and is bounded by physical RAM. Apache Spark operates in-memory with parallel partitions across all available cores (<code>local[*]</code>), supporting horizontal scaling for massive multi-gigabyte or streaming sensor datasets.", body_style)
        ],
        [
            Paragraph("<b>Lazy Evaluation & Catalyst Optimizer</b>", body_style),
            Paragraph("Spark does not execute transformations (<code>filter</code>, <code>groupBy</code>, <code>withColumn</code>) immediately. Instead, it constructs a Directed Acyclic Graph (DAG). The Catalyst Optimizer reorganizes expressions and filters before an action (<code>count</code>, <code>show</code>) triggers execution.", body_style)
        ],
        [
            Paragraph("<b>Percentile Imputation (percentile_approx)</b>", body_style),
            Paragraph("Rather than filling missing readings with arbitrary global constants or simple arithmetic means, we used PySpark's <code>percentile_approx(col, 0.5)</code> grouped by City. Median imputation is robust to environmental outliers and preserves regional baseline characteristics.", body_style)
        ],
        [
            Paragraph("<b>Caching Strategy (@st.cache_data & df.cache())</b>", body_style),
            Paragraph("In Spark, <code>df.cache()</code> prevents re-evaluating the upstream DAG across multiple analytical queries. In Streamlit, <code>@st.cache_data</code> stores the parsed dataframe in memory to ensure sub-second UI responsiveness.", body_style)
        ],
        [
            Paragraph("<b>Column Escaping (Backticks)</b>", body_style),
            Paragraph("In Spark SQL, periods represent nested struct fields. Because columns like <code>PM2.5</code> include a dot, PySpark requires backticks (<code>F.col('`PM2.5`')</code>) to reference the literal column name safely.", body_style)
        ]
    ]

    concept_table = Table(concepts_data, colWidths=[150, 354])
    concept_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(concept_table)
    story.append(Spacer(1, 10))

    # SECTION 4: DEFENSE & ANTICIPATED GUIDE QUESTIONS
    story.append(Paragraph("4. Anticipated Guide Questions & Ready-to-Answer Responses", h1_style))
    story.append(Paragraph("Prepare for these common cross-examination questions during your evaluation:", body_style))

    qas = [
        ("Q1: Why did you run Spark in local mode instead of deploying on a physical Hadoop cluster?",
         "Local mode (<code>local[*]</code>) executes the complete Spark engine with multi-threaded parallel executors across all laptop CPU cores. It provides full PySpark API fidelity and Catalyst optimization without the hardware, network, and operational overhead of maintaining a multi-node YARN/HDFS cluster for development and evaluation."),
        ("Q2: Why did you use Pandas to write the CSV file at the end of clean_data.py?",
         "On native Windows machines without Hadoop binaries, Spark's native Hadoop FileSystem writer throws a <code>winutils.exe</code> file permission exception. Exporting the consolidated partition via Pandas cleanly bypasses this Windows OS limitation while preserving all distributed cleaning operations in Spark."),
        ("Q3: Does this dashboard display live or real-time air quality?",
         "No, respected Guide. This is explicitly a historical time-series analytics project analyzing 12,042 validated records from 2018 to 2024. We have clearly documented this limitation in the dashboard footer and README to maintain academic and data-integrity rigor."),
        ("Q4: How would you extend this project into an enterprise production system?",
         "We would ingest live sensor telemetry streams using Apache Kafka, process them in real-time via Spark Structured Streaming, train AQI forecasting models using PySpark MLlib (Random Forest Regressors), and persist data into a Delta Lake on cloud object storage (AWS S3 / GCP Cloud Storage).")
    ]

    for q, a in qas:
        qa_content = f"<b>{q}</b><br/><font color='#1E293B'>{a}</font>"
        qa_box = Table([[Paragraph(qa_content, body_style)]], colWidths=[504])
        qa_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('LINELEFT', (0,0), (-1,-1), 2.5, colors.HexColor("#2563EB")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(qa_box)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 5))

    # SECTION 5: KEY NUMBERS TO MEMORIZE
    story.append(Paragraph("5. Critical Project Statistics to Memorize", h1_style))
    stats_data = [
        [Paragraph("<b>Metric</b>", callout_label), Paragraph("<b>Exact Value</b>", callout_label), Paragraph("<b>Context / Explanation</b>", callout_label)],
        [Paragraph("Total Cleaned Records", body_style), Paragraph("<b>12,042</b>", body_style), Paragraph("Bengaluru: 2556, Hyderabad: 2556, Chennai: 2551, Delhi: 2191, Mumbai: 2188", body_style)],
        [Paragraph("Date Span", body_style), Paragraph("<b>2018 to 2024</b>", body_style), Paragraph("7 full calendar years of observations", body_style)],
        [Paragraph("Delhi Average AQI", body_style), Paragraph("<b>208.29</b>", body_style), Paragraph("Highest in India; Maximum observed AQI reached <b>494.0</b>", body_style)],
        [Paragraph("Bengaluru Average AQI", body_style), Paragraph("<b>74.32</b>", body_style), Paragraph("Lowest / cleanest among the 5 metropolitan cities", body_style)],
        [Paragraph("Dominant Pollutant", body_style), Paragraph("<b>PM2.5 & PM10</b>", body_style), Paragraph("Particulate matter drives >85% of elevated AQI episodes", body_style)]
    ]
    stats_table = Table(stats_data, colWidths=[140, 100, 264])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(stats_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    output_dir = r"C:\AirQualityAnalysis\docs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Project_Guide_Explanation_Guide.pdf")
    build_pdf(pdf_path)

    # Also place a copy at the project root for immediate convenience
    root_pdf_path = os.path.join(r"C:\AirQualityAnalysis", "Project_Guide_Explanation_Guide.pdf")
    build_pdf(root_pdf_path)
