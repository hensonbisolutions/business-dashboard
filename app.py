import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Company Screening Tool", layout="wide")

st.title("🏢 AI Company Screening & Ranking Tool")
st.write("Vibe-coded prototype for evaluating and ranking companies using growth, margin, and risk signals.")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"company": "AlphaTech", "sector": "Technology", "revenue": 500, "growth": 25, "margin": 18, "region": "US"},
    {"company": "BetaRetail", "sector": "Retail", "revenue": 300, "growth": 5, "margin": 6, "region": "UK"},
    {"company": "GammaEnergy", "sector": "Energy", "revenue": 800, "growth": 12, "margin": 10, "region": "Middle East"},
    {"company": "DeltaHealth", "sector": "Healthcare", "revenue": 450, "growth": 20, "margin": 15, "region": "EU"},
    {"company": "EpsilonFin", "sector": "Finance", "revenue": 600, "growth": 8, "margin": 22, "region": "US"},
    {"company": "ZetaLogistics", "sector": "Logistics", "revenue": 350, "growth": 18, "margin": 9, "region": "Asia"},
    {"company": "EtaAI", "sector": "Technology", "revenue": 200, "growth": 40, "margin": 5, "region": "US"},
    {"company": "ThetaFoods", "sector": "Food", "revenue": 250, "growth": 6, "margin": 7, "region": "EU"},
]

df = pd.DataFrame(data)

# -----------------------------
# ENRICHMENT
# -----------------------------
def growth_label(x):
    if x > 20:
        return "High"
    elif x > 10:
        return "Medium"
    return "Low"

def risk_label(row):
    if row["growth"] < 10 or row["margin"] < 8:
        return "High Risk"
    elif row["margin"] < 15:
        return "Medium Risk"
    return "Low Risk"

df["growth_signal"] = df["growth"].apply(growth_label)
df["risk"] = df.apply(risk_label, axis=1)

# scoring model (simple but explainable)
df["score"] = (df["growth"] * 0.5) + (df["margin"] * 0.3) + (df["revenue"] * 0.01)

df = df.sort_values("score", ascending=False)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")
sector = st.sidebar.multiselect("Sector", df["sector"].unique(), default=df["sector"].unique())
region = st.sidebar.multiselect("Region", df["region"].unique(), default=df["region"].unique())

filtered = df[(df["sector"].isin(sector)) & (df["region"].isin(region))]

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Companies", len(filtered))
col2.metric("Avg Growth", f"{filtered['growth'].mean():.1f}%")
col3.metric("High Risk Firms", len(filtered[filtered["risk"] == "High Risk"]))

st.divider()

# -----------------------------
# TOP PICKS
# -----------------------------
st.subheader("🏆 Top 3 Companies")
st.dataframe(filtered.head(3)[["company", "sector", "growth", "margin", "score"]])

# -----------------------------
# FULL TABLE
# -----------------------------
st.subheader("📋 Ranked Company List")
st.dataframe(filtered)

# -----------------------------
# VISUALS
# -----------------------------
st.subheader("📊 Growth vs Risk View")

fig = px.scatter(
    filtered,
    x="growth",
    y="margin",
    color="risk",
    size="revenue",
    hover_name="company",
    title="Company Risk vs Growth Quadrant"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# INSIGHT ENGINE (WOW FACTOR)
# -----------------------------
st.subheader("🧠 AI-Style Insights")

top = filtered.iloc[0]

st.success(
    f"""
    🔎 Top Pick: {top['company']}

    - Sector: {top['sector']}
    - Growth: {top['growth']}%
    - Margin: {top['margin']}%
    - Risk Level: {top['risk']}

    💡 Insight: This company shows the strongest combined growth and margin profile in the current selection.
    """
)