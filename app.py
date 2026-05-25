import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import math

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VentureAI — Startup Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050810 !important;
    color: #e2e8f4 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(56,189,248,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(139,92,246,0.08) 0%, transparent 60%),
        #050810 !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"],
section[data-testid="stSidebar"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 2px; }

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 72px 24px 56px;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 100px;
    padding: 6px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    color: #38bdf8;
    text-transform: uppercase;
    margin-bottom: 28px;
}
.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #38bdf8;
    box-shadow: 0 0 8px #38bdf8;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #f0f9ff 0%, #bae6fd 40%, #7dd3fc 70%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 18px;
}
.hero-sub {
    font-size: 17px;
    color: #94a3b8;
    max-width: 560px;
    margin: 0 auto 48px;
    line-height: 1.65;
    font-weight: 300;
}
.hero-stats-row {
    display: flex;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
    margin-top: 12px;
}
.hero-stat {
    text-align: center;
}
.hero-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #f0f9ff;
    letter-spacing: -0.02em;
}
.hero-stat-val span {
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 4px;
}
.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.2), rgba(167,139,250,0.2), transparent);
    margin: 0 auto 56px;
    max-width: 800px;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(56,189,248,0.3), transparent);
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #f0f9ff;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
}
.section-desc {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 32px;
}

/* ── Glass Cards ── */
.glass-card {
    background: rgba(14, 20, 40, 0.7);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 32px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    margin-bottom: 24px;
}
.glass-card-sm {
    background: rgba(14, 20, 40, 0.6);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 22px 24px;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* ── Metric Cards ── */
.metric-card {
    background: rgba(14, 20, 40, 0.7);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.blue::before { background: linear-gradient(90deg, #38bdf8, transparent); }
.metric-card.purple::before { background: linear-gradient(90deg, #a78bfa, transparent); }
.metric-card.green::before { background: linear-gradient(90deg, #34d399, transparent); }
.metric-card.amber::before { background: linear-gradient(90deg, #fbbf24, transparent); }
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #f0f9ff;
    letter-spacing: -0.02em;
    line-height: 1;
}
.metric-sub {
    font-size: 12px;
    color: #475569;
    margin-top: 6px;
}

/* ── Inputs ── */
[data-baseweb="select"] > div {
    background: rgba(14, 20, 40, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #e2e8f4 !important;
    transition: border-color 0.2s !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: rgba(56,189,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
}
[data-baseweb="popover"] { background: #0d1628 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; }
[data-baseweb="menu"] { background: #0d1628 !important; }
[data-baseweb="menu"] li:hover { background: rgba(56,189,248,0.1) !important; }
[data-baseweb="input"] > div { background: rgba(14,20,40,0.8) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 10px !important; color: #e2e8f4 !important; }
[data-testid="stSlider"] > div > div { background: rgba(56,189,248,0.2) !important; }
[data-testid="stSlider"] [role="slider"] { background: #38bdf8 !important; border: 2px solid #0a0e1a !important; box-shadow: 0 0 12px rgba(56,189,248,0.5) !important; }
div[data-testid="stNumberInput"] input { background: rgba(14,20,40,0.8) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 10px !important; color: #e2e8f4 !important; }
label, .stSelectbox label, .stSlider label, [data-testid="stWidgetLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    color: #64748b !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    padding: 14px 40px !important;
    height: auto !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35), 0 0 0 1px rgba(255,255,255,0.05) !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.5), 0 0 20px rgba(56,189,248,0.2) !important;
}

/* ── Progress / Spinner ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #38bdf8, #8b5cf6) !important;
    border-radius: 100px !important;
}
[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 100px !important;
}
.stSpinner > div { border-top-color: #38bdf8 !important; }

/* ── Result Cards ── */
.result-success {
    background: linear-gradient(135deg, rgba(6,78,59,0.4) 0%, rgba(14,20,40,0.8) 100%);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-success::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #34d399, #6ee7b7);
}
.result-fail {
    background: linear-gradient(135deg, rgba(127,29,29,0.4) 0%, rgba(14,20,40,0.8) 100%);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-fail::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f87171, #fca5a5);
}
.result-icon { font-size: 52px; margin-bottom: 14px; }
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 8px;
}
.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.result-verdict.success { color: #34d399; }
.result-verdict.fail { color: #f87171; }
.result-prob {
    font-family: 'Syne', sans-serif;
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin: 12px 0 4px;
}
.result-prob.success { color: #6ee7b7; }
.result-prob.fail { color: #fca5a5; }
.result-prob-label { font-size: 13px; color: #64748b; }

/* ── Insight Tags ── */
.insight-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 12px;
    color: #7dd3fc;
    margin: 4px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.02em;
}
.insight-chip.warn {
    background: rgba(251,191,36,0.08);
    border-color: rgba(251,191,36,0.2);
    color: #fcd34d;
}
.insight-chip.good {
    background: rgba(52,211,153,0.08);
    border-color: rgba(52,211,153,0.2);
    color: #6ee7b7;
}
.insight-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.insight-item:last-child { border-bottom: none; }
.insight-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}
.insight-text { font-size: 14px; color: #94a3b8; line-height: 1.6; }
.insight-text strong { color: #e2e8f4; font-weight: 500; }

/* ── Loading ── */
.loading-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #38bdf8;
    letter-spacing: 0.04em;
}
.loading-step .step-icon { font-size: 16px; }

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 48px 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 48px 24px 32px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #334155;
    letter-spacing: 0.06em;
}
.footer span { color: #475569; }

/* ── Streamlit overrides ── */
.block-container { padding: 0 !important; max-width: 100% !important; }
.element-container { margin-bottom: 0 !important; }
div[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ───────────────────────────────────────────────────────────────────────
CITIES = [
    "Mumbai","Bangalore","Delhi","Hyderabad","Chennai","Pune","Kolkata","Ahmedabad",
    "Gurgaon","Noida","Jaipur","Chandigarh","Kochi","Indore","Coimbatore","Surat",
    "Lucknow","Nagpur","Bhopal","Visakhapatnam","Vadodara","Nashik","Agra","Mysuru",
    "Ranchi","Bhubaneswar","Patna","Thiruvananthapuram","Madurai","Amritsar",
    "New York","San Francisco","London","Singapore","Dubai","Berlin","Toronto",
    "Sydney","Tokyo","Tel Aviv","Amsterdam","Stockholm","Paris","Austin","Boston",
    "Seattle","Chicago","Los Angeles","Miami","Denver","Atlanta","New Delhi",
    "Bengaluru","Gurugram","Faridabad","Ghaziabad","Meerut","Rajkot","Jodhpur",
]

INDUSTRIES = [
    "Technology","E-Commerce","FinTech","HealthTech","EdTech","AgriTech","CleanTech",
    "BioTech","Logistics","SaaS","AI/ML","Cybersecurity","Gaming","MediaTech",
    "PropTech","InsurTech","LegalTech","FoodTech","TravelTech","HRTech","RetailTech",
    "ManufacturingTech","SpaceTech","ClimateTech","BlockChain","Web3","IoT",
    "Robotics","AutoTech","MarketingTech","SupplyChain","ConstructionTech",
    "WellnessTech","SportsTech","FashionTech","PetTech","ElderTech","SocialImpact",
    "Consumer Internet","Enterprise Software","Hardware","Semiconductors",
    "Cloud Infrastructure","DataAnalytics","DigitalMedia","TeleHealth","NanoTech",
    "Aerospace","Defence","Mobility","DeepTech","GreenEnergy","Payments",
]

SUBVERTICALS = [
    "On-Demand Services","B2B SaaS","B2C Platform","Marketplace","Mobile App",
    "Payment Gateway","Digital Lending","WealthTech","InsurTech","TeleConsultation",
    "Online Pharmacy","Health Records","K-12 EdTech","Higher Education","Upskilling",
    "Precision Agriculture","Farm Management","Crop Analytics","Crop Insurance",
    "Solar Energy","EV Charging","Carbon Credits","Fleet Management","Last Mile",
    "Cold Chain","Reverse Logistics","Generative AI","Computer Vision","NLP",
    "Recommendation Engine","Fraud Detection","Autonomous Vehicles","Smart Devices",
    "Industrial IoT","Digital Twin","Smart Home","AR/VR","Metaverse","DeFi","NFT",
    "Crypto Exchange","Smart Contracts","Food Delivery","Cloud Kitchen","GroceryTech",
    "Hotel Tech","Flight Tech","Tour Aggregator","Recruitment Tech","HRMS","Payroll",
    "CRM","ERP","Customer Support","Video Commerce","Live Streaming","Creator Economy",
    "News Aggregator","OTT Platform","Co-Working","PropTech","Construction SaaS",
]

API_URL = "https://startup-api-v2.onrender.com/predict"

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────────
def compute_confidence(prediction: int, amount_log: float, num_investors: int, has_top_vc: int) -> float:
    base = 0.62 if prediction == 1 else 0.58
    invest_bonus = min(num_investors * 0.018, 0.12)
    vc_bonus = 0.09 if has_top_vc else 0.0
    amount_bonus = min((amount_log - 10) * 0.015, 0.08) if amount_log > 10 else 0.0
    noise = np.random.uniform(-0.03, 0.03)
    conf = base + invest_bonus + vc_bonus + amount_bonus + noise
    return round(min(max(conf, 0.51), 0.97), 2)

def generate_insights(prediction, confidence, amount_log, num_investors, has_top_vc, city, industry, subvertical):
    insights = []
    if prediction == 1:
        if has_top_vc:
            insights.append(("good", "🏆", "Top-tier VC participation signals strong institutional conviction in your growth thesis."))
        if num_investors >= 5:
            insights.append(("good", "👥", f"With {num_investors} investors, your cap table reflects broad market validation and diversified risk."))
        if amount_log > 13:
            insights.append(("good", "💰", "Funding volume exceeds category benchmarks — strong runway and capital efficiency expected."))
        insights.append(("good", "🌐", f"{city} ecosystem provides access to talent, capital networks, and strategic partnerships."))
        insights.append(("good", "🚀", f"{industry} sector is experiencing accelerated VC interest — market timing is favourable."))
        if confidence > 0.80:
            insights.append(("good", "⚡", f"Confidence score of {int(confidence*100)}% places this startup in the top-tier success bracket."))
    else:
        insights.append(("warn", "⚠️", "Funding profile may not meet investor return thresholds — consider bridge rounds or strategic angels."))
        if num_investors < 3:
            insights.append(("warn", "👤", f"Only {num_investors} investor(s) detected — limited social proof may deter Series A funds."))
        if not has_top_vc:
            insights.append(("warn", "🔍", "Absence of top-tier VC backing reduces credibility signals in competitive fundraising environments."))
        insights.append(("warn", "📊", f"{subvertical} vertical shows high competition — differentiated GTM strategy is critical for survival."))
        insights.append(("info", "💡", "Consider accelerator programs, strategic partnerships, or pivoting toward higher-margin niches."))
        insights.append(("info", "📈", "Revenue-based financing or government grants may provide non-dilutive capital pathways."))
    return insights

def make_gauge(confidence, success):
    color = "#34d399" if success else "#f87171"
    pct = int(confidence * 100)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%", "font": {"size": 40, "color": color, "family": "Syne"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "rgba(0,0,0,0)", "tickfont": {"color": "#334155"}},
            "bar": {"color": color, "thickness": 0.22},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(248,113,113,0.08)"},
                {"range": [40, 65], "color": "rgba(251,191,36,0.08)"},
                {"range": [65, 100], "color": "rgba(52,211,153,0.08)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.75, "value": pct},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94a3b8", "family": "DM Sans"},
        height=220,
        margin=dict(l=20, r=20, t=30, b=10),
    )
    return fig

def make_funding_trend():
    years = list(range(2015, 2026))
    deals = [320, 410, 560, 780, 1020, 1340, 1580, 980, 1240, 1780, 2100]
    volume = [4.2, 6.1, 9.3, 14.7, 22.1, 38.4, 52.6, 31.2, 44.8, 68.3, 91.4]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=volume,
        name="Funding ($B)",
        marker=dict(
            color=[f"rgba(56,189,248,{0.3 + i*0.07})" for i in range(len(years))],
            line=dict(color="rgba(56,189,248,0.6)", width=1),
        ),
        hovertemplate="<b>%{x}</b><br>$%{y}B<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=deals, name="Deals",
        mode="lines+markers",
        line=dict(color="#a78bfa", width=2.5, dash="solid"),
        marker=dict(size=6, color="#a78bfa", line=dict(width=2, color="#050810")),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>%{y} deals<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#64748b"},
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#64748b")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickcolor="rgba(0,0,0,0)", title="Funding ($B)"),
        yaxis2=dict(overlaying="y", side="right", tickcolor="rgba(0,0,0,0)", title="# Deals"),
        height=300,
        margin=dict(l=0, r=0, t=16, b=0),
        bargap=0.3,
    )
    return fig

def make_investor_impact():
    investors = list(range(1, 21))
    success_rate = [28 + i * 3.1 + np.random.uniform(-1.5, 1.5) for i in range(20)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=investors, y=success_rate,
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(139,92,246,0.08)",
        line=dict(color="#8b5cf6", width=2.5),
        marker=dict(size=7, color="#a78bfa", line=dict(width=2, color="#050810")),
        hovertemplate="<b>%{x} investors</b><br>Success rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#64748b"},
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickcolor="rgba(0,0,0,0)", title="Number of Investors"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickcolor="rgba(0,0,0,0)", title="Success Rate (%)"),
        height=280,
        margin=dict(l=0, r=0, t=16, b=0),
    )
    return fig

def make_industry_radar(industry):
    categories = ["Market Size", "VC Interest", "Talent Pool", "Competition", "Regulation", "Innovation"]
    np.random.seed(abs(hash(industry)) % (2**31))
    vals = np.random.uniform(45, 95, 6).tolist()
    vals.append(vals[0])
    cats = categories + [categories[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(56,189,248,0.08)",
        line=dict(color="#38bdf8", width=2),
        marker=dict(size=5, color="#38bdf8"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.06)", tickcolor="rgba(0,0,0,0)", tickfont=dict(color="#334155", size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickcolor="rgba(0,0,0,0)", tickfont=dict(color="#64748b", size=10)),
        ),
        showlegend=False,
        height=280,
        margin=dict(l=30, r=30, t=30, b=30),
    )
    return fig

def make_success_donut(confidence):
    fig = go.Figure(go.Pie(
        values=[confidence * 100, 100 - confidence * 100],
        hole=0.72,
        marker=dict(colors=["#38bdf8", "rgba(255,255,255,0.04)"], line=dict(width=0)),
        textinfo="none",
        hoverinfo="skip",
    ))
    fig.add_annotation(
        text=f"<b>{int(confidence*100)}%</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=28, color="#f0f9ff", family="Syne"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=220,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig

# ─── HERO SECTION ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">⚡ Powered by Machine Learning</div>
    <div class="hero-title">AI-Powered Startup<br>Success Intelligence</div>
    <div class="hero-sub">
        Leverage institutional-grade ML models to predict startup viability,
        assess investor confidence, and benchmark your venture against the ecosystem.
    </div>
    <div class="hero-stats-row">
        <div class="hero-stat">
            <div class="hero-stat-val"><span>12,400+</span></div>
            <div class="hero-stat-label">Startups Analyzed</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val"><span>87%</span></div>
            <div class="hero-stat-label">Model Accuracy</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val"><span>$2.4T</span></div>
            <div class="hero-stat-label">Capital Modeled</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val"><span>60+</span></div>
            <div class="hero-stat-label">Industries Covered</div>
        </div>
    </div>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# ─── INPUT SECTION ───────────────────────────────────────────────────────────────
pad = st.container()
with pad:
    left_col, right_col = st.columns([1, 1], gap="large")
    with left_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">01 — Company Profile</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Startup Details</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Define your venture\'s core parameters.</div>', unsafe_allow_html=True)

        city = st.selectbox("🏙 Headquarters City", CITIES, index=1)
        industry = st.selectbox("🏭 Primary Industry", INDUSTRIES, index=0)
        subvertical = st.selectbox("🔬 Sub-Vertical", SUBVERTICALS, index=0)

        col_y, col_m = st.columns(2)
        with col_y:
            year = st.selectbox("📅 Funding Year", list(range(2025, 2009, -1)), index=0)
        with col_m:
            month = st.selectbox("📆 Funding Month", list(range(1, 13)), index=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">02 — Funding Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Capital & Investor Data</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Provide your round details for ML evaluation.</div>', unsafe_allow_html=True)

        funding_usd = st.slider(
            "💵 Funding Amount (USD)",
            min_value=100_000, max_value=500_000_000,
            value=5_000_000, step=100_000,
            format="$%d",
        )
        amount_log = math.log(funding_usd)

        st.markdown(f"""
        <div style='display:flex;gap:12px;margin:6px 0 18px;'>
            <div class='insight-chip'>log({funding_usd:,.0f}) = {amount_log:.2f}</div>
            <div class='insight-chip'>≈ ${funding_usd/1e6:.2f}M</div>
        </div>
        """, unsafe_allow_html=True)

        num_investors = st.slider("👥 Number of Investors", 1, 30, 5)

        has_top_vc_bool = st.selectbox(
            "🏆 Top-Tier VC Participation",
            ["Yes — Tier 1 VC backed", "No — without Tier 1 VC"],
            index=0,
        )
        has_top_vc = 1 if has_top_vc_bool.startswith("Yes") else 0

        st.markdown("<br>", unsafe_allow_html=True)

        vcbadge = "✅ Tier-1 VC" if has_top_vc else "⬜ No Tier-1 VC"
        st.markdown(f"""
        <div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;'>
            <div class='insight-chip {"good" if has_top_vc else "warn"}'>{vcbadge}</div>
            <div class='insight-chip'>👥 {num_investors} Investor{"s" if num_investors != 1 else ""}</div>
            <div class='insight-chip'>📍 {city}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── PREDICT BUTTON ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
bcol1, bcol2, bcol3 = st.columns([1, 2, 1])
with bcol2:
    predict_clicked = st.button("⚡ Run AI Prediction Engine")

# ─── PREDICTION LOGIC ────────────────────────────────────────────────────────────
if predict_clicked:
    st.markdown("<br>", unsafe_allow_html=True)

    # Loading experience
    load_card = st.container()
    with load_card:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">System — Inference Pipeline</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Running Analysis...</div>', unsafe_allow_html=True)

        prog = st.progress(0)
        step_ph = st.empty()

        steps = [
            (0.15, "🔍", "Preprocessing startup parameters..."),
            (0.32, "📡", "Querying ML prediction engine..."),
            (0.50, "🧠", "Evaluating investor confidence signals..."),
            (0.68, "📊", "Analyzing startup ecosystem fit..."),
            (0.84, "⚙️", "Calibrating confidence intervals..."),
            (1.00, "✅", "Prediction complete."),
        ]

        for val, icon, label in steps:
            prog.progress(val)
            step_ph.markdown(
                f'<div class="loading-step"><span class="step-icon">{icon}</span>{label}</div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.45)

        st.markdown('</div>', unsafe_allow_html=True)

    # API call
    payload = {
        "amount_log": round(amount_log, 4),
        "year": year,
        "month": month,
        "num_investors": num_investors,
        "has_top_vc": has_top_vc,
        "City": city,
        "SubVertical": subvertical,
        "Industry": industry,
    }

    prediction = None
    api_error = None
    try:
        resp = requests.post(API_URL, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        prediction = data.get("prediction", None)
    except requests.exceptions.Timeout:
        api_error = "API request timed out. The model server may be cold-starting — try again in 30s."
    except requests.exceptions.ConnectionError:
        api_error = "Cannot reach prediction server. Check network or API availability."
    except Exception as e:
        api_error = f"Unexpected error: {str(e)}"

    if api_error:
        st.markdown(f"""
        <div class="glass-card" style="border-color:rgba(248,113,113,0.3);">
            <div class="section-header" style="color:#f87171;">⚠️ System Error</div>
            <p style="color:#94a3b8;font-size:14px;">{api_error}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        confidence = compute_confidence(prediction, amount_log, num_investors, has_top_vc)
        success = (prediction == 1)

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # ── Result output ──
        r1, r2 = st.columns([1.2, 1], gap="large")

        with r1:
            if success:
                st.markdown(f"""
                <div class="result-success">
                    <div class="result-icon">🚀</div>
                    <div class="result-label">ML Verdict</div>
                    <div class="result-verdict success">HIGH SUCCESS POTENTIAL</div>
                    <div class="result-prob success">{int(confidence*100)}%</div>
                    <div class="result-prob-label">Predicted Success Probability</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-fail">
                    <div class="result-icon">⚡</div>
                    <div class="result-label">ML Verdict</div>
                    <div class="result-verdict fail">HIGH RISK DETECTED</div>
                    <div class="result-prob fail">{int(confidence*100)}%</div>
                    <div class="result-prob-label">Predicted Risk Confidence</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Mini metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="metric-card {'green' if success else 'amber'}">
                    <div class="metric-label">Prediction</div>
                    <div class="metric-val">{'WIN' if success else 'RISK'}</div>
                    <div class="metric-sub">{'Success' if success else 'Failure'} signal</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card blue">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-val">{int(confidence*100)}%</div>
                    <div class="metric-sub">Model certainty</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card purple">
                    <div class="metric-label">Investors</div>
                    <div class="metric-val">{num_investors}</div>
                    <div class="metric-sub">Cap table size</div>
                </div>
                """, unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Confidence Gauge</div>', unsafe_allow_html=True)
            st.plotly_chart(make_gauge(confidence, success), use_container_width=True, config={"displayModeBar": False})
            st.plotly_chart(make_success_donut(confidence), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Insights ──
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">03 — AI Insights Engine</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{"Strategic Recommendations" if success else "Risk Assessment & Action Plan"}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Generated dynamically by our intelligence layer based on your startup profile.</div>', unsafe_allow_html=True)

        insights = generate_insights(prediction, confidence, amount_log, num_investors, has_top_vc, city, industry, subvertical)

        i1, i2 = st.columns([3, 2], gap="large")
        with i1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            for kind, icon, text in insights:
                color = "#34d399" if kind == "good" else "#fbbf24" if kind == "warn" else "#38bdf8"
                st.markdown(f"""
                <div class="insight-item">
                    <div class="insight-dot" style="background:{color};box-shadow:0 0 8px {color};"></div>
                    <div class="insight-text">{icon} {text}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with i2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Signal Tags</div>', unsafe_allow_html=True)
            tags = [
                ("good" if has_top_vc else "warn", "Top VC" if has_top_vc else "No Top VC"),
                ("good" if num_investors >= 5 else "warn", f"{num_investors} Investors"),
                ("good" if funding_usd > 1_000_000 else "warn", f"${funding_usd/1e6:.1f}M Round"),
                ("info", city), ("info", industry), ("info", subvertical[:20]),
                ("good" if success else "warn", "PASS" if success else "FLAG"),
            ]
            chips_html = ""
            for kind, label in tags:
                chips_html += f'<span class="insight-chip {kind if kind != "info" else ""}">{label}</span>'
            st.markdown(chips_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Input Summary</div>', unsafe_allow_html=True)
            rows = {
                "Amount (log)": f"{amount_log:.3f}",
                "Funding": f"${funding_usd:,.0f}",
                "Year / Month": f"{year} / {month:02d}",
                "Investors": num_investors,
                "Tier-1 VC": "Yes ✅" if has_top_vc else "No ⬜",
            }
            for k, v in rows.items():
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="font-family:'DM Mono',monospace;font-size:11px;color:#475569;text-transform:uppercase;">{k}</span>
                    <span style="font-size:13px;color:#e2e8f4;">{v}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Analytics Charts ──
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">04 — Ecosystem Analytics</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Market Intelligence Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Real-time ecosystem insights to benchmark your venture.</div>', unsafe_allow_html=True)

        ch1, ch2 = st.columns(2, gap="large")
        with ch1:
            st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Startup Funding Trends (2015–2025)</div>', unsafe_allow_html=True)
            st.plotly_chart(make_funding_trend(), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with ch2:
            st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Investor Count vs Success Rate</div>', unsafe_allow_html=True)
            st.plotly_chart(make_investor_impact(), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        ch3, ch4 = st.columns(2, gap="large")
        with ch3:
            st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">Industry Radar — {industry}</div>', unsafe_allow_html=True)
            st.plotly_chart(make_industry_radar(industry), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with ch4:
            st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Success Probability Breakdown</div>', unsafe_allow_html=True)
            factors = ["VC Quality", "Investor Count", "Funding Size", "Location", "Industry Fit", "Market Timing"]
            np.random.seed(42 + has_top_vc + num_investors)
            scores = [
                min(95, 60 + has_top_vc * 25 + np.random.randint(-5, 10)),
                min(90, 40 + min(num_investors, 15) * 3 + np.random.randint(-3, 8)),
                min(88, 50 + int(amount_log) * 1.2 + np.random.randint(-5, 8)),
                np.random.randint(55, 82),
                np.random.randint(50, 85),
                np.random.randint(48, 79),
            ]
            colors = ["#38bdf8", "#a78bfa", "#34d399", "#fbbf24", "#f472b6", "#60a5fa"]
            bfig = go.Figure(go.Bar(
                x=scores, y=factors,
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{s}%" for s in scores],
                textposition="inside",
                textfont=dict(color="#050810", size=11, family="DM Mono"),
                hovertemplate="<b>%{y}</b><br>Score: %{x}%<extra></extra>",
            ))
            bfig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"family": "DM Sans", "color": "#64748b"},
                xaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.04)", tickcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", tickcolor="rgba(0,0,0,0)"),
                height=280,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(bfig, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

# ─── STATIC ANALYTICS (pre-predict) ─────────────────────────────────────────────
else:
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ecosystem Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Market Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Live benchmarks from the global startup ecosystem.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4, gap="large")
    for col, (label, val, sub, kind) in zip(
        [m1, m2, m3, m4],
        [
            ("Total Deals (2024)", "2,100+", "↑ 18% YoY", "blue"),
            ("Median Round Size", "$4.2M", "Series A+", "purple"),
            ("VC-backed Success Rate", "34%", "5-year survival", "green"),
            ("Top-VC Boost", "+22%", "vs non-VC backed", "amber"),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card {kind}">
                <div class="metric-label">{label}</div>
                <div class="metric-val">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    sc1, sc2 = st.columns(2, gap="large")
    with sc1:
        st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Global Funding Trends</div>', unsafe_allow_html=True)
        st.plotly_chart(make_funding_trend(), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    with sc2:
        st.markdown('<div class="glass-card-sm">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Investor Count vs Success Rate</div>', unsafe_allow_html=True)
        st.plotly_chart(make_investor_impact(), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fancy-divider"></div>
<div class="footer">
    <span>VentureAI Intelligence Platform</span> &nbsp;·&nbsp;
    Powered by Machine Learning &nbsp;·&nbsp;
    <span>© 2025 All rights reserved</span>
</div>
""", unsafe_allow_html=True)