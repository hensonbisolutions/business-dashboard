import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Company Screening Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional corporate styling
st.markdown("""
<style>
    :root {
        --primary-color: #0F3460;
        --secondary-color: #16213E;
        --accent-color: #2C3E50;
        --success-color: #27AE60;
        --warning-color: #F39C12;
        --danger-color: #E74C3C;
        --text-light: #ECF0F1;
        --text-muted: #BDC3C7;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background-color: #F8F9FA;
    }
    
    header {
        background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
        padding: 2.5rem 2rem;
        border-radius: 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 2.5rem;
    }
    
    .stMetric {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        border-left: 4px solid #2C3E50;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #2C3E50;
        margin-bottom: 1.25rem;
    }
    
    .subheader {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F3460;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2C3E50;
    }
    
    .top-company-card {
        background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    .metric-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .badge-high {
        background-color: #E74C3C;
        color: white;
    }
    
    .badge-medium {
        background-color: #F39C12;
        color: #333;
    }
    
    .badge-low {
        background-color: #27AE60;
        color: white;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #2C3E50, transparent);
        margin: 2.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0F3460 0%, #16213E 100%);
        color: white;
    }
    
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: white;
    }
    
    .sidebar .sidebar-content .stMultiSelect, .sidebar .sidebar-content .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
        color: white;
    }
    
    .sidebar .sidebar-content .stMultiSelect label, .sidebar .sidebar-content .stSelectbox label {
        color: #00D4FF;
        font-weight: 600;
    }
    
    .sidebar .sidebar-content .stMultiSelect div[data-baseweb="select"] div, 
    .sidebar .sidebar-content .stSelectbox div[data-baseweb="select"] div {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .sidebar .sidebar-content .stMultiSelect div[data-baseweb="select"] svg, 
    .sidebar .sidebar-content .stSelectbox div[data-baseweb="select"] svg {
        color: #00D4FF;
    }
    
    /* Filter header styling */
    .sidebar .sidebar-content .stMarkdown h1 {
        color: #2C3E50;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        border-bottom: 2px solid #2C3E50;
        padding-bottom: 0.5rem;
    }
    
    /* Enhanced sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F3460 0%, #16213E 100%) !important;
        border-right: 3px solid #2C3E50;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label, 
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Enhanced sidebar multiselect styling */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(44, 62, 80, 0.2) !important;
        border-radius: 8px !important;
        min-height: 40px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"]:hover {
        border-color: #2C3E50 !important;
        box-shadow: 0 0 0 1px rgba(44, 62, 80, 0.1) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"] {
        background: #2C3E50 !important;
        color: white !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
        padding: 2px 6px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #0F3460 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        color: #2C3E50 !important;
    }
    
    /* Label styling */
    [data-testid="stSidebar"] .stMultiSelect label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    /* Sidebar spacing improvements */
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #0F3460 0%, #16213E 100%); 
     padding: 3rem 2rem; 
     border-radius: 0; 
     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); 
     margin-bottom: 2.5rem;
     text-align: center;
     border-bottom: 3px solid #2C3E50;">
    <h1 style="font-size: 2.8rem; font-weight: 600; margin: 0; color: white; letter-spacing: -0.5px; font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;">
        🏢 Company Screening & Ranking Platform
    </h1>
    <p style="font-size: 1rem; margin-top: 1rem; opacity: 0.9; font-weight: 400; letter-spacing: 0.3px; color: rgba(255,255,255,0.95); font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;">
        Enterprise-Grade Intelligence for Investment & Partnership Decisions
    </p>
</div>
""", unsafe_allow_html=True)

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
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
     padding: 1.5rem;
     border-radius: 12px;
     margin-bottom: 1rem;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
     border-top: 3px solid #2C3E50;">
    <h2 style="color: white; font-size: 1.4rem; font-weight: 700; margin: 0 0 1rem 0; text-align: center; letter-spacing: 0.3px;">
        🎯 Smart Filters
    </h2>
    <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0; text-align: center;">
        Refine your company selection
    </p>
</div>
""", unsafe_allow_html=True)

# Filter controls with improved layout
st.sidebar.markdown('<div style="color: white; font-weight: 600; margin-bottom: 0.75rem; margin-top: 0.5rem; font-size: 1rem;">🏭 Sector Selection</div>', unsafe_allow_html=True)
sector = st.sidebar.multiselect(
    "Choose sectors",
    df["sector"].unique(),
    default=df["sector"].unique(),
    key="sector_filter"
)

st.sidebar.markdown('<div style="color: white; font-weight: 600; margin-bottom: 0.75rem; margin-top: 1.5rem; font-size: 1rem;">🌍 Region Selection</div>', unsafe_allow_html=True)
region = st.sidebar.multiselect(
    "Choose regions",
    df["region"].unique(),
    default=df["region"].unique(),
    key="region_filter"
)

# Filter summary
total_sectors = len(df["sector"].unique())
total_regions = len(df["region"].unique())
st.sidebar.markdown(f"""
<div style="background: rgba(44, 62, 80, 0.08);
     padding: 0.75rem;
     border-radius: 6px;
     margin-top: 1.5rem;
     border: 1px solid rgba(44, 62, 80, 0.2);">
    <div style="color: #0F3460; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">📊 Active Filters</div>
    <div style="color: #333; font-size: 0.8rem; line-height: 1.4;">
        <div>🏭 Sectors: <strong>{len(sector)}/{total_sectors}</strong> selected</div>
        <div>🌍 Regions: <strong>{len(region)}/{total_regions}</strong> selected</div>
    </div>
</div>
""", unsafe_allow_html=True)

filtered = df[(df["sector"].isin(sector)) & (df["region"].isin(region))]

# -----------------------------
# KPI CARDS
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Companies", len(filtered), delta=None)
with col2:
    st.metric("📈 Avg Growth", f"{filtered['growth'].mean():.1f}%", delta=None)
with col3:
    st.metric("💰 Avg Margin", f"{filtered['margin'].mean():.1f}%", delta=None)
with col4:
    high_risk = len(filtered[filtered["risk"] == "High Risk"])
    st.metric("⚠️ High Risk", high_risk, delta=None)

# Results summary
st.sidebar.markdown(f"""
<div style="background: rgba(27, 174, 96, 0.1);
     padding: 0.75rem;
     border-radius: 6px;
     margin-top: 1rem;
     border: 1px solid rgba(27, 174, 96, 0.3);">
    <div style="color: #27AE60; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.25rem;">📈 Results</div>
    <div style="color: #27AE60; font-size: 1rem; font-weight: 700;">{len(filtered)} companies</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# TOP PICKS
st.markdown('<h2 class="subheader">🏆 Executive Top 3 Picks</h2>', unsafe_allow_html=True)

for idx, (_, row) in enumerate(filtered.head(3).iterrows(), 1):
    risk_color = "badge-high" if row["risk"] == "High Risk" else "badge-medium" if row["risk"] == "Medium Risk" else "badge-low"
    growth_color = "badge-high" if row["growth_signal"] == "High" else "badge-medium" if row["growth_signal"] == "Medium" else "badge-low"
    
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3 style="color: #0F3460; margin: 0 0 0.5rem 0; font-size: 1.4rem;">
                    #{idx} {row['company']}
                </h3>
                <p style="color: #666; margin: 0; font-size: 0.9rem; font-weight: 500;">{row['sector']} • {row['region']}</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2rem; font-weight: 800; color: #2C3E50;">
                    {row['score']:.1f}
                </div>
                <p style="color: #999; margin: 0; font-size: 0.75rem;">Composite Score</p>
            </div>
        </div>
        <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
            <div style="background: #f5f5f5; padding: 0.75rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600;">Growth</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #0F3460;">{row['growth']}%</div>
            </div>
            <div style="background: #f5f5f5; padding: 0.75rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600;">Margin</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #0F3460;">{row['margin']}%</div>
            </div>
            <div style="background: #f5f5f5; padding: 0.75rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600;">Revenue</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #0F3460;">${row['revenue']}M</div>
            </div>
            <div style="background: #f5f5f5; padding: 0.75rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600;">Risk</div>
                <span class="metric-badge {risk_color}" style="display: block; margin-top: 0.25rem;">{row['risk']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FULL TABLE
st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">📋 Complete Company Rankings</h2>', unsafe_allow_html=True)

display_cols = ["company", "sector", "region", "growth", "margin", "revenue", "score", "risk"]
styled_data = filtered[display_cols].copy()
styled_data = styled_data.rename(columns={
    "company": "Company",
    "sector": "Sector",
    "region": "Region",
    "growth": "Growth %",
    "margin": "Margin %",
    "revenue": "Revenue $M",
    "score": "Score",
    "risk": "Risk Level"
})
st.dataframe(styled_data, width='stretch')

# VISUALS
st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">📊 Market Intelligence Dashboard</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        filtered,
        x="growth",
        y="margin",
        color="risk",
        size="revenue",
        hover_name="company",
        title="Growth vs Margin Quadrant Analysis",
        color_discrete_map={
            "High Risk": "#E74C3C",
            "Medium Risk": "#F39C12",
            "Low Risk": "#27AE60"
        }
    )
    fig.update_layout(
        plot_bgcolor="rgba(240, 240, 240, 0.5)",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=12, color="#0F3460"),
        title_font_size=14,
        height=450
    )
    st.plotly_chart(fig, width='stretch')

with col2:
    fig2 = px.bar(
        filtered.sort_values("score", ascending=True),
        y="company",
        x="score",
        orientation="h",
        title="Companies Ranked by Composite Score",
        labels={"score": "Composite Score", "company": "Company"}
    )
    fig2.update_traces(marker_color="#2C3E50")
    fig2.update_layout(
        plot_bgcolor="rgba(240, 240, 240, 0.5)",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=12, color="#0F3460"),
        title_font_size=14,
        height=450
    )
    st.plotly_chart(fig2, width='stretch')

# Risk Distribution
col3, col4 = st.columns(2)

with col3:
    risk_counts = filtered["risk"].value_counts()
    fig3 = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Distribution",
        color_discrete_map={
            "High Risk": "#E74C3C",
            "Medium Risk": "#F39C12",
            "Low Risk": "#27AE60"
        }
    )
    fig3.update_layout(
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=12, color="#0F3460"),
        title_font_size=14,
        height=400
    )
    st.plotly_chart(fig3, width='stretch')

with col4:
    sector_counts = filtered["sector"].value_counts()
    fig4 = px.pie(
        values=sector_counts.values,
        names=sector_counts.index,
        title="Sector Distribution"
    )
    fig4.update_layout(
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=12, color="#0F3460"),
        title_font_size=14,
        height=400
    )
    st.plotly_chart(fig4, width='stretch')

# INSIGHT ENGINE (WOW FACTOR)
st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">💡 Strategic Intelligence Summary</h2>', unsafe_allow_html=True)

if not filtered.empty:
    top = filtered.iloc[0]
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        # Build top company HTML to prevent script display
        top_html = f'<div class="top-company-card" style="background: linear-gradient(135deg, #0F3460 0%, #16213E 100%); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);"><div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-bottom: 0.5rem;">🎯 Top Investment Opportunity</div><h2 style="margin: 0 0 1rem 0; font-size: 2rem; font-family: \'Segoe UI\', \'Trebuchet MS\', sans-serif;">{top["company"]}</h2><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;"><div><div style="opacity: 0.8; font-size: 0.85rem; margin-bottom: 0.25rem;">Sector</div><div style="font-size: 1.3rem; font-weight: 700;">{top["sector"]}</div></div><div><div style="opacity: 0.8; font-size: 0.85rem; margin-bottom: 0.25rem;">Region</div><div style="font-size: 1.3rem; font-weight: 700;">{top["region"]}</div></div><div><div style="opacity: 0.8; font-size: 0.85rem; margin-bottom: 0.25rem;">Growth</div><div style="font-size: 1.3rem; font-weight: 700;">{top["growth"]}%</div></div><div><div style="opacity: 0.8; font-size: 0.85rem; margin-bottom: 0.25rem;">Margin</div><div style="font-size: 1.3rem; font-weight: 700;">{top["margin"]}%</div></div></div><div style="padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);"><div style="opacity: 0.8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">Risk Assessment</div><span style="display: inline-block; background: #27AE60; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">{top["risk"]}</span></div></div>'
        st.markdown(top_html, unsafe_allow_html=True)
    
    with col_insight2:
        avg_growth = filtered['growth'].mean()
        avg_margin = filtered['margin'].mean()
        low_risk_pct = (len(filtered[filtered['risk'] == 'Low Risk']) / len(filtered) * 100) if len(filtered) > 0 else 0
        
        # Determine growth characteristic and sector focus
        growth_char = 'strong' if avg_growth > 15 else 'moderate' if avg_growth > 10 else 'conservative'
        sector_focus = 'emerging sectors' if low_risk_pct < 40 else 'established sectors'
        recommendation = f"The current portfolio shows {growth_char} growth characteristics. Focus on diversification across {sector_focus} for optimal risk-return balance."
        
        # Build HTML string for Market Insights card
        insight_html = f'<div class="card" style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); border-top: 4px solid #2C3E50; margin-bottom: 1.25rem;"><h3 style="color: #0F3460; margin-top: 0;">Market Insights</h3><div style="margin-bottom: 1.5rem;"><p style="color: #666; margin-bottom: 0.5rem; font-weight: 600;">Portfolio Average Growth</p><div style="font-size: 1.8rem; font-weight: 800; color: #2C3E50;">{avg_growth:.1f}%</div></div><div style="margin-bottom: 1.5rem;"><p style="color: #666; margin-bottom: 0.5rem; font-weight: 600;">Portfolio Average Margin</p><div style="font-size: 1.8rem; font-weight: 800; color: #2C3E50;">{avg_margin:.1f}%</div></div><div style="margin-bottom: 1.5rem;"><p style="color: #666; margin-bottom: 0.5rem; font-weight: 600;">Low Risk Companies</p><div style="font-size: 1.8rem; font-weight: 800; color: #27AE60;">{low_risk_pct:.0f}%</div></div><div style="padding-top: 1rem; border-top: 1px solid #eee;"><p style="color: #666; font-size: 0.9rem; line-height: 1.6; margin: 0;"><strong style="color: #0F3460;">Key Recommendation:</strong> {recommendation}</p></div></div>'
        st.markdown(insight_html, unsafe_allow_html=True)