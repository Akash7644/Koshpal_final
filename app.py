import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

from pathlib import Path

from financial_ai.predictor import predict_financial_health
from financial_ai.langchain import generate_financial_report


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"

FEATURE_FILE = MODEL_DIR / "final_features.pkl"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Koshpal | Financial Health",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


# ============================================================
# LOAD MODEL FEATURES
# ============================================================

if not FEATURE_FILE.exists():
    st.error(f"Model feature file was not found:\n\n{FEATURE_FILE}")
    st.stop()

try:
    final_features = joblib.load(FEATURE_FILE)
except Exception as e:
    st.error(f"Unable to load model features: {e}")
    st.stop()


# ============================================================
# THEME TOKENS — dark "ledger" palette only
# ============================================================

BG = "#0B0E14"
SIDEBAR_BG = "#0D111A"
CARD_BG = "#131826"
CARD_BG_2 = "#0F1420"

TEXT = "#EDEFF5"
MUTED = "#8B93A7"
BORDER = "#232938"
GRID = "#202636"

ACCENT = "#2FD9B0"          # jade
ACCENT_SOFT = "#173B34"
ACCENT_2 = "#E8B44C"        # brass
ACCENT_2_SOFT = "#3A2E15"
NEGATIVE = "#E8697A"

INPUT_BG = "#0F1420"
INPUT_BORDER = "#2A3143"

RADIUS = "10px"
RADIUS_LG = "14px"
RADIUS_PILL = "999px"

PLOTLY_TEMPLATE = "plotly_dark"
FONT_BODY = "Inter, -apple-system, sans-serif"
FONT_DISPLAY = "'Space Grotesk', Inter, sans-serif"

# Treemap category palette
TREEMAP_COLORS = {
    "Gross Salary": "#1A2030",
    "Deductions": "#3A2530",
    "Income Tax": "#E8697A",
    "PF Contribution": "#D9576A",
    "Insurance": "#C94559",
    "Other Deductions": "#B23A4C",
    "Net Salary": "#12241F",
    "Expenses": "#16283A",
    "Rent": "#5FB8E8",
    "Groceries": "#4FA3D1",
    "EMI": "#3E8DBA",
    "Entertainment": "#2E78A3",
    "Other Expenses": "#1F638C",
    "Savings": "#2FD9B0",
    "Investments": "#22B294",
    "Remaining": "#5A6479",
}


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: {BG};
        color: {TEXT};
        font-family: {FONT_BODY};
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-right: 3rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
    }}

    /* ---------- Header ---------- */

    .ledger-mark {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: {MUTED};
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 6px;
    }}

    .ledger-mark span.dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: {ACCENT};
        display: inline-block;
    }}

    .dashboard-title {{
        font-family: {FONT_DISPLAY};
        font-size: clamp(30px, 3.6vw, 42px);
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.5px;
        color: {TEXT};
        margin: 0;
    }}

    .dashboard-subtitle {{
        color: {MUTED};
        font-size: 15px;
        line-height: 1.55;
        margin-top: 8px;
        max-width: 640px;
    }}

    .header-wrapper {{
        width: 100%;
        padding: 4px 0 20px 0;
        margin-bottom: 6px;
    }}

    /* ---------- Section headings ---------- */

    .section-heading {{
        font-family: {FONT_DISPLAY};
        font-size: 20px;
        font-weight: 600;
        color: {TEXT};
        margin-top: 30px;
        margin-bottom: 4px;
        padding-left: 12px;
        border-left: 3px solid {ACCENT};
    }}

    .section-description {{
        color: {MUTED};
        font-size: 13.5px;
        margin-top: 4px;
        margin-bottom: 18px;
        padding-left: 15px;
    }}

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {{
        background: {SIDEBAR_BG};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.2rem;
    }}

    .sidebar-brand {{
        padding: 4px 10px 22px 10px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 18px;
    }}

    .sidebar-seal {{
        width: 38px;
        height: 38px;
        border-radius: {RADIUS};
        background: {ACCENT};
        color: #08110D;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: {FONT_DISPLAY};
        font-weight: 700;
        font-size: 17px;
        flex-shrink: 0;
    }}

    .sidebar-brand-name {{
        font-family: {FONT_DISPLAY};
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: {TEXT};
        line-height: 1.15;
    }}

    .sidebar-brand-subtitle {{
        color: {MUTED};
        font-size: 11.5px;
        margin-top: 2px;
    }}

    .sidebar-label {{
        color: {MUTED};
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.3px;
        padding: 0 10px 12px 10px;
    }}

    .snapshot-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: {RADIUS_LG};
        padding: 14px 16px;
        margin: 0 8px 10px 8px;
    }}

    .snapshot-row {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: 7px 0;
        border-bottom: 1px dashed {BORDER};
    }}

    .snapshot-row:last-child {{
        border-bottom: none;
    }}

    .snapshot-label {{
        color: {MUTED};
        font-size: 12.5px;
        font-weight: 500;
    }}

    .snapshot-value {{
        font-family: {FONT_DISPLAY};
        color: {TEXT};
        font-size: 15px;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
    }}

    .snapshot-highlight {{
        margin: 0 8px 16px 8px;
        padding: 16px;
        border-radius: {RADIUS_LG};
        background: linear-gradient(135deg, {ACCENT_SOFT} 0%, {CARD_BG} 80%);
        border: 1px solid {BORDER};
    }}

    .snapshot-highlight-label {{
        color: {MUTED};
        font-size: 11.5px;
        font-weight: 600;
        margin-bottom: 4px;
    }}

    .snapshot-highlight-value {{
        font-family: {FONT_DISPLAY};
        color: {ACCENT};
        font-size: 26px;
        font-weight: 700;
    }}

    .progress-track {{
        width: 100%;
        height: 6px;
        border-radius: {RADIUS_PILL};
        background: {BORDER};
        margin-top: 10px;
        overflow: hidden;
    }}

    .progress-fill {{
        height: 100%;
        border-radius: {RADIUS_PILL};
        background: {ACCENT};
    }}

    .sidebar-footnote {{
        color: {MUTED};
        font-size: 11px;
        padding: 10px 16px 0 16px;
        line-height: 1.5;
    }}

    /* ---------- Inputs (unified radius, no clashing corners) ---------- */

    div[data-baseweb="select"] > div {{
        background: {INPUT_BG};
        border: 1px solid {INPUT_BORDER};
        border-radius: {RADIUS};
    }}

    div[data-baseweb="select"] * {{
        color: {TEXT};
        font-family: {FONT_BODY};
    }}

    div[data-baseweb="select"]:focus-within {{
        border-color: {ACCENT};
        box-shadow: 0 0 0 1px {ACCENT};
    }}

    div[data-testid="stNumberInputContainer"] {{
        background: {INPUT_BG};
        border: 1px solid {INPUT_BORDER};
        border-radius: {RADIUS};
        overflow: hidden;
    }}

    div[data-testid="stNumberInputContainer"]:focus-within {{
        border-color: {ACCENT};
        box-shadow: 0 0 0 1px {ACCENT};
    }}

    div[data-testid="stNumberInputContainer"] input {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        color: {TEXT};
        font-family: {FONT_BODY};
    }}

    div[data-testid="stNumberInputContainer"] button {{
        background: {CARD_BG_2} !important;
        border: none !important;
        border-radius: 0 !important;
        color: {MUTED} !important;
    }}

    div[data-testid="stNumberInputContainer"] button:hover {{
        background: {ACCENT_SOFT} !important;
        color: {ACCENT} !important;
    }}

    label {{
        color: {MUTED} !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
    }}

    /* ---------- Buttons ---------- */

    div.stButton > button {{
        border-radius: {RADIUS};
        min-height: 44px;
        font-weight: 600;
        font-family: {FONT_BODY};
        border: 1px solid {BORDER};
        color: {TEXT};
        background: {CARD_BG};
    }}

    div.stButton > button:hover {{
        border-color: {ACCENT};
        color: {ACCENT};
    }}

    div.stButton > button[kind="primary"] {{
        background: {ACCENT};
        color: #08110D;
        border: none;
    }}

    div.stButton > button[kind="primary"]:hover {{
        opacity: 0.9;
        color: #08110D;
    }}

    /* ---------- Metric cards ---------- */

    div[data-testid="stMetric"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: {RADIUS_LG};
        padding: 16px 18px;
        min-height: 100px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {MUTED};
        font-size: 12px;
        font-weight: 600;
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT};
        font-family: {FONT_DISPLAY};
        font-size: 25px;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {CARD_BG};
        border-color: {BORDER};
        border-radius: {RADIUS_LG};
    }}

    /* ---------- AI banner ---------- */

    .ai-banner {{
        background: linear-gradient(135deg, {ACCENT_SOFT} 0%, {CARD_BG} 65%);
        border: 1px solid {BORDER};
        border-left: 3px solid {ACCENT_2};
        border-radius: {RADIUS_LG};
        padding: 18px 20px;
        margin-bottom: 18px;
    }}

    .ai-banner-title {{
        font-family: {FONT_DISPLAY};
        color: {TEXT};
        font-size: 16px;
        font-weight: 600;
    }}

    .ai-banner-text {{
        color: {MUTED};
        font-size: 13.5px;
        line-height: 1.55;
        margin-top: 5px;
    }}

    hr {{ border-color: {BORDER}; }}

    @media (max-width: 900px) {{
        .block-container {{ padding-left: 1.25rem; padding-right: 1.25rem; padding-top: 1.25rem; }}
        .dashboard-title {{ font-size: 30px; }}
        .section-heading {{ font-size: 18px; }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHART THEME HELPER
# ============================================================

def apply_chart_theme(fig, height=380, show_legend=False):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT, family=FONT_BODY, size=12.5),
        height=height,
        margin=dict(l=20, r=20, t=55, b=30),
        showlegend=show_legend,
        legend=dict(font=dict(color=MUTED, size=11), orientation="h", y=-0.15),
        hoverlabel=dict(
            bgcolor=CARD_BG_2,
            bordercolor=BORDER,
            font=dict(color=TEXT, family=FONT_BODY, size=12),
        ),
    )
    # Only style the title font if the chart actually has title text set —
    # setting title_font on a titleless figure (e.g. the gauge) makes
    # Plotly render a stray "undefined" label.
    if fig.layout.title and fig.layout.title.text:
        fig.update_layout(title_font=dict(size=16, color=TEXT, family=FONT_DISPLAY))
    fig.update_xaxes(
        gridcolor=GRID, zerolinecolor=GRID,
        tickfont=dict(color=MUTED), title_font=dict(color=MUTED),
    )
    fig.update_yaxes(
        gridcolor=GRID, zerolinecolor=GRID,
        tickfont=dict(color=MUTED), title_font=dict(color=MUTED),
    )
    return fig


# ============================================================
# SIDEBAR — brand only (live snapshot renders further down,
# once the financial figures have been calculated)
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-seal">K</div>
            <div>
                <div class="sidebar-brand-name">Koshpal</div>
                <div class="sidebar-brand-subtitle">Employee Financial Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Live snapshot</div>', unsafe_allow_html=True)
    snapshot_placeholder = st.container()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="header-wrapper">
        <div class="ledger-mark"><span class="dot"></span>Live financial ledger</div>
        <div class="dashboard-title">AI Financial Intelligence Dashboard</div>
        <div class="dashboard-subtitle">
            Employee financial health analysis, machine learning prediction
            and personalized AI insights — in one place.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EMPLOYEE INFORMATION
# ============================================================

st.markdown('<div class="section-heading">Employee information</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Enter the employee information used for the financial health assessment.</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=22, max_value=60, value=30, step=1, key="age_input")

with col2:
    experience = st.number_input(
        "Years of Experience", min_value=0, max_value=38, value=5, step=1, key="experience_input",
    )

with col3:
    department = st.selectbox(
        "Department",
        ["Sales", "IT", "Operations", "Finance", "Marketing", "Data Science",
         "HR", "Customer Support", "Cyber Security", "Product Management"],
        key="department_input",
    )

if experience > age - 18:
    st.error("Please enter a valid combination of age and years of experience.")
    st.stop()

# ------------------------------------------------------------
# INCOME & DEDUCTIONS
# ------------------------------------------------------------

st.markdown('<div class="section-heading">Income & deductions</div>', unsafe_allow_html=True)

income_col1, income_col2 = st.columns(2)

with income_col1:
    monthly_salary = st.number_input(
        "Monthly Salary", min_value=35000.0, max_value=220000.0, value=90000.0, step=1000.0, key="salary_input",
    )
    income_tax = st.number_input("Income Tax", min_value=0.0, value=5000.0, step=500.0, key="tax_input")
    pf_contribution = st.number_input("PF Contribution", min_value=0.0, value=5000.0, step=500.0, key="pf_input")

with income_col2:
    insurance_deduction = st.number_input(
        "Insurance Deduction", min_value=0.0, value=2000.0, step=500.0, key="insurance_input",
    )
    other_deductions = st.number_input(
        "Other Deductions", min_value=0.0, value=1500.0, step=500.0, key="other_deductions_input",
    )

total_deductions = income_tax + pf_contribution + insurance_deduction + other_deductions
net_salary = monthly_salary - total_deductions

if total_deductions > monthly_salary:
    st.error("Total deductions cannot be greater than your monthly salary.")
    st.stop()

salary_col1, salary_col2 = st.columns(2)

with salary_col1:
    st.metric("In-Hand Salary", f"₹{net_salary:,.0f}")

with salary_col2:
    st.metric("Total Deductions", f"₹{total_deductions:,.0f}")


# ============================================================
# MONTHLY EXPENSES
# ============================================================

st.markdown('<div class="section-heading">Monthly expenses</div>', unsafe_allow_html=True)

expense_col1, expense_col2, expense_col3 = st.columns(3)

with expense_col1:
    rent_expense = st.number_input("Rent Expense", min_value=0.0, value=10000.0, step=500.0, key="rent_input")
    grocery_expense = st.number_input("Grocery Expense", min_value=0.0, value=10000.0, step=500.0, key="grocery_input")

with expense_col2:
    emi = st.number_input("EMI / Loan Payment", min_value=0.0, value=5000.0, step=500.0, key="emi_input")
    entertainment_expense = st.number_input(
        "Entertainment Expense", min_value=0.0, value=5000.0, step=500.0, key="entertainment_input",
    )

with expense_col3:
    other_expenses = st.number_input("Other Expenses", min_value=0.0, value=4000.0, step=500.0, key="other_expenses_input")

total_expenditure = rent_expense + grocery_expense + emi + entertainment_expense + other_expenses

if total_expenditure > net_salary:
    st.error("Your total monthly expenses cannot be greater than your in-hand salary.")
    st.stop()


# ============================================================
# SAVINGS & INVESTMENTS
# ============================================================

st.markdown('<div class="section-heading">Savings & investments</div>', unsafe_allow_html=True)

saving_col1, saving_col2 = st.columns(2)

with saving_col1:
    savings = st.number_input("Savings Amount", min_value=0.0, value=15000.0, step=500.0, key="savings_input")

with saving_col2:
    investments = st.number_input("Investments", min_value=0.0, value=5000.0, step=500.0, key="investments_input")

disposable_income = net_salary - total_expenditure
total_savings_investments = savings + investments

if total_savings_investments > disposable_income:
    st.error("Savings and investments cannot be greater than the money left after your monthly expenses.")
    st.stop()


# ============================================================
# FINANCIAL METRICS
# ============================================================

if net_salary > 0:
    expense_ratio = total_expenditure / net_salary
    savings_ratio = savings / net_salary
    investment_ratio = investments / net_salary
    emi_ratio = emi / net_salary
else:
    expense_ratio = savings_ratio = investment_ratio = emi_ratio = 0

debt_burden_index = round(emi / monthly_salary, 3) if monthly_salary > 0 else 0
investment_to_savings_ratio = round(investments / savings, 3) if savings > 0 else 0

remaining_money = max(disposable_income - savings - investments, 0)


# ============================================================
# SIDEBAR — LIVE SNAPSHOT (filled in now that figures exist)
# ============================================================

with snapshot_placeholder:

    combined_savings_rate = savings_ratio + investment_ratio
    progress_pct = min(combined_savings_rate * 100, 100)

    st.markdown(
        f"""
        <div class="snapshot-highlight">
            <div class="snapshot-highlight-label">Savings + investment rate</div>
            <div class="snapshot-highlight-value">{combined_savings_rate:.1%}</div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{progress_pct}%;"></div>
            </div>
        </div>

        <div class="snapshot-card">
            <div class="snapshot-row">
                <span class="snapshot-label">In-hand salary</span>
                <span class="snapshot-value">₹{net_salary:,.0f}</span>
            </div>
            <div class="snapshot-row">
                <span class="snapshot-label">Total expenses</span>
                <span class="snapshot-value">₹{total_expenditure:,.0f}</span>
            </div>
            <div class="snapshot-row">
                <span class="snapshot-label">Money left after bills</span>
                <span class="snapshot-value">₹{disposable_income:,.0f}</span>
            </div>
            <div class="snapshot-row">
                <span class="snapshot-label">Debt burden</span>
                <span class="snapshot-value">{debt_burden_index:.1%}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-footnote">Updates instantly as you edit the employee\'s '
        'financial details on the right.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FINANCIAL SNAPSHOT
# ============================================================

st.markdown('<div class="section-heading">Financial snapshot</div>', unsafe_allow_html=True)

snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)

with snapshot_col1:
    st.metric("Gross Salary", f"₹{monthly_salary:,.0f}")

with snapshot_col2:
    st.metric("In-Hand Salary", f"₹{net_salary:,.0f}")

with snapshot_col3:
    st.metric("Monthly Expenses", f"₹{total_expenditure:,.0f}", delta=f"{expense_ratio:.1%}", delta_color="inverse")

with snapshot_col4:
    st.metric("Money Left", f"₹{disposable_income:,.0f}")

st.markdown('<div class="section-heading">Financial metrics</div>', unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Savings Ratio", f"{savings_ratio:.2%}")

with metric_col2:
    st.metric("Investment Ratio", f"{investment_ratio:.2%}")

with metric_col3:
    st.metric("EMI Ratio", f"{emi_ratio:.2%}")

with metric_col4:
    st.metric("Debt Burden", f"{debt_burden_index:.2%}")


# ============================================================
# FINANCIAL OVERVIEW CHARTS
# ============================================================

st.markdown('<div class="section-heading">Financial overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">How salary is deducted and where monthly expenses are concentrated.</div>',
    unsafe_allow_html=True,
)

chart_col1, chart_col2 = st.columns(2)

# ---------- Salary deductions: gradient horizontal bar ----------

with chart_col1:

    income_labels = ["Income Tax", "PF Contribution", "Insurance", "Other Deductions"]
    income_values = [income_tax, pf_contribution, insurance_deduction, other_deductions]

    order = sorted(range(len(income_values)), key=lambda i: income_values[i])
    income_labels = [income_labels[i] for i in order]
    income_values = [income_values[i] for i in order]

    max_val = max(income_values) if max(income_values) > 0 else 1
    bar_colors = [f"rgba(47,217,176,{0.35 + 0.55 * (v / max_val)})" for v in income_values]

    fig_income = go.Figure()
    fig_income.add_trace(
        go.Bar(
            x=income_values,
            y=income_labels,
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"₹{v:,.0f}" for v in income_values],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Amount: ₹%{x:,.0f}<extra></extra>",
        )
    )
    fig_income.update_layout(title="Salary deductions", xaxis_title="Amount (₹)")
    apply_chart_theme(fig_income)
    st.plotly_chart(fig_income, use_container_width=True)

# ---------- Expense breakdown: lollipop chart ----------

with chart_col2:

    expense_labels = ["Rent", "Groceries", "EMI", "Entertainment", "Other"]
    expense_values = [rent_expense, grocery_expense, emi, entertainment_expense, other_expenses]

    order = sorted(range(len(expense_values)), key=lambda i: expense_values[i])
    expense_labels = [expense_labels[i] for i in order]
    expense_values = [expense_values[i] for i in order]

    fig_expenses = go.Figure()

    for label, value in zip(expense_labels, expense_values):
        fig_expenses.add_trace(
            go.Scatter(
                x=[0, value], y=[label, label],
                mode="lines",
                line=dict(color=BORDER, width=3),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig_expenses.add_trace(
        go.Scatter(
            x=expense_values, y=expense_labels,
            mode="markers+text",
            marker=dict(size=16, color=ACCENT_2, line=dict(width=2, color=CARD_BG)),
            text=[f"₹{v:,.0f}" for v in expense_values],
            textposition="middle right",
            textfont=dict(color=TEXT, size=12),
            hovertemplate="<b>%{y}</b><br>Amount: ₹%{x:,.0f}<extra></extra>",
            showlegend=False,
        )
    )

    fig_expenses.update_layout(title="Monthly expense breakdown", xaxis_title="Amount (₹)")
    fig_expenses.update_xaxes(range=[0, max(expense_values) * 1.35 if max(expense_values) > 0 else 1])
    apply_chart_theme(fig_expenses)
    st.plotly_chart(fig_expenses, use_container_width=True)


# ============================================================
# WHERE YOUR MONEY GOES — TREEMAP
# ============================================================

st.markdown('<div class="section-heading">Where your money goes</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Proportional breakdown of gross salary across deductions, '
    'expenses, savings and investments — click a block to zoom in.</div>',
    unsafe_allow_html=True,
)

treemap_ids = [
    "Gross Salary",
    "Deductions", "Income Tax", "PF Contribution", "Insurance", "Other Deductions",
    "Net Salary",
    "Expenses", "Rent", "Groceries", "EMI", "Entertainment", "Other Expenses",
    "Savings", "Investments",
]
treemap_parents = [
    "",
    "Gross Salary", "Deductions", "Deductions", "Deductions", "Deductions",
    "Gross Salary",
    "Net Salary", "Expenses", "Expenses", "Expenses", "Expenses", "Expenses",
    "Net Salary", "Net Salary",
]
treemap_values = [
    monthly_salary,
    total_deductions, income_tax, pf_contribution, insurance_deduction, other_deductions,
    net_salary,
    total_expenditure, rent_expense, grocery_expense, emi, entertainment_expense, other_expenses,
    savings, investments,
]

if remaining_money > 0:
    treemap_ids.append("Remaining")
    treemap_parents.append("Net Salary")
    treemap_values.append(remaining_money)

treemap_colors = [TREEMAP_COLORS.get(node, MUTED) for node in treemap_ids]

fig_treemap = go.Figure(
    go.Treemap(
        ids=treemap_ids,
        labels=treemap_ids,
        parents=treemap_parents,
        values=treemap_values,
        branchvalues="total",
        marker=dict(
            colors=treemap_colors,
            line=dict(width=2, color=BG),
            pad=dict(t=4, l=4, r=4, b=4),
        ),
        textfont=dict(color="#FFFFFF", size=13, family=FONT_BODY),
        texttemplate="<b>%{label}</b><br>₹%{value:,.0f}",
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percentParent:.1%} of parent<extra></extra>",
        pathbar=dict(visible=True, textfont=dict(color=MUTED, size=12)),
        root=dict(color=BG),
    )
)

fig_treemap.update_layout(title="Monthly money allocation")
apply_chart_theme(fig_treemap, height=460)
st.plotly_chart(fig_treemap, use_container_width=True)


# ---------- Summary strip ----------

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric("Total Deductions", f"₹{total_deductions:,.0f}")

with summary_col2:
    st.metric("Savings + Investments", f"₹{total_savings_investments:,.0f}")

with summary_col3:
    st.metric("Unallocated Money", f"₹{remaining_money:,.0f}")


# ============================================================
# FINANCIAL RATIOS — RADAR CHART
# ============================================================

st.markdown('<div class="section-heading">Financial ratios</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">A balanced profile keeps expenses low and savings/investments high.</div>',
    unsafe_allow_html=True,
)

ratio_labels = ["Expenses", "Savings", "Investments", "EMI"]
ratio_values = [expense_ratio * 100, savings_ratio * 100, investment_ratio * 100, emi_ratio * 100]

fig_ratios = go.Figure()

fig_ratios.add_trace(
    go.Scatterpolar(
        r=ratio_values + [ratio_values[0]],
        theta=ratio_labels + [ratio_labels[0]],
        fill="toself",
        fillcolor="rgba(47,217,176,0.25)",
        line=dict(color=ACCENT, width=2),
        marker=dict(size=7, color=ACCENT_2),
        hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>",
        name="Ratio",
    )
)

fig_ratios.update_layout(
    title="Financial ratio profile",
    polar=dict(
        bgcolor=CARD_BG,
        radialaxis=dict(
            visible=True, range=[0, max(ratio_values + [10]) * 1.2],
            gridcolor=GRID, tickfont=dict(color=MUTED, size=10),
        ),
        angularaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT, size=12)),
    ),
)
apply_chart_theme(fig_ratios, height=420)
st.plotly_chart(fig_ratios, use_container_width=True)


# ============================================================
# BUILD EMPLOYEE DATA
# ============================================================

employee_data = {
    "Age": age,
    "Years_of_Experience": experience,
    "Department": department,
    "Monthly_Salary": monthly_salary,
    "Income_Tax": income_tax,
    "PF_Contribution": pf_contribution,
    "Insurance_Deduction": insurance_deduction,
    "Other_Deductions": other_deductions,
    "Net_Salary": net_salary,
    "Rent_Expense": rent_expense,
    "Grocery_Expense": grocery_expense,
    "EMI_or_Loan_Payment": emi,
    "Entertainment_Expense": entertainment_expense,
    "Other_Expenses": other_expenses,
    "Total_Expenditure": total_expenditure,
    "Savings_Amount": savings,
    "Investments": investments,
    "Disposable_Income": disposable_income,
    "Debt_Burden_Index": debt_burden_index,
    "Investment_to_Savings_Ratio": investment_to_savings_ratio,
}

missing_features = [f for f in final_features if f not in employee_data]

if missing_features:
    st.error(f"Missing model features: {missing_features}")
    st.stop()


# ============================================================
# FINANCIAL HEALTH ASSESSMENT PAGE
# ============================================================

st.markdown('<div class="section-heading">Financial health assessment</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Run the trained XGBoost model using the employee financial information entered above.</div>',
    unsafe_allow_html=True,
)

assess_button = st.button("Assess Financial Health", type="primary", use_container_width=True)

if assess_button:
    try:
        with st.spinner("Analyzing your financial health..."):
            prediction_result = predict_financial_health(employee_data)

        st.session_state.prediction_result = prediction_result
        st.session_state.recommendations = None

    except Exception as e:
        st.error(f"Unable to complete the financial assessment: {e}")


prediction_result = st.session_state.prediction_result

if prediction_result is not None:

    st.markdown('<div class="section-heading">Predicted financial health</div>', unsafe_allow_html=True)

    prediction = prediction_result.get("prediction")
    confidence = prediction_result.get("confidence", 0)
    probabilities = prediction_result.get("probabilities", {})

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        with st.container(border=True):
            st.metric("Predicted Financial Health", str(prediction))
            st.caption("Prediction generated by the trained XGBoost model.")

    with result_col2:
        with st.container(border=True):

            fig_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=confidence * 100,
                    number=dict(suffix="%", font=dict(color=TEXT, family=FONT_DISPLAY, size=30)),
                    gauge=dict(
                        axis=dict(range=[0, 100], tickcolor=MUTED, tickfont=dict(color=MUTED, size=10)),
                        bar=dict(color=ACCENT, thickness=0.3),
                        bgcolor=CARD_BG,
                        borderwidth=0,
                        steps=[
                            dict(range=[0, 50], color="#241A0E"),
                            dict(range=[50, 80], color=CARD_BG_2),
                            dict(range=[80, 100], color=ACCENT_SOFT),
                        ],
                    ),
                    title=dict(text="Model Confidence", font=dict(color=MUTED, size=13)),
                )
            )
            apply_chart_theme(fig_gauge, height=200)
            fig_gauge.update_layout(margin=dict(l=20, r=20, t=40, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

    if probabilities:

        probability_df = pd.DataFrame(
            {
                "Financial Health": list(probabilities.keys()),
                "Probability": [v * 100 for v in probabilities.values()],
            }
        ).sort_values("Probability")

        st.markdown('<div class="section-heading">Model prediction probabilities</div>', unsafe_allow_html=True)

        fig_probability = go.Figure()
        fig_probability.add_trace(
            go.Bar(
                x=probability_df["Probability"],
                y=probability_df["Financial Health"],
                orientation="h",
                marker=dict(color=ACCENT, line=dict(width=0)),
                text=[f"{v:.2f}%" for v in probability_df["Probability"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Probability: %{x:.2f}%<extra></extra>",
            )
        )
        fig_probability.update_layout(title="Prediction probabilities", xaxis_title="Probability (%)", xaxis_range=[0, 105])
        apply_chart_theme(fig_probability, height=340)
        st.plotly_chart(fig_probability, use_container_width=True)


# ============================================================
# AI INSIGHTS PAGE
# ============================================================

st.markdown('<div class="section-heading">AI-powered financial recommendations</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="ai-banner">
        <div class="ai-banner-title">Personalized financial guidance</div>
        <div class="ai-banner-text">
            Recommendations are generated using the employee's financial information,
            calculated financial metrics, and the XGBoost financial health prediction.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if prediction_result is None:
    st.info("Run the Financial Health Assessment above to generate personalized AI insights.")

else:
    prediction = prediction_result.get("prediction")
    confidence = prediction_result.get("confidence", 0)
    probabilities = prediction_result.get("probabilities", {})

    llm_profile = {
        "employee_data": employee_data,
        "xgboost_prediction": prediction,
        "prediction_confidence": confidence,
        "class_probabilities": probabilities,
        "calculated_metrics": {
            "Total_Expenditure": total_expenditure,
            "Disposable_Income": disposable_income,
            "Expense_Ratio": expense_ratio,
            "Savings_Ratio": savings_ratio,
            "Investment_Ratio": investment_ratio,
            "EMI_Ratio": emi_ratio,
            "Debt_Burden_Index": debt_burden_index,
            "Investment_to_Savings_Ratio": investment_to_savings_ratio,
        },
    }

    if st.session_state.recommendations is None:

        generate_button = st.button(
            "Generate Personalized AI Insights", type="primary", use_container_width=True,
        )

        if generate_button:
            try:
                with st.spinner("Generating personalized recommendations..."):
                    recommendations = generate_financial_report(
                        employee_data=llm_profile, prediction_result=prediction_result,
                    )

                st.session_state.recommendations = recommendations
                st.rerun()

            except Exception as e:
                st.error(f"Unable to generate AI recommendations: {e}")

    if st.session_state.recommendations:

        st.markdown(st.session_state.recommendations)
        st.divider()
        st.caption(
            "Disclaimer: This assessment is generated using an automated machine "
            "learning model and an AI language model. It is provided for informational "
            "purposes only and does not constitute professional financial advice."
        )


# ============================================================
# OVERVIEW PAGE — WORKFLOW
# ============================================================




# ============================================================
# FOOTER
# ============================================================

st.divider()

footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:
    st.caption("Koshpal • AI Financial Intelligence Dashboard")

with footer_col2:
    st.caption("ML + AI powered financial analysis")