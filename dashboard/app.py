"""PulseGrid - Retail Analytics — Main Entry Point."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# pyrefly: ignore[missing-import]
import streamlit as st

st.set_page_config(
    page_title="PulseGrid - Retail Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  /* ── Base App Surface ── */
  html, body, .stApp {
    background-color: #0F172A !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    color: #E2E8F0 !important;
  }

  .block-container {
    padding: 1.75rem 2rem 3rem 2rem !important;
    max-width: 1440px !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #0B132B !important;
    border-right: 1px solid #1E293B !important;
  }

  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div,
  [data-testid="stSidebar"] label {
    color: #94A3B8 !important;
  }

  /* Radio navigation */
  [data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    padding: 6px 10px;
    border-radius: 8px;
    transition: all 0.15s ease;
  }

  [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(30, 41, 59, 0.6);
  }

  [data-testid="stSidebar"] [data-testid="stRadio"] label span {
    color: #CBD5E1 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
  }

  [data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
    background: rgba(2, 132, 199, 0.15) !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    border-radius: 8px;
  }

  [data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] span {
    color: #38BDF8 !important;
    font-weight: 700 !important;
  }

  /* ── Headings ── */
  h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
  }

  /* ── Streamlit native metrics ── */
  [data-testid="stMetric"] {
    background: #1E293B !important;
    border: 1px solid rgba(51, 65, 85, 0.6) !important;
    border-radius: 14px !important;
    padding: 16px 18px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
  }

  [data-testid="stMetricValue"] {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
  }

  [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #94A3B8 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* ── Dividers ── */
  hr {
    border-color: #334155 !important;
  }

  /* ── Sliders ── */
  [data-testid="stSlider"] label {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
  }

  /* ── Inputs & Selects ── */
  .stSelectbox label, .stMultiSelect label, .stTextInput label,
  .stNumberInput label, .stTextArea label, .stDateInput label,
  .stCheckbox label, .stRadio label {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
  }

  div[data-baseweb="select"] > div {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
  }

  /* ── Tables & DataFrames ── */
  .stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #334155 !important;
  }

  /* ── Download buttons ── */
  .stDownloadButton button {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    border: 1px solid #334155 !important;
    background: #1E293B !important;
    border-radius: 8px !important;
    transition: all 0.2s ease;
  }

  .stDownloadButton button:hover {
    background: #0284C7 !important;
    border-color: #38BDF8 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
  }

  /* ── Regular button ── */
  .stButton button {
    background: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
  }
  .stButton button:hover {
    border-color: #0284C7 !important;
    color: #38BDF8 !important;
  }

  /* ── Markdown text ── */
  .stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #CBD5E1;
  }

  /* ── Tab widget labels ── */
  .stTabs [data-baseweb="tab"] {
    color: #94A3B8 !important;
    font-weight: 600 !important;
  }
  .stTabs [aria-selected="true"] {
    color: #38BDF8 !important;
    border-bottom-color: #38BDF8 !important;
  }

  /* ── Plotly chart containers ── */
  .js-plotly-plot {
    border-radius: 14px !important;
    border: 1px solid rgba(51, 65, 85, 0.6) !important;
    overflow: hidden !important;
    background-color: #1E293B !important;
  }

  /* ── Scrollbars ── */
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  ::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.6);
  }
  ::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #64748b;
  }

  /* ── Hide Streamlit chrome ── */
  footer, #MainMenu, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar branding ──────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:14px 0 20px 0;border-bottom:1px solid rgba(51,65,85,0.7);margin-bottom:18px;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#0284C7 0%,#6366F1 100%);display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:1.15rem;font-weight:800;box-shadow:0 4px 12px rgba(2,132,199,0.35);">
      ⚡
    </div>
    <div>
      <div style="color:#FFFFFF;font-size:1.25rem;font-weight:800;letter-spacing:-0.02em;line-height:1.1;">
        PulseGrid - Retail
      </div>
      <div style="color:#38BDF8;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">
        Analytics Platform
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    '<div style="color:#64748B;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;margin-bottom:10px;">Executive Modules</div>',
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    label="Navigation",
    options=[
        "Executive Sales Summary",
        "Regional Logistics & Supply Chain",
        "Customer Intelligence",
        "Demand Forecasting",
        "Inventory Optimization",
    ],
    index=0,
    label_visibility="collapsed",
)

st.sidebar.markdown("""
<div style="margin-top:36px;padding-top:18px;border-top:1px solid rgba(51,65,85,0.7);">
  <div style="color:#64748B;font-size:0.7rem;line-height:1.8;">
    <div style="color:#94A3B8;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:6px;">Data Infrastructure</div>
    Online Retail II & Live Enriched<br>
    <span style="color:#38BDF8;font-weight:600;">PulseGrid - Retail Engine Core</span><br><br>
    <div style="color:#94A3B8;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:6px;">Transaction Coverage</div>
    Dec 2009 – Dec 2011<br>
    <span style="color:#E2E8F0;">1,033,034 global transactions</span><br>
    <span style="color:#E2E8F0;">3,806 enriched logistics records</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────────
if page == "Executive Sales Summary":
    from views import sales;               sales.render()
elif page == "Regional Logistics & Supply Chain":
    from views import regional_logistics; regional_logistics.render()
elif page == "Customer Intelligence":
    from views import customers;           customers.render()
elif page == "Demand Forecasting":
    from views import forecast;            forecast.render()
elif page == "Inventory Optimization":
    from views import inventory;           inventory.render()
