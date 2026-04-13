import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Business Health Dashboard", layout="wide")

st.title("📊 Business Health Monitoring Dashboard")
st.write("A vibe-coded analytics tool for tracking revenue performance and anomalies.")

# -----------------------------
# DUMMY DATA
# -----------------------------
data = {
    "date": [
        "2024-01-01", "2024-01-02", "2024-01-03",
        "2024-01-04", "2024-01-05", "2024-01-06",
        "2024-01-07", "2024-01-08"
    ],
    "region": [
        "Dubai", "Dubai", "Abu Dhabi", "Dubai",
        "Abu Dhabi", "Dubai", "Abu Dhabi", "Dubai"
    ],
    "revenue": [200, 50, 300, 80, 400, 120, 60, 250]
}

df = pd.DataFrame(data)

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", df["region"].unique())

filtered_df = df[df["region"] == region].copy()

# -----------------------------
# BUSINESS LOGIC
# -----------------------------
filtered_df["anomaly"] = filtered_df["revenue"] < 100

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", filtered_df["revenue"].sum())
col2.metric("Average Revenue", round(filtered_df["revenue"].mean(), 2))
col3.metric("Anomalies", int(filtered_df["anomaly"].sum()))

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🧠 Insights")

if filtered_df["revenue"].mean() < 150:
    st.warning("⚠️ Revenue is below expected threshold.")
else:
    st.success("📈 Revenue performance is healthy.")

# -----------------------------
# TABLE VIEW
# -----------------------------
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📈 Revenue Trend")
st.line_chart(filtered_df.set_index("date")["revenue"])

st.subheader("📊 Revenue by Region (Overall)")
st.bar_chart(df.groupby("region")["revenue"].sum())

# -----------------------------
# ALERTS SECTION
# -----------------------------
st.subheader("🚨 Anomaly Detection")

alerts = filtered_df[filtered_df["anomaly"] == True]

if not alerts.empty:
    st.error("Anomalies detected in revenue!")
    st.dataframe(alerts)
else:
    st.success("No anomalies detected.")