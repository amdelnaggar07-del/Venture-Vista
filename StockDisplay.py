# MarketVista.py
# A polished, multi-page market overview and comparison dashboard for business enthusiasts.
# Run with:  streamlit run StockDisplay.py

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="MarketVista",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# CUSTOM THEME-AWARE CSS
# ==========================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* ---- Navigation ---- */
        .nav-container {
            background: linear-gradient(90deg, 
                color-mix(in srgb, var(--primary-color) 8%, var(--secondary-background-color)) 0%,
                var(--secondary-background-color) 50%,
                color-mix(in srgb, var(--primary-color) 5%, var(--secondary-background-color)) 100%);
            padding: 16px 24px;
            border-radius: 14px;
            margin-bottom: 28px;
            border: 1.5px solid color-mix(in srgb, var(--primary-color) 25%, transparent);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(10px);
        }

        .nav-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--text-color);
            opacity: 0.55;
            margin-bottom: 10px;
            display: block;
        }

        .nav-buttons {
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
        }

        div[data-testid="stHorizontalBlock"] .stRadio > div {
            display: flex !important;
            gap: 8px !important;
            justify-content: center !important;
        }

        div[data-testid="stHorizontalBlock"] .stRadio > div > label > div:first-child {
            width: 18px !important;
            height: 18px !important;
            border: 2px solid color-mix(in srgb, var(--primary-color) 60%, transparent) !important;
            border-radius: 50% !important;
            background: transparent !important;
            position: relative;
        }

        div[data-testid="stHorizontalBlock"] .stRadio > div > label > div:first-child::after {
            content: '' !important;
            position: absolute;
            width: 8px;
            height: 8px;
            background: var(--primary-color);
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            opacity: 0;
            transition: opacity 0.2s ease;
        }

        div[data-testid="stHorizontalBlock"] .stRadio label {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: color-mix(in srgb, var(--text-color) 2%, transparent);
            border: 1.5px solid color-mix(in srgb, var(--primary-color) 15%, transparent);
            border-radius: 8px;
            padding: 10px 20px !important;
            font-weight: 600;
            font-size: 0.9rem;
            letter-spacing: 0.3px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-color);
            margin: 0 !important;
        }

        div[data-testid="stHorizontalBlock"] .stRadio label:hover {
            background: color-mix(in srgb, var(--primary-color) 8%, transparent);
            border-color: color-mix(in srgb, var(--primary-color) 35%, transparent);
            transform: translateY(-1px);
        }

        div[data-testid="stHorizontalBlock"] .stRadio label[aria-checked="true"] {
            background: color-mix(in srgb, var(--primary-color) 10%, var(--secondary-background-color));
            color: var(--primary-color);
            border-color: var(--primary-color);
            font-weight: 700;
            box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--primary-color) 20%, transparent);
        }

        div[data-testid="stHorizontalBlock"] .stRadio label[aria-checked="true"] > div:first-child {
            border-color: var(--primary-color) !important;
        }

        div[data-testid="stHorizontalBlock"] .stRadio label[aria-checked="true"] > div:first-child::after {
            opacity: 1 !important;
        }

        div[data-testid="stHorizontalBlock"] .stRadio label[aria-checked="true"]:hover {
            transform: translateY(-2px);
            box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--primary-color) 20%, transparent), 0 4px 12px color-mix(in srgb, var(--primary-color) 20%, transparent);
        }

        /* ---- Hero Card ---- */
        .hero-card {
            background: linear-gradient(135deg,
                color-mix(in srgb, var(--primary-color) 12%, var(--background-color)) 0%,
                color-mix(in srgb, var(--primary-color) 4%, var(--background-color)) 100%);
            border: 1px solid color-mix(in srgb, var(--primary-color) 20%, var(--secondary-background-color));
            border-radius: 18px;
            padding: 28px 32px;
            margin-bottom: 12px;
        }

        .hero-logo {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            background: var(--primary-color);
            color: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            box-shadow: 0 4px 14px color-mix(in srgb, var(--primary-color) 30%, transparent);
        }

        .hero-title {
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.6px;
            line-height: 1.15;
            color: var(--text-color);
            margin: 0;
        }

        .hero-subtitle {
            font-size: 0.95rem;
            font-weight: 400;
            color: var(--text-color);
            opacity: 0.65;
            margin-top: 4px;
        }

        .badge {
            display: inline-block;
            background: color-mix(in srgb, var(--primary-color) 14%, transparent);
            border: 1.5px solid color-mix(in srgb, var(--primary-color) 30%, transparent);
            color: var(--text-color);
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 6px;
            margin-top: 6px;
            letter-spacing: 0.2px;
        }

        .badge-outline {
            display: inline-block;
            border: 1.5px solid color-mix(in srgb, var(--text-color) 15%, transparent);
            color: var(--text-color);
            opacity: 0.7;
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 500;
            margin-right: 6px;
            margin-top: 6px;
        }

        /* ---- Section Title ---- */
        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: -0.3px;
            color: var(--text-color);
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .section-caption {
            font-size: 0.82rem;
            color: var(--text-color);
            opacity: 0.55;
            margin-bottom: 14px;
        }

        /* ---- Quick-Facts Tiles ---- */
        .fact-tile {
            background: var(--secondary-background-color);
            border: 1px solid color-mix(in srgb, var(--text-color) 8%, transparent);
            border-radius: 14px;
            padding: 24px 20px;
            transition: border-color 0.2s ease;
            height: 100%;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .fact-tile:hover {
            border-color: color-mix(in srgb, var(--primary-color) 25%, transparent);
        }

        .fact-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
            display: block;
        }

        .fact-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-color);
            opacity: 0.5;
            margin-bottom: 6px;
        }

        .fact-value {
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--text-color);
            line-height: 1.2;
            margin-bottom: 8px;
        }

        .fact-detail {
            font-size: 0.82rem;
            color: var(--text-color);
            opacity: 0.6;
            line-height: 1.4;
        }

        /* ---- Key-Value pair (At a Glance) ---- */
        .kv-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 9px 0;
            border-bottom: 1px solid color-mix(in srgb, var(--text-color) 6%, transparent);
        }

        .kv-row:last-child { border-bottom: none; }

        .kv-key {
            font-size: 0.78rem;
            font-weight: 500;
            color: var(--text-color);
            opacity: 0.5;
        }

        .kv-val {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-color);
            text-align: right;
            max-width: 60%;
        }

        /* ---- Price tag ---- */
        .price-tag {
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: var(--text-color);
        }

        .price-change-up {
            color: #22c55e;
            font-weight: 700;
            font-size: 0.95rem;
        }

        .price-change-down {
            color: #ef4444;
            font-weight: 700;
            font-size: 0.95rem;
        }

        /* ---- Peer Pills ---- */
        div[data-testid="stHorizontalBlock"] > div .stButton > button[kind="primary"] {
            border-radius: 999px !important;
            font-weight: 600 !important;
            font-size: 0.82rem !important;
            padding: 4px 16px !important;
        }

        div[data-testid="stHorizontalBlock"] > div .stButton > button[kind="secondary"] {
            border-radius: 999px !important;
            font-weight: 500 !important;
            font-size: 0.82rem !important;
            padding: 4px 16px !important;
        }

        /* ---- Chart container polish ---- */
        .stPlotlyChart {
            border-radius: 12px;
            overflow: hidden;
        }

        /* ---- Tooltip Icon ---- */
        .info-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            background: var(--primary-color);
            border-radius: 50%;
            font-size: 12px;
            font-weight: 900;
            color: #ffffff;
            cursor: help;
            margin-left: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .info-icon:hover {
            transform: scale(1.15);
        }

        /* ---- Exec Card ---- */
        .exec-card {
            background: var(--secondary-background-color);
            border: 1px solid color-mix(in srgb, var(--text-color) 8%, transparent);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            height: 100%;
            transition: transform 0.2s;
        }
        .exec-card:hover {
            transform: translateY(-4px);
            border-color: var(--primary-color);
        }
        .exec-name {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 2px;
        }
        .exec-title {
            font-size: 0.78rem;
            opacity: 0.6;
            margin-bottom: 10px;
            line-height: 1.2;
            min-height: 2.4em;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .exec-pay {
            font-weight: 700;
            font-size: 0.9rem;
            color: var(--primary-color);
        }
        
        /* ---- Hierarchy Connector ---- */
        .hierarchy-line {
            width: 2px;
            height: 20px;
            background: color-mix(in srgb, var(--text-color) 15%, transparent);
            margin: 0 auto;
        }

        /* ---- Dividers ---- */
        hr {
            border-color: color-mix(in srgb, var(--text-color) 8%, transparent);
            margin: 6px 0 18px 0;
        }
        
        /* ---- Comparison Controls ---- */
        .comp-tag {
            display: inline-flex;
            align-items: center;
            background: color-mix(in srgb, var(--primary-color) 10%, var(--secondary-background-color));
            border: 1px solid var(--primary-color);
            border-radius: 8px;
            padding: 4px 12px;
            margin: 4px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .app-hero {
            background: linear-gradient(135deg,
                color-mix(in srgb, var(--primary-color) 18%, var(--background-color)) 0%,
                var(--secondary-background-color) 100%);
            border: 1px solid color-mix(in srgb, var(--primary-color) 25%, transparent);
            border-radius: 20px;
            padding: 28px 28px 22px;
            margin-bottom: 24px;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.12);
        }

        .app-title {
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 8px;
        }

        .app-subtitle {
            font-size: 1.05rem;
            color: var(--text-color);
            opacity: 0.75;
            margin-bottom: 22px;
        }

        .feature-grid {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
        }

        .feature-card {
            background: var(--background-color);
            border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
            border-radius: 16px;
            padding: 18px;
            flex: 1;
            min-width: 220px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
        }

        .feature-card-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-color);
        }

        .feature-card-desc {
            font-size: 0.92rem;
            opacity: 0.78;
            line-height: 1.6;
        }

        .section-text {
            background: var(--secondary-background-color);
            border: 1px solid color-mix(in srgb, var(--primary-color) 15%, transparent);
            border-radius: 18px;
            padding: 24px;
            color: var(--text-color);
        }

        .section-text ul,
        .section-text ol {
            margin: 12px 0 16px 1.4rem;
            color: var(--text-color);
            opacity: 0.9;
        }

        .section-text li {
            margin-bottom: 0.65rem;
        }

        .section-text strong {
            color: var(--text-color);
        }

        .section-text em {
            font-style: italic;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# FORMATTING HELPERS
# ==========================================================

def money(v):
    if v is None:
        return "—"
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "—"
    if abs(v) >= 1e12:
        return f"${v/1e12:.2f}T"
    if abs(v) >= 1e9:
        return f"${v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:.2f}M"
    return f"${v:,.0f}"


def pct(v):
    if v is None:
        return "—"
    try:
        return f"{v*100:.2f}%"
    except (TypeError, ValueError):
        return "—"


def ratio(v):
    if v is None:
        return "—"
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return "—"


def big_number(v):
    if v is None:
        return "—"
    try:
        return f"{int(v):,}"
    except (TypeError, ValueError):
        return "—"


# ==========================================================
# SEARCH & FILTERING
# ==========================================================

_FALLBACK = {
    "APPLE": "AAPL", "MICROSOFT": "MSFT", "ALPHABET": "GOOGL",
    "GOOGLE": "GOOGL", "AMAZON": "AMZN", "TESLA": "TSLA",
    "META": "META", "NVIDIA": "NVDA", "NETFLIX": "NFLX", "WALMART": "WMT",
}

CREATIVE_COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
    "#F7DC6F", "#BB8FCE", "#82E0AA", "#F1948A", "#85C1E9",
    "#73C6B6", "#F8C471", "#C39BD3", "#7DCEA0", "#F1948A"
]

INDICATOR_DESCRIPTIONS = {
    "Revenue": "The total amount of income generated by the sale of goods or services related to the company's primary operations.",
    "Net Income": "The total profit of a company after all expenses, including taxes and interest, have been deducted from total revenue.",
    "Gross Profit": "The profit a company makes after deducting the costs associated with making and selling its products or providing its services.",
    "Operating Income": "The amount of profit realized from a business's operations after deducting operating expenses such as wages, depreciation, and cost of goods sold.",
    "EBITDA": "Earnings Before Interest, Taxes, Depreciation, and Amortization; a measure of a company's overall financial performance.",
    "Total Assets": "The total value of everything a company owns, including cash, inventory, property, and equipment.",
    "Free Cash Flow": "The cash a company produces through its operations, less the cost of expenditures on assets.",
    "CapEx": "Capital Expenditure; the money a company spends to buy, maintain, or improve its fixed assets.",
    "Total Liabilities": "The total value of a company's debts and financial obligations.",
    "Stockholders Equity": "The remaining value of assets after all liabilities have been paid; the 'book value' of the company.",
    "Research & Development": "The amount spent on developing new products or improving existing ones.",
    "Operating Cash Flow": "The cash generated by a company's normal business operations.",
    "Long Term Debt": "The portion of a company's debt that is due in more than one year.",
    "Net Borrowings": "The net amount of debt the company has taken on or paid off during the period.",
}

@st.cache_data(ttl=1800)
def search_companies(query, max_results=8):
    if not query or not query.strip():
        return pd.DataFrame(columns=["Ticker", "Company", "Exchange"])

    rows = []
    try:
        if hasattr(yf, "Search"):
            result = yf.Search(query.strip(), max_results=max_results)
            quotes = getattr(result, "quotes", []) or []
            for q in quotes:
                if q.get("quoteType") not in ["EQUITY", "COMMONSTOCK"]:
                    continue
                rows.append({
                    "Ticker": q.get("symbol"),
                    "Company": q.get("longname") or q.get("shortname") or q.get("symbol"),
                    "Exchange": q.get("exchange", "—"),
                })
    except Exception:
        pass

    if not rows:
        q = query.strip().upper()
        for name, sym in _FALLBACK.items():
            if q in name or q == sym:
                rows.append({"Ticker": sym, "Company": name.title(), "Exchange": "—"})

    return pd.DataFrame(rows).drop_duplicates(subset="Ticker").reset_index(drop=True)


@st.cache_data(ttl=3600)
def get_industry_peers(industry, sector, exclude_symbol, limit=8):
    if not industry or industry == "—":
        return []
    peers = []
    
    queries = [industry, f"{industry} stocks", f"{sector} stocks"]
    
    for q in queries:
        if not q or q == "—": continue
        try:
            search = yf.Search(q, max_results=25)
            quotes = getattr(search, "quotes", []) or []
            for quote in quotes:
                sym = quote.get("symbol")
                if not sym or sym == exclude_symbol: continue
                if quote.get("quoteType") not in ["EQUITY", "COMMONSTOCK"]: continue
                
                name = quote.get("longname") or quote.get("shortname") or sym
                if not any(p['Ticker'] == sym for p in peers):
                    peers.append({"Ticker": sym, "Company": name})
                
                if len(peers) >= limit:
                    return peers
        except Exception:
            pass
            
    if len(peers) < 3:
        fallbacks = {
            "Technology": ["MSFT", "GOOGL", "AMZN", "META", "NVDA", "ORCL", "CRM"],
            "Consumer Cyclical": ["AMZN", "TSLA", "HD", "NKE", "MCD", "SBUX", "F"],
            "Financial Services": ["JPM", "BAC", "WFC", "C", "GS", "MS", "AXP"],
            "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "LLY", "MRK", "TMO"],
            "Communication Services": ["GOOGL", "META", "DIS", "NFLX", "VZ", "T", "CMCSA"],
            "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX"],
            "Industrials": ["HON", "UPS", "GE", "UNP", "CAT", "RTX", "LMT"],
            "Consumer Defensive": ["WMT", "PG", "KO", "PEP", "COST", "PM", "EL"],
            "Utilities": ["NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE"],
            "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "DLR", "PSA", "WY"],
            "Basic Materials": ["LIN", "APD", "SHW", "FCX", "NEM", "CTVA", "DOW"]
        }
        
        sector_peers = fallbacks.get(sector, [])
        for sym in sector_peers:
            if sym == exclude_symbol: continue
            if not any(p['Ticker'] == sym for p in peers):
                try:
                    t = yf.Ticker(sym)
                    name = t.info.get("longName") or sym
                    peers.append({"Ticker": sym, "Company": name})
                except:
                    pass
            if len(peers) >= 3:
                break
                
    return peers


# ==========================================================
# DATA ACCESS
# ==========================================================

@st.cache_data(ttl=3600)
def get_company_info(symbol):
    try:
        return yf.Ticker(symbol).info or {}
    except Exception:
        return {}


@st.cache_data(ttl=3600)
def get_annual_financials(symbol):
    ticker = yf.Ticker(symbol)
    
    def safe(getter):
        try:
            df = getter()
            return df if df is not None else pd.DataFrame()
        except Exception:
            return pd.DataFrame()

    fin = safe(lambda: ticker.financials)
    bs = safe(lambda: ticker.balance_sheet)
    cf = safe(lambda: ticker.cashflow)

    def pick(df, keys):
        if df is None or df.empty:
            return None
        for k in keys:
            if k in df.index:
                return df.loc[k]
        return None

    fields = {
        "Revenue": pick(fin, ["Total Revenue", "TotalRevenue"]),
        "Net Income": pick(fin, ["Net Income", "NetIncome", "Net Income Common Stockholders"]),
        "Gross Profit": pick(fin, ["Gross Profit", "GrossProfit"]),
        "Operating Income": pick(fin, ["Operating Income", "OperatingIncome"]),
        "EBITDA": pick(fin, ["EBITDA", "Normalized EBITDA"]),
        "Total Assets": pick(bs, ["Total Assets", "TotalAssets"]),
        "Free Cash Flow": pick(cf, ["Free Cash Flow", "FreeCashFlow"]),
        "CapEx": pick(cf, ["Capital Expenditure", "CapitalExpenditure"]),
        "Total Liabilities": pick(bs, ["Total Liabilities Net Minority Interest", "TotalLiabilities"]),
        "Stockholders Equity": pick(bs, ["Total Equity Gross Minority Interest", "StockholdersEquity"]),
        "Research & Development": pick(fin, ["Research And Development", "ResearchDevelopment"]),
        "Operating Cash Flow": pick(cf, ["Operating Cash Flow", "OperatingCashFlow"]),
        "Long Term Debt": pick(bs, ["Long Term Debt", "LongTermDebt"]),
        "Net Borrowings": pick(cf, ["Net Borrowings", "NetBorrowings"]),
    }

    data = {k: v for k, v in fields.items() if v is not None}
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df = df.sort_index()
    df.index = pd.to_datetime(df.index)
    df = df[~df.index.duplicated(keep="last")]
    return df


# ==========================================================
# PLOTLY CHART BUILDERS
# ==========================================================

def plotly_theme():
    return dict(
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#9ca3af"),
        margin=dict(l=10, r=10, t=40, b=30),
        hoverlabel=dict(
            bgcolor="rgba(30,30,30,0.95)",
            font=dict(family="Inter, sans-serif", size=13, color="#fff"),
            bordercolor="rgba(255,255,255,0.1)",
        ),
    )


def make_dynamic_chart(series, title, chart_type="bar", color="#6366f1"):
    s = series.dropna()
    if s.empty:
        return None

    df = s.reset_index()
    df.columns = ["Period", "Value"]
    
    if pd.api.types.is_datetime64_any_dtype(df["Period"]):
        df["Period_Str"] = df["Period"].dt.strftime('%Y')
    else:
        df["Period_Str"] = df["Period"].astype(str)

    fig = go.Figure()

    if chart_type == "bar":
        fig.add_trace(go.Bar(
            x=df["Period_Str"],
            y=df["Value"],
            marker_color=color,
            width=0.4,
            text=[money(v) for v in df["Value"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Value: %{text}<extra></extra>",
        ))
    elif chart_type == "area":
        fig.add_trace(go.Scatter(
            x=df["Period_Str"],
            y=df["Value"],
            mode="lines+markers+text",
            fill="tozeroy",
            fillcolor=f"rgba{tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}",
            line=dict(color=color, width=3),
            marker=dict(size=8, symbol="circle"),
            text=[money(v) for v in df["Value"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>Value: %{text}<extra></extra>",
        ))
    elif chart_type == "line":
        fig.add_trace(go.Scatter(
            x=df["Period_Str"],
            y=df["Value"],
            mode="lines+markers+text",
            line=dict(color=color, width=3),
            marker=dict(size=8, symbol="circle"),
            text=[money(v) for v in df["Value"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>Value: %{text}<extra></extra>",
        ))
    elif chart_type == "scatter":
        fig.add_trace(go.Scatter(
            x=df["Period_Str"],
            y=df["Value"],
            mode="markers+text",
            marker=dict(size=14, color=color, symbol="diamond"),
            text=[money(v) for v in df["Value"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>Value: %{text}<extra></extra>",
        ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=14, color="#e5e7eb"), x=0),
        height=320,
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        **plotly_theme(),
    )
    return fig


# ==========================================================
# QUICK-FACTS BUILDER
# ==========================================================

def build_fun_facts(info, annual):
    facts = []

    pe = info.get("trailingPE")
    fwd_pe = info.get("forwardPE")
    val_detail = ""
    if pe and fwd_pe:
        val_detail = f"Trading at {pe:.1f}x trailing earnings, {fwd_pe:.1f}x forward"
    elif pe:
        val_detail = f"P/E ratio of {pe:.1f}x"
    
    mcap = info.get("marketCap")
    if mcap:
        facts.append({
            "icon": "💰",
            "label": "Valuation Context",
            "value": money(mcap),
            "detail": val_detail or f"Market capitalisation of {money(mcap)}",
        })

    rev = info.get("totalRevenue")
    rev_growth = info.get("revenueGrowth")
    if rev_growth is not None:
        direction = "growing" if rev_growth > 0 else "declining"
        facts.append({
            "icon": "📊",
            "label": "Growth Rate",
            "value": pct(rev_growth),
            "detail": f"Revenue {direction} {abs(rev_growth)*100:.1f}% YoY",
        })

    margins = info.get("profitMargins")
    if margins is not None:
        ebitda_m = info.get("ebitdaMargins")
        detail = f"EBITDA margin {ebitda_m*100:.1f}%" if ebitda_m else ""
        facts.append({
            "icon": "📈",
            "label": "Profitability",
            "value": pct(margins),
            "detail": detail or f"Net profit margin of {pct(margins)}",
        })

    employees = info.get("fullTimeEmployees")
    if employees and rev:
        rpe = rev / employees
        facts.append({
            "icon": "👥",
            "label": "Efficiency",
            "value": money(rpe),
            "detail": f"~{money(rpe)} revenue per employee",
        })

    beta = info.get("beta")
    if beta:
        if beta > 1.3:
            desc, detail = "High Volatility", f"Beta of {beta:.2f} — significantly more volatile than the S&P 500"
        elif beta > 1.05:
            desc, detail = "Above-Avg Risk", f"Beta of {beta:.2f} — moderately more volatile than the market"
        elif beta < 0.8:
            desc, detail = "Defensive", f"Beta of {beta:.2f} — less volatile, tends to hold value in downturns"
        else:
            desc, detail = "Market-Correlated", f"Beta of {beta:.2f} — moves roughly in line with the market"
        facts.append({"icon": "🛡️", "label": "Risk Profile", "value": desc, "detail": detail})

    div_yield = info.get("dividendYield")
    payout = info.get("payoutRatio")
    if div_yield:
        facts.append({
            "icon": "💵",
            "label": "Dividend Yield",
            "value": pct(div_yield),
            "detail": f"Payout ratio of {payout*100:.1f}%" if payout else f"Current yield of {pct(div_yield)}",
        })

    earnings_growth = info.get("earningsGrowth")
    if earnings_growth is not None:
        direction = "📗" if earnings_growth > 0 else "📕"
        facts.append({
            "icon": "🚀",
            "label": "Earnings Growth",
            "value": f"{earnings_growth*100:.1f}%",
            "detail": f"Year-over-year earnings {direction}",
        })

    roe = info.get("returnOnEquity")
    if roe:
        roa = info.get("returnOnAssets")
        detail = f"ROA of {roa*100:.1f}%" if roa else ""
        facts.append({
            "icon": "🏆",
            "label": "Return on Equity",
            "value": pct(roe),
            "detail": detail or f"ROE of {pct(roe)} — how efficiently shareholder capital is used",
        })

    debt_to_eq = info.get("debtToEquity")
    if debt_to_eq:
        try:
            dte = float(debt_to_eq)
            health = "Highly Leveraged" if dte > 200 else ("Moderate Debt" if dte > 100 else "Low Leverage")
            facts.append({
                "icon": "⚖️",
                "label": "Debt Position",
                "value": health,
                "detail": f"Debt-to-equity ratio of {dte:.1f}%",
            })
        except: pass

    fcf = info.get("freeCashflow")
    if fcf:
        facts.append({
            "icon": "💨",
            "label": "Free Cash Flow",
            "value": money(fcf),
            "detail": f"Cash produced after capital expenditures",
        })

    inst_pct = info.get("heldPercentInstitutions")
    if inst_pct:
        facts.append({
            "icon": "🏛️",
            "label": "Institutional Hold",
            "value": pct(inst_pct),
            "detail": f"{pct(inst_pct)} held by institutional investors",
        })

    rec_mean = info.get("recommendationMean")
    rec_key = info.get("recommendationKey")
    if rec_mean and rec_key:
        rec_labels = {1: "Strong Buy", 2: "Buy", 3: "Hold", 4: "Sell", 5: "Strong Sell"}
        rec_text = rec_labels.get(int(rec_mean), rec_key.replace("-", " ").title())
        facts.append({
            "icon": "🎯",
            "label": "Analyst Consensus",
            "value": rec_text,
            "detail": f"Mean recommendation: {rec_mean:.2f}",
        })

    return facts


# ==========================================================
# PAGE: OVERVIEW
# ==========================================================

def page_overview():
    symbol = st.session_state.symbol
    info = get_company_info(symbol)

    if not info:
        st.error("Could not load data for this company. Try another search.")
        return

    company_name = info.get("longName") or info.get("shortName") or symbol
    sector = info.get("sector") or "—"
    industry = info.get("industry") or "—"
    hq = ", ".join(filter(None, [info.get("city"), info.get("state"), info.get("country")])) or "—"
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    price_change = info.get("regularMarketChange") or 0
    price_change_pct = info.get("regularMarketChangePercent") or 0

    hero_html = f"""<div class="hero-card">
<div style="display:flex;align-items:center;gap:18px;">
<div class="hero-logo">{company_name.strip()[0].upper() if company_name.strip() else "?"}</div>
<div style="flex:1;">
<div class="hero-title">{company_name}</div>
<div class="hero-subtitle">{hq} &nbsp;·&nbsp; {info.get('exchange','—')} &nbsp;·&nbsp; {info.get('currency','USD')}</div>
<div style="margin-top:8px;">
<span class="badge">{symbol}</span>
<span class="badge">{sector}</span>
<span class="badge">{industry}</span>
{'<span class="badge-outline">Dividend Stock</span>' if info.get('dividendYield') else ''}
{'<span class="badge-outline">Growth</span>' if (info.get('earningsGrowth', 0) or 0) > 0.1 else ''}
</div>
</div>
<div style="text-align:right;">
<div class="price-tag">${current_price:,.2f}</div>
<div class="{'price-change-up' if price_change >= 0 else 'price-change-down'}">
{'+' if price_change >= 0 else ''}{price_change:,.2f} ({price_change_pct*100:+.2f}%)
</div>
</div>
</div>
</div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    peers = get_industry_peers(industry, sector, symbol)
    peer_list = [{"Ticker": symbol, "Company": company_name}] + peers

    st.caption(f"Peers in {industry}")
    pill_cols = st.columns(min(len(peer_list), 4))
    for i, p in enumerate(peer_list[:8]):
        col_idx = i % 4
        with pill_cols[col_idx]:
            tck = p["Ticker"]
            name = p["Company"]
            st.button(
                name,
                key=f"pill_{tck}_{i}",
                type="primary" if tck == symbol else "secondary",
                use_container_width=True,
                on_click=lambda t=tck: setattr(st.session_state, 'symbol', t)
            )

    st.write("")

    st.markdown('<div class="section-title">Key Financial Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Snapshot of the company\'s financial health</div>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5, gap="medium")
    with m1: st.metric("Market Cap", money(info.get("marketCap")))
    with m2: st.metric("Revenue (TTM)", money(info.get("totalRevenue")))
    with m3: st.metric("Net Income (TTM)", money(info.get("netIncomeToCommon")))
    with m4: st.metric("Profit Margin", pct(info.get("profitMargins")))
    with m5: st.metric("P/E Ratio", ratio(info.get("trailingPE")))

    st.write("")

    left, right = st.columns([3, 2], gap="large")

    with left:
        summary = info.get("longBusinessSummary") or "No description available."
        short_summary = summary
        if len(summary) > 400:
            short_summary = summary[:400].rsplit(" ", 1)[0] + "…"

        st.markdown('<div class="section-title">About the Business</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">What this company does and how it makes money</div>', unsafe_allow_html=True)

        st.write(short_summary)
        if len(summary) > 400:
            with st.expander("Read full overview"):
                st.write(summary)

    with right:
        st.markdown('<div class="section-title">At a Glance</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Key identifiers and fundamentals</div>', unsafe_allow_html=True)

        glance_items = [
            ("Headquarters", hq),
            ("Sector", sector),
            ("Industry", industry),
            ("Exchange", info.get("exchange", "—")),
            ("Currency", info.get("currency", "USD")),
            ("Employees", big_number(info.get("fullTimeEmployees"))),
            ("Fiscal Year End", info.get("fiscalYearEnd") or "—"),
            ("Website", info.get("website") or "—"),
        ]

        for key, val in glance_items:
            st.markdown(
                f'<div class="kv-row"><span class="kv-key">{key}</span><span class="kv-val">{val}</span></div>',
                unsafe_allow_html=True,
            )

    st.write("")

    annual = get_annual_financials(symbol)

    st.markdown('<div class="section-title">Financial Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Build your own charts to visualize annual trends</div>', unsafe_allow_html=True)

    if not annual.empty:
        if "chart_list" not in st.session_state:
            st.session_state.chart_list = [
                {"indicator": "Revenue", "type": "Bar"},
                {"indicator": "Net Income", "type": "Bar"}
            ]

        with st.expander("➕ Add / Modify Charts", expanded=True):
            cb1, cb2, cb3 = st.columns([2, 2, 1])
            with cb1:
                new_indicator = st.selectbox("Select Indicator", options=list(INDICATOR_DESCRIPTIONS.keys()))
            with cb2:
                new_type = st.selectbox("Select Chart Type", options=["Bar", "Area", "Line", "Scatter"])
            with cb3:
                st.write("")
                if st.button("Add Chart", use_container_width=True, type="primary"):
                    st.session_state.chart_list.append({"indicator": new_indicator, "type": new_type})
                    st.rerun()

        if st.session_state.chart_list:
            for i in range(0, len(st.session_state.chart_list), 2):
                c1, c2 = st.columns(2, gap="medium")
                for j, col in enumerate([c1, c2]):
                    idx = i + j
                    if idx < len(st.session_state.chart_list):
                        chart_config = st.session_state.chart_list[idx]
                        ind = chart_config["indicator"]
                        ctype = chart_config["type"]
                        if ind in annual.columns:
                            with col:
                                definition = INDICATOR_DESCRIPTIONS.get(ind, "")
                                header_col1, header_col2 = st.columns([0.9, 0.1])
                                with header_col1:
                                    st.markdown(
                                        f'<div class="section-title">{ind} <span class="info-icon" title="{definition}">?</span></div>',
                                        unsafe_allow_html=True
                                    )
                                with header_col2:
                                    if st.button("🗑️", key=f"del_{idx}"):
                                        st.session_state.chart_list.pop(idx)
                                        st.rerun()
                                fig = make_dynamic_chart(annual[ind], "", chart_type=ctype.lower(), color=CREATIVE_COLORS[idx % len(CREATIVE_COLORS)])
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No charts added yet. Use the builder above to add some!")
    else:
        st.info("Annual financial data unavailable for this company.")

    st.write("")

    st.markdown('<div class="section-title">Business Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Deep-dive facts for business enthusiasts</div>', unsafe_allow_html=True)

    facts = build_fun_facts(info, annual)
    if facts:
        cols_per_row = 3
        for i in range(0, len(facts), cols_per_row):
            row_facts = facts[i : i + cols_per_row]
            cols = st.columns(cols_per_row, gap="medium")
            for j, fact in enumerate(row_facts):
                with cols[j]:
                    st.markdown(
                        f"""<div class="fact-tile">
<span class="fact-icon">{fact['icon']}</span>
<div class="fact-label">{fact['label']}</div>
<div class="fact-value">{fact['value']}</div>
<div class="fact-detail">{fact['detail']}</div>
</div>""",
                        unsafe_allow_html=True,
                    )

    st.write("")

    st.markdown('<div class="section-title">Executive Leadership</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Organizational hierarchy and compensation</div>', unsafe_allow_html=True)

    officers = info.get("companyOfficers", [])
    if officers:
        ceo = next((o for o in officers if "CEO" in o.get("title", "").upper() or "CHIEF EXECUTIVE" in o.get("title", "").upper()), officers[0])
        others = [o for o in officers if o != ceo]
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        c_top1, c_top2, c_top3 = st.columns([1, 1.2, 1])
        with c_top2:
            st.markdown(
                f"""<div class="exec-card" style="border: 2px solid var(--primary-color);">
<div class="exec-name" style="font-size:1.15rem;">{ceo.get('name', 'N/A')}</div>
<div class="exec-title" style="color:var(--primary-color); font-weight:600;">{ceo.get('title', 'CEO')}</div>
<div class="exec-pay">{money(ceo.get('totalPay')) if ceo.get('totalPay') else "Pay not disclosed"}</div>
</div>""",
                unsafe_allow_html=True
            )
        st.markdown('<div class="hierarchy-line"></div>', unsafe_allow_html=True)
        if others:
            cols_exec = st.columns(min(len(others), 4), gap="small")
            for i, officer in enumerate(others[:8]):
                with cols_exec[i % len(cols_exec)]:
                    name = officer.get("name", "N/A")
                    title = officer.get("title", "Executive")
                    pay = money(officer.get("totalPay"))
                    st.markdown(
                        f"""<div class="exec-card">
<div class="exec-name">{name}</div>
<div class="exec-title">{title}</div>
<div class="exec-pay">{pay if pay != "—" else "Pay not disclosed"}</div>
</div>""",
                        unsafe_allow_html=True
                    )
    else:
        st.info("Executive data not available.")


# ==========================================================
# PAGE: COMPARISON
# ==========================================================

def page_comparison():
    st.markdown('<div class="section-title">Company Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Compare key metrics across multiple companies in an industry (Max 5)</div>', unsafe_allow_html=True)

    if "comp_symbols" not in st.session_state:
        st.session_state.comp_symbols = ["AMZN", "MSFT", "GOOGL"]

    # --- CONTROLS ---
    with st.expander("⚙️ Manage Comparison List", expanded=True):
        col_ctrl1, col_ctrl2 = st.columns([3, 1])
        with col_ctrl1:
            if len(st.session_state.comp_symbols) < 5:
                new_comp_query = st.text_input("Add Company to Compare", placeholder="Enter ticker or name...")
                if new_comp_query:
                    results = search_companies(new_comp_query, max_results=5)
                    if not results.empty:
                        for row in results.itertuples():
                            if st.button(f"Add {row.Company} ({row.Ticker})", key=f"add_{row.Ticker}"):
                                if row.Ticker not in st.session_state.comp_symbols:
                                    st.session_state.comp_symbols.append(row.Ticker)
                                    st.rerun()
            else:
                st.warning("Maximum of 5 companies reached. Remove one to add another.")
        with col_ctrl2:
            st.write("Current List:")
            for sym in st.session_state.comp_symbols:
                st.markdown(f"""<div class="comp-tag">{sym}</div>""", unsafe_allow_html=True)
                if st.button(f"Remove {sym}", key=f"rem_{sym}"):
                    st.session_state.comp_symbols.remove(sym)
                    st.rerun()
        
        # --- PEER SUGGESTIONS ---
        if st.session_state.comp_symbols and len(st.session_state.comp_symbols) < 5:
            st.write("Suggested Peers:")
            last_sym = st.session_state.comp_symbols[-1]
            last_info = get_company_info(last_sym)
            if last_info:
                industry = last_info.get("industry")
                sector = last_info.get("sector")
                suggested_peers = get_industry_peers(industry, sector, last_sym, limit=6)
                
                final_suggestions = [p for p in suggested_peers if p["Ticker"] not in st.session_state.comp_symbols]
                
                if final_suggestions:
                    s_cols = st.columns(min(len(final_suggestions), 4))
                    for idx, peer in enumerate(final_suggestions[:4]):
                        with s_cols[idx]:
                            if st.button(peer["Company"], key=f"s_peer_{peer['Ticker']}", use_container_width=True):
                                st.session_state.comp_symbols.append(peer["Ticker"])
                                st.rerun()
                else:
                    st.caption("No additional peers found.")

    if len(st.session_state.comp_symbols) < 2:
        st.info("Add at least two companies to begin comparison.")
        return

    # --- DATA FETCHING ---
    with st.spinner("Fetching comparison data..."):
        comparison_data = []
        for sym in st.session_state.comp_symbols:
            info = get_company_info(sym)
            if info:
                comparison_data.append({
                    "Symbol": sym,
                    "Company": info.get("shortName") or sym,
                    "Market Cap": info.get("marketCap", 0),
                    "Revenue": info.get("totalRevenue", 0),
                    "Net Income": info.get("netIncomeToCommon", 0),
                    "Profit Margin": info.get("profitMargins", 0),
                    "P/E Ratio": info.get("trailingPE", 0),
                    "ROE": info.get("returnOnEquity", 0),
                    "FCF": info.get("freeCashflow", 0)
                })
        
        if not comparison_data:
            st.error("Could not retrieve data.")
            return

        df_comp = pd.DataFrame(comparison_data)

    # --- MAIN VISUALIZATION: RADAR CHART ---
    st.write("")
    metrics = ["Market Cap", "Revenue", "Net Income", "Profit Margin", "ROE"]
    df_norm = df_comp.copy()
    for metric in metrics:
        max_val = df_norm[metric].max()
        if max_val != 0:
            df_norm[metric] = df_norm[metric] / max_val
    
    fig_radar = go.Figure()
    for i, row in df_norm.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[m] for m in metrics],
            theta=metrics,
            fill='toself',
            name=row["Company"],
            line=dict(color=CREATIVE_COLORS[i % len(CREATIVE_COLORS)])
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False), bgcolor="rgba(0,0,0,0)"),
        showlegend=True, height=500, **plotly_theme()
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # --- ADDITIONAL CHARTS ---
    st.divider()
    st.markdown('<div class="section-title">Comparative Analysis</div>', unsafe_allow_html=True)
    
    col_extra1, col_extra2 = st.columns(2)
    
    with col_extra1:
        fig_scale = px.scatter(
            df_comp, x="Revenue", y="Market Cap", size="Net Income", color="Company",
            hover_name="Company", text="Symbol", title="<b>Financial Scale: Market Cap vs Revenue</b>",
            color_discrete_sequence=CREATIVE_COLORS
        )
        fig_scale.update_traces(textposition='top center')
        fig_scale.update_layout(
            height=400,
            xaxis=dict(showgrid=False, showticklabels=True, zeroline=False, title="Revenue"),
            yaxis=dict(showgrid=False, showticklabels=True, zeroline=False, title="Market Cap"),
            legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center', yanchor='top'),
            **plotly_theme()
        )
        st.plotly_chart(fig_scale, use_container_width=True)

    with col_extra2:
        fig_eff = px.bar(
            df_comp, x="Company", y=["Profit Margin", "ROE"], barmode="group",
            title="<b>Efficiency Matrix: Margins & Returns</b>",
            color_discrete_sequence=[CREATIVE_COLORS[0], CREATIVE_COLORS[1]],
            text_auto='.2%'
        )
        fig_eff.update_traces(textposition='outside', textfont=dict(size=12, color='white'))
        fig_eff.update_layout(
            height=400,
            bargap=0.3,
            bargroupgap=0.25,
            xaxis=dict(showgrid=False, showticklabels=True, title="Company"),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, title=""),
            legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center', yanchor='top'),
            **plotly_theme()
        )
        st.plotly_chart(fig_eff, use_container_width=True)

    # --- DATA BREAKDOWN TABLE ---
    st.divider()
    st.markdown('<div class="section-title">Raw Data Breakdown</div>', unsafe_allow_html=True)
    display_df = df_comp.copy()
    display_df["Market Cap"] = display_df["Market Cap"].apply(money)
    display_df["Revenue"] = display_df["Revenue"].apply(money)
    display_df["Net Income"] = display_df["Net Income"].apply(money)
    display_df["FCF"] = display_df["FCF"].apply(money)
    display_df["Profit Margin"] = display_df["Profit Margin"].apply(pct)
    display_df["ROE"] = display_df["ROE"].apply(pct)
    st.table(display_df.drop(columns=["Symbol"]))


# ==========================================================
# MAIN APP ENTRY
# ==========================================================

st.markdown(
    """
    <div class="nav-container">
        <span class="nav-title">Navigation</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["About", "Company Overview", "Company Comparison"])

with tabs[0]:
    st.markdown(
        """<div class="app-title">🚀 Venture Vista: Discover Company Trails</div>
        <div class="app-subtitle">Explore company financials and compare market leaders</div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="section-text">
        <strong>What this app offers</strong>
        <ul>
            <li><strong>Company Overview</strong>: search for a company or ticker and view key financials, stock data, and a summary.</li>
            <li><strong>Company Comparison</strong>: compare multiple companies across revenue, market cap, profitability, and efficiency metrics.</li>
            <li>Interactive charts and raw data tables for quick insight into performance.</li>
        </ul>
        <strong>Quick user guide</strong>
        <ol>
            <li>Choose the <em>Company Overview</em> tab.</li>
            <li>Enter a company name or ticker in the search box.</li>
            <li>Select a match and click <em>View company</em> to load its profile.</li>
            <li>Switch to <em>Company Comparison</em> to compare selected firms side-by-side.</li>
            <li>Review the charts and table to inspect financial scale, efficiency, and raw metrics.</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

with tabs[1]:
    st.markdown(
        """<div class="app-title">🏢 Company Explorer</div>
        <div class="app-subtitle">Comprehensive overview for business enthusiasts</div>""",
        unsafe_allow_html=True,
    )

    if "symbol" not in st.session_state:
        st.session_state.symbol = "AMZN"

    query = st.text_input("Search company or ticker", placeholder="e.g. Apple, Tesla, NVDA, Microsoft")
    if query:
        results = search_companies(query)
        if not results.empty:
            labels = [f"{row.Company}  ({row.Ticker})  · {row.Exchange}" for row in results.itertuples()]
            picked_label = st.radio("Matches", labels, label_visibility="collapsed")
            picked_ticker = results.iloc[labels.index(picked_label)]["Ticker"]
            if st.button("View company", use_container_width=True, type="primary"):
                st.session_state.symbol = picked_ticker
                if "chart_list" in st.session_state:
                    del st.session_state.chart_list
                st.rerun()
        else:
            st.warning("No matches found.")

    st.divider()
    page_overview()

with tabs[2]:
    st.markdown(
        """<div class="app-title">📊 Company Comparison</div>
        <div class="app-subtitle">Compare industry leaders side-by-side</div>""",
        unsafe_allow_html=True,
    )
    st.divider()
    page_comparison()
