# vision-dashboard

# 📊 Organizational Initiatives & Progress Dashboard

This is an **interactive Streamlit dashboard** to track, visualize, and manage organizational initiatives. It loads data from a CSV file, provides visual insights using Plotly, and allows adding new initiatives with progress tracking.

## 🚀 Features

* **Overview Metrics** – Total initiatives, completed, and in-progress count.
* **Interactive Filters** – Filter by category, status, timeline, and owner.
* **Visual Insights** – Pie charts, bar graphs, histograms for distribution analysis.
* **Progress Tracking** – Individual progress bars with evaluation status.
* **Data Management** – Add new initiatives, download filtered data as Excel.

## 📂 Project Structure

```
project/
│-- vdic_dashboard_ready.csv   # Data file with initiatives
│-- dashboard.py               # Streamlit app code
│-- README.md                   # Project documentation
```

Live App
https://vision-dashboard.streamlit.app/

## 🛠️ Steps to Run

1. **Install Dependencies**

   ```bash
   pip install streamlit pandas plotly openpyxl
   ```
2. **Place your CSV file**

   * Ensure `vdic_dashboard_ready.csv` exists in the same folder.
3. **Run the App**

   ```bash
   streamlit run vdic_dashboard.py
   ```
4. **Use the Dashboard**

   * Apply filters from the sidebar.
   * View progress, category breakdowns, and timelines.
   * Add new initiatives via the form.
   * Download filtered results as Excel.

## 📌 Data Format

The CSV file should have:

```
Title, Category, Assigned To, Status, Timeline, Start Date, Target Date, Progress (%)
```
