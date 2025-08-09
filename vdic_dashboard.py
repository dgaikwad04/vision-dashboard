import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from io import BytesIO

# Path to your existing CSV data file
EXCEL_PATH = "vdic_dashboard_ready.csv"

# Configure page
st.set_page_config(page_title="Strategy & Initiative Dashboard", layout="wide")

# Header (generic business/IT friendly)
st.markdown("""
<h1 style='text-align: center; margin-top: 10px; margin-bottom: 0; font-size: 38px; color: #3778C2;'>
    Organizational Initiatives & Progress Dashboard
</h1>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv(EXCEL_PATH)

# Drop rows without a title
df = df.dropna(subset=['Title'])

# Create essential columns if missing
if 'Initiative ID' not in df.columns:
    df['Initiative ID'] = ['INIT{:03}'.format(i + 1) for i in range(len(df))]

# Rename columns for business context
df = df.rename(columns={
    'Strategy ID': 'Initiative ID',
    'Enabler': 'Category',
    'Term Plan': 'Timeline'
})

# Fill missing columns if not present
if 'Start Date' not in df.columns:
    df['Start Date'] = pd.NaT
if 'Target Date' not in df.columns:
    df['Target Date'] = pd.NaT
if 'Progress (%)' not in df.columns:
    df['Progress (%)'] = 0
if 'Timeline' not in df.columns:
    df['Timeline'] = 'Short-Term'
if 'Evaluation Status' not in df.columns:
    df['Evaluation Status'] = ''

# Convert column types
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['Target Date'] = pd.to_datetime(df['Target Date'], errors='coerce')

# Status evaluation function
def evaluate_status(progress):
    if progress >= 90:
        return "Target Achieved"
    elif 50 <= progress < 90:
        return "Partially Achieved"
    else:
        return "Not Achieved"

df['Evaluation Status'] = df['Progress (%)'].apply(evaluate_status)

# Keep only required columns
df = df[['Initiative ID', 'Title', 'Category', 'Assigned To', 'Status',
         'Timeline', 'Evaluation Status', 'Start Date', 'Target Date', 'Progress (%)']]

# Overview metrics
st.header("📌 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Initiatives", len(df))
col2.metric("Completed", df[df['Status'] == 'Completed'].shape[0])
col3.metric("In Progress", df[df['Status'] == 'In Progress'].shape[0])

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
category_filter = st.sidebar.multiselect("Filter by Category", options=df['Category'].dropna().unique())
status_filter = st.sidebar.multiselect("Filter by Status", options=df['Status'].dropna().unique())
timeline_filter = st.sidebar.multiselect("Filter by Timeline", options=df['Timeline'].dropna().unique())
assigned_filter = st.sidebar.multiselect("Filter by Owner", options=df['Assigned To'].dropna().unique())

# Apply filters
filtered_df = df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
if timeline_filter:
    filtered_df = filtered_df[filtered_df['Timeline'].isin(timeline_filter)]
if assigned_filter:
    filtered_df = filtered_df[filtered_df['Assigned To'].isin(assigned_filter)]

# Remove duplicate columns
filtered_df = filtered_df.loc[:, ~filtered_df.columns.duplicated()]

# Visual insights
st.header("📊 Visual Insights")
col1, col2 = st.columns(2)

with col1:
    status_count = filtered_df['Status'].value_counts().reset_index()
    status_count.columns = ['Status', 'Count']
    st.plotly_chart(
        px.pie(status_count, values='Count', names='Status',
               title='Initiative Status Distribution',
               color_discrete_sequence=px.colors.sequential.RdBu),
        use_container_width=True
    )

with col2:
    category_count = filtered_df['Category'].value_counts().reset_index()
    category_count.columns = ['Category', 'Count']
    st.plotly_chart(
        px.bar(category_count, x='Category', y='Count',
               title='Initiatives per Category',
               color='Category',
               color_discrete_sequence=px.colors.qualitative.Set2),
        use_container_width=True
    )

st.subheader("📈 Progress Distribution")
st.plotly_chart(
    px.histogram(filtered_df, x='Progress (%)', nbins=10,
                 title="Initiative Progress (%) Spread",
                 range_x=[0, 100], color_discrete_sequence=["#3b82f6"]),
    use_container_width=True
)

st.subheader("📊 Timeline Distribution")
timeline_count = filtered_df['Timeline'].value_counts().reset_index()
timeline_count.columns = ['Timeline', 'Count']
st.plotly_chart(
    px.bar(timeline_count, x='Timeline', y='Count',
           title='Initiatives by Timeline',
           color='Timeline',
           color_discrete_sequence=px.colors.qualitative.Set3),
    use_container_width=True
)

st.subheader("📊 Evaluation Status")
eval_count = filtered_df['Evaluation Status'].value_counts().reset_index()
eval_count.columns = ['Evaluation Status', 'Count']
st.plotly_chart(
    px.bar(eval_count, x='Evaluation Status', y='Count',
           title='Achievement Status',
           color='Evaluation Status',
           color_discrete_sequence=px.colors.qualitative.Pastel),
    use_container_width=True
)

# Data table
st.header("📋 Initiative Tracker Table")
st.dataframe(filtered_df, use_container_width=True)

# Export to Excel
def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

excel_data = to_excel(filtered_df)

st.download_button(
    label="📥 Download Filtered Data as Excel",
    data=excel_data,
    file_name="Initiatives_Filtered.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Individual progress bars
st.subheader("📍 Individual Initiative Progress")
for _, row in filtered_df.iterrows():
    st.markdown(f"**{row['Title']}** ({row['Timeline']}) – {row['Evaluation Status']}")
    st.progress(float(row['Progress (%)']) / 100)

# Add Initiative form (safe concat)
st.subheader("➕ Add New Initiative")
with st.form("add_form"):
    title = st.text_input("Title")
    category = st.selectbox("Category", options=sorted(df['Category'].dropna().unique()))
    timeline = st.selectbox("Timeline", options=['Short-Term', 'Mid-Term', 'Long-Term'])
    assigned_to = st.text_input("Owner")
    status = st.selectbox("Status", options=['Not Started', 'In Progress', 'Completed'])
    start_date = st.date_input("Start Date", datetime.now())
    target_date = st.date_input("Target Date", datetime.now())
    progress = st.slider("Progress (%)", 0, 100, 0)
    submit = st.form_submit_button("Add Initiative")

    if submit:
        eval_status = evaluate_status(progress)
        new_row = {
            'Initiative ID': f"INIT{len(df) + 1:03}",
            'Title': title,
            'Category': category,
            'Assigned To': assigned_to,
            'Status': status,
            'Timeline': timeline,
            'Evaluation Status': eval_status,
            'Start Date': pd.to_datetime(start_date),
            'Target Date': pd.to_datetime(target_date),
            'Progress (%)': progress
        }

        # Ensure no duplicate column names
        df = df.loc[:, ~df.columns.duplicated()]

        # Match column order and add new row safely
        new_df = pd.DataFrame([new_row], columns=df.columns)
        df = pd.concat([df, new_df], ignore_index=True)

        # Save updated CSV
        df.to_csv(EXCEL_PATH, index=False)
        st.success("✅ Initiative Added! Please refresh to see it updated.")
