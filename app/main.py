"""
InsureWise AI — Health Insurance Premium Predictor
A modern, healthcare-finance themed Streamlit dashboard.

Requires: streamlit, plotly
Expects a sibling module `prediction_helper.py` exposing a `predict(input_dict) -> float` function.
"""

import time
import streamlit as st
import plotly.graph_objects as go

from prediction_helper import predict

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="InsureWise AI | Health Insurance Predictor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# THEME TOKENS
# ----------------------------------------------------------------------------
PRIMARY = "#1565C0"      # Deep Blue
SECONDARY = "#26A69A"    # Teal
ACCENT = "#2E7D32"       # Emerald Green
RISK_LOW = "#2E7D32"
RISK_MOD = "#F9A825"
RISK_HIGH = "#C62828"

# ----------------------------------------------------------------------------
# GLOBAL CSS
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background: linear-gradient(180deg, #EAF4FF 0%, #F7FBFF 35%, #FFFFFF 100%);
}}

#MainMenu, footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{background: transparent;}}

/* ---------------- HERO ---------------- */
.hero {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    border-radius: 24px;
    padding: 2.6rem 2.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 12px 35px rgba(21, 101, 192, 0.25);
    animation: fadeInDown 0.7s ease;
    position: relative;
    overflow: hidden;
}}
.hero::after {{
    content: "";
    position: absolute;
    top: -40%; right: -10%;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    border-radius: 50%;
}}
.hero-icon {{
    font-size: 2.6rem;
    background: rgba(255,255,255,0.18);
    width: 64px; height: 64px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 16px;
    margin-bottom: 0.9rem;
    backdrop-filter: blur(6px);
}}
.hero h1 {{
    color: #FFFFFF;
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}}
.hero .tagline {{
    color: rgba(255,255,255,0.95);
    font-size: 1.08rem;
    font-weight: 500;
    margin-bottom: 0.6rem;
}}
.hero .desc {{
    color: rgba(255,255,255,0.85);
    font-size: 0.92rem;
    font-weight: 300;
    max-width: 680px;
    line-height: 1.5;
}}

@keyframes fadeInDown {{
    from {{ opacity: 0; transform: translateY(-14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ---------------- SECTION HEADERS ---------------- */
.section-title {{
    font-size: 1.02rem;
    font-weight: 700;
    color: {PRIMARY};
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
}}

/* ---------------- GLASS CARD ---------------- */
.glass-card {{
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 18px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 8px 28px rgba(21, 101, 192, 0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: fadeIn 0.6s ease;
    margin-bottom: 1.1rem;
}}
.glass-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 14px 34px rgba(21, 101, 192, 0.15);
}}

/* ---------------- EXPANDERS AS CARDS ---------------- */
div[data-testid="stExpander"] {{
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(21, 101, 192, 0.08);
    border-radius: 18px !important;
    box-shadow: 0 6px 22px rgba(21, 101, 192, 0.07);
    margin-bottom: 1rem;
    transition: box-shadow 0.25s ease;
    overflow: hidden;
}}
div[data-testid="stExpander"]:hover {{
    box-shadow: 0 10px 28px rgba(21, 101, 192, 0.14);
}}
div[data-testid="stExpander"] summary {{
    font-weight: 600;
    font-size: 1.0rem;
    color: {PRIMARY};
}}

/* ---------------- RISK PILLS ---------------- */
.risk-pill {{
    display: inline-block;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.3px;
}}
.risk-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0;
    border-bottom: 1px dashed rgba(21,101,192,0.15);
}}
.risk-row:last-child {{ border-bottom: none; }}
.risk-label {{
    font-size: 0.86rem;
    font-weight: 500;
    color: #2C3E50;
}}

/* ---------------- PROGRESS BAR ---------------- */
.progress-outer {{
    width: 100%;
    background: rgba(21,101,192,0.08);
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
    margin-top: 0.4rem;
}}
.progress-inner {{
    height: 100%;
    border-radius: 999px;
    transition: width 1.1s ease;
}}

/* ---------------- PREDICT BUTTON ---------------- */
.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.85rem 1rem;
    border-radius: 14px;
    border: none;
    box-shadow: 0 10px 26px rgba(21, 101, 192, 0.3);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}}
.stButton > button:hover {{
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 14px 32px rgba(38, 166, 154, 0.4);
    color: white;
}}

/* ---------------- SUCCESS CARD ---------------- */
.success-card {{
    background: linear-gradient(135deg, rgba(46,125,50,0.94) 0%, rgba(38,166,154,0.94) 100%);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    color: white;
    box-shadow: 0 14px 36px rgba(46, 125, 50, 0.28);
    animation: fadeIn 0.6s ease;
    margin: 1rem 0 1.6rem 0;
}}
.success-card .amount {{
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0.1rem 0 0.3rem 0;
}}
.success-card .label {{
    font-size: 0.82rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}}

/* ---------------- FOOTER ---------------- */
.app-footer {{
    text-align: center;
    color: #7A8A99;
    font-size: 0.82rem;
    padding: 1.6rem 0 0.6rem 0;
    margin-top: 1.5rem;
    border-top: 1px solid rgba(21,101,192,0.1);
}}

/* tighten default streamlit spacing */
div[data-testid="stVerticalBlock"] > div {{ gap: 0.4rem; }}

/* ---------------- FORCE LABEL VISIBILITY (fixes invisible labels on mobile / dark mode) ---------------- */
label, .stSelectbox label, .stNumberInput label, .stTextInput label,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label {{
    color: #1A2B3C !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    opacity: 1 !important;
}}

/* Selectbox / number input text itself */
.stSelectbox div[data-baseweb="select"] span,
input[type="number"], input[type="text"] {{
    color: #1A2B3C !important;
}}

/* Number input / text input boxes need a light background to match the dark text above */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
.stNumberInput input,
.stTextInput input {{
    background-color: #FFFFFF !important;
    border: 1px solid rgba(21,101,192,0.25) !important;
    border-radius: 8px !important;
}}

/* The +/- step buttons on number inputs */
div[data-testid="stNumberInput"] button {{
    background-color: #F0F4FA !important;
    color: #1A2B3C !important;
    border: 1px solid rgba(21,101,192,0.25) !important;
}}

/* Help tooltip icon visibility */
div[data-testid="stTooltipIcon"] svg {{
    color: {PRIMARY} !important;
}}

@media (max-width: 640px) {{
    label, div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label {{
        font-size: 1rem !important;
    }}
    .hero h1 {{ font-size: 1.7rem; }}
    .hero .tagline {{ font-size: 0.95rem; }}
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HERO SECTION
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-icon">🛡️</div>
    <h1>InsureWise AI</h1>
    <div class="tagline">Predict your health insurance premium instantly using AI-powered risk analysis.</div>
    <div class="desc">Enter your personal, lifestyle, and health details to receive an estimated insurance
    premium based on advanced machine learning models. Designed to help users understand how different
    factors influence insurance costs.</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# OPTIONS
# ----------------------------------------------------------------------------
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# ----------------------------------------------------------------------------
# RISK ENGINE (heuristic — used after prediction to enrich the results view)
# ----------------------------------------------------------------------------
def age_risk(age):
    if age < 30:
        return "Low", 18
    elif age <= 50:
        return "Moderate", 52
    return "High", 86


def medical_risk(medical_history, genetical_risk):
    multi_condition = '&' in medical_history
    severe = 'Heart disease' in medical_history
    if medical_history == 'No Disease' and genetical_risk <= 1:
        base = 12
    elif multi_condition or severe or genetical_risk >= 4:
        base = 88
    elif medical_history != 'No Disease' or genetical_risk >= 2:
        base = 54
    else:
        base = 25
    return ("High" if base >= 70 else "Moderate" if base >= 40 else "Low"), base


def lifestyle_risk(smoking_status, bmi_category):
    if smoking_status == 'Regular' or bmi_category == 'Obesity':
        base = 85
    elif smoking_status == 'Occasional' or bmi_category == 'Overweight':
        base = 50
    else:
        base = 16
    return ("High" if base >= 70 else "Moderate" if base >= 40 else "Low"), base


def risk_color(label):
    return {"Low": RISK_LOW, "Moderate": RISK_MOD, "High": RISK_HIGH}[label]


def overall_risk(scores):
    avg = sum(scores) / len(scores)
    label = "High" if avg >= 65 else "Moderate" if avg >= 35 else "Low"
    return label, avg


# ----------------------------------------------------------------------------
# MAIN LAYOUT — single-column input form (live risk sidebar removed)
# ----------------------------------------------------------------------------

# ---- Section 1: Personal Information ----
with st.expander("👤  Personal Information", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input('Age', min_value=18, max_value=100, step=1,
                               help="Your current age in years. Premiums typically rise with age.")
    with c2:
        gender = st.selectbox('Gender', categorical_options['Gender'],
                               help="Biological sex as recorded on your policy application.")
    with c3:
        marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'],
                                       help="Married applicants may be eligible for family-linked plans.")

# ---- Section 2: Financial Information ----
with st.expander("💰  Financial Information", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        income_lakhs = st.number_input('Income in Lakhs', min_value=0, max_value=200, step=1,
                                        help="Your annual income in INR Lakhs.")
    with c2:
        employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'],
                                          help="Your current employment type.")
    with c3:
        insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'],
                                       help="Higher tiers offer broader coverage at a higher premium.")

# ---- Section 3: Health Information ----
with st.expander("🏥  Health Information", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'],
                                     help="Your Body Mass Index classification.")
    with c2:
        medical_history = st.selectbox('Medical History', categorical_options['Medical History'],
                                        help="Pre-existing or diagnosed medical conditions.")
    c3, c4 = st.columns(2)
    with c3:
        genetical_risk = st.number_input('Genetical Risk', min_value=0, max_value=5, step=1,
                                           help="Family/genetic predisposition score, 0 (none) to 5 (high).")
    with c4:
        smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'],
                                       help="Your current smoking habits.")

# ---- Section 4: Family Information ----
with st.expander("👨‍👩‍👧  Family Information", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        number_of_dependants = st.number_input('Number of Dependants', min_value=0, max_value=20, step=1,
                                                 help="Number of people financially dependent on you.")
    with c2:
        region = st.selectbox('Region', categorical_options['Region'],
                               help="Your place of residence, used for regional cost adjustment.")

# Compute risk scores quietly in the background (used in the results section below,
# no longer shown as a live sidebar summary).
a_label, a_score = age_risk(age)
m_label, m_score = medical_risk(medical_history, genetical_risk)
l_label, l_score = lifestyle_risk(smoking_status, bmi_category)
o_label, o_score = overall_risk([a_score, m_score, l_score])

# ----------------------------------------------------------------------------
# INPUT DICTIONARY
# ----------------------------------------------------------------------------
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# ----------------------------------------------------------------------------
# PREDICTION
# ----------------------------------------------------------------------------
st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
predict_clicked = st.button('🔮  Predict Premium')

if predict_clicked:
    with st.spinner('Analyzing your risk profile and computing premium...'):
        time.sleep(1.1)
        try:
            prediction = predict(input_dict)
        except Exception as e:
            st.error(f"Couldn't generate a prediction: {e}")
            st.stop()

    st.markdown(f"""
    <div class="success-card">
        <div class="label">Estimated Annual Premium</div>
        <div class="amount">₹ {prediction:,.0f}</div>
        <div style="display:flex; gap:2.2rem; margin-top:0.6rem; flex-wrap:wrap;">
            <div><div class="label">Risk Category</div><div style="font-weight:700;">{o_label}</div></div>
            <div><div class="label">Insurance Plan</div><div style="font-weight:700;">{insurance_plan}</div></div>
            <div><div class="label">Region</div><div style="font-weight:700;">{region}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- VISUALIZATION AREA ----------------
    v1, v2 = st.columns(2, gap="large")

    # Premium gauge meter
    with v1:
        st.markdown('<div class="section-title">⏱️ Premium Gauge</div>', unsafe_allow_html=True)
        gauge_max = max(prediction * 1.8, 10000)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            number={'prefix': "₹", 'font': {'size': 30, 'color': PRIMARY}},
            gauge={
                'axis': {'range': [0, gauge_max], 'tickcolor': PRIMARY},
                'bar': {'color': PRIMARY, 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, gauge_max * 0.4], 'color': '#C8E6C9'},
                    {'range': [gauge_max * 0.4, gauge_max * 0.7], 'color': '#FFE082'},
                    {'range': [gauge_max * 0.7, gauge_max], 'color': '#FFAB91'},
                ],
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(t=20, b=10, l=20, r=20),
                                 paper_bgcolor="rgba(0,0,0,0)", font={'family': "Poppins", 'color': "#1A2B3C", 'size': 13})
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Risk score progress / breakdown bar (now shown only post-prediction)
    with v2:
        st.markdown('<div class="section-title">📈 Risk Score Breakdown</div>', unsafe_allow_html=True)
        fig_risk = go.Figure(go.Bar(
            x=[a_score, m_score, l_score],
            y=["Age", "Medical", "Lifestyle"],
            orientation='h',
            marker=dict(color=[risk_color(a_label), risk_color(m_label), risk_color(l_label)]),
            text=[f"{a_score}", f"{m_score}", f"{l_score}"],
            textposition='outside',
        ))
        fig_risk.update_layout(
            height=260, margin=dict(t=20, b=10, l=10, r=20),
            xaxis=dict(range=[0, 100], title="Risk score"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "Poppins", 'color': "#1A2B3C", 'size': 13}
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    v3, v4 = st.columns(2, gap="large")

    # Feature impact chart (illustrative weighting derived from inputs)
    with v3:
        st.markdown('<div class="section-title">🧩 Feature Impact</div>', unsafe_allow_html=True)
        impact_labels = ["Smoking", "Medical History", "Age", "Genetical Risk", "BMI", "Income", "Dependants"]
        impact_values = [
            {'No Smoking': 5, 'Occasional': 35, 'Regular': 60}[smoking_status],
            {'No Disease': 5}.get(medical_history, 30 if '&' not in medical_history else 55),
            min(age, 100) * 0.4,
            genetical_risk * 9,
            {'Underweight': 15, 'Normal': 5, 'Overweight': 25, 'Obesity': 45}[bmi_category],
            max(0, 20 - income_lakhs * 0.15),
            number_of_dependants * 3,
        ]
        order = sorted(zip(impact_labels, impact_values), key=lambda x: x[1])
        labels_sorted, values_sorted = zip(*order)
        fig_impact = go.Figure(go.Bar(
            x=values_sorted, y=labels_sorted, orientation='h',
            marker=dict(color=values_sorted, colorscale=[[0, "#B2DFDB"], [1, PRIMARY]]),
        ))
        fig_impact.update_layout(
            height=300, margin=dict(t=20, b=10, l=10, r=20),
            xaxis=dict(title="Relative influence"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "Poppins", 'color': "#1A2B3C", 'size': 13}
        )
        st.plotly_chart(fig_impact, use_container_width=True)
        st.caption("Illustrative weighting based on your entered profile — not the model's internal feature importances.")

    # Premium comparison across plans (re-queries the model per plan)
    with v4:
        st.markdown('<div class="section-title">⚖️ Premium by Plan</div>', unsafe_allow_html=True)
        plan_values = {}
        for plan in categorical_options['Insurance Plan']:
            trial_input = dict(input_dict)
            trial_input['Insurance Plan'] = plan
            try:
                plan_values[plan] = predict(trial_input)
            except Exception:
                plan_values[plan] = None

        plans = list(plan_values.keys())
        values = [plan_values[p] if plan_values[p] is not None else 0 for p in plans]
        colors = [SECONDARY if p != insurance_plan else PRIMARY for p in plans]
        fig_compare = go.Figure(go.Bar(
            x=plans, y=values, marker=dict(color=colors),
            text=[f"₹{v:,.0f}" if v else "N/A" for v in values],
            textposition='outside',
        ))
        fig_compare.update_layout(
            height=300, margin=dict(t=20, b=10, l=10, r=20),
            yaxis=dict(title="Estimated premium (₹)"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "Poppins", 'color': "#1A2B3C", 'size': 13}
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="app-footer">Powered by Machine Learning | Developed by Arnab Chatterjee</div>
""", unsafe_allow_html=True)