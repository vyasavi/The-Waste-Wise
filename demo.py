import streamlit as st
import pandas as pd
import altair as alt
import pickle

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="The Waste Wise",
    page_icon="icon.png",
    layout="centered",
)

# Load the trained model once
model_filename = 'workfile'
with open(model_filename, 'rb') as f:
    copy_of_model = pickle.load(f)

# ---------------------------------------------------------------------------
# Design system  —  white canvas, green accent, generous whitespace
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Hide Streamlit chrome for a product-grade look */
    [data-testid="stDecoration"], [data-testid="stToolbar"] { display: none; }
    header[data-testid="stHeader"] { background: transparent; height: 0; }
    #MainMenu, footer { visibility: hidden; }

    .block-container { padding-top: 3.5rem; padding-bottom: 3rem; max-width: 760px; }

    /* Typography */
    .eyebrow {
        text-transform: uppercase; letter-spacing: 2.5px; font-size: .78rem;
        font-weight: 700; color: #2E8B57; margin-bottom: .6rem;
    }
    .hero-title {
        font-size: 3rem; font-weight: 800; line-height: 1.05;
        letter-spacing: -1px; color: #101828; margin: 0 0 1.1rem 0;
    }
    .hero-title span { color: #2E8B57; }
    .hero-sub {
        font-size: 1.12rem; color: #667085; line-height: 1.6; max-width: 48ch;
        margin-bottom: .5rem;
    }
    .section-label {
        text-transform: uppercase; letter-spacing: 2px; font-size: .74rem;
        font-weight: 700; color: #98a2b3; margin: 2.75rem 0 1rem 0;
    }

    /* Feature cards (self-contained HTML, no Streamlit nesting) */
    .features { display: flex; gap: 1rem; }
    .feat {
        flex: 1; background: #fff; border: 1px solid #eaecef;
        border-radius: 16px; padding: 1.4rem 1.25rem;
    }
    .feat .badge {
        width: 32px; height: 32px; border-radius: 9px;
        background: #eaf5ee; color: #2E8B57; font-weight: 800;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: .9rem; font-size: .95rem;
    }
    .feat .t { font-weight: 700; color: #101828; margin-bottom: .35rem; font-size: 1rem; }
    .feat .d { color: #667085; font-size: .9rem; line-height: 1.5; }

    /* Inputs */
    div[data-testid="stNumberInput"] label p { font-weight: 600; color: #344054; }
    div[data-baseweb="input"] { border-radius: 10px; }

    /* Primary button */
    div.stButton > button {
        border-radius: 10px; font-weight: 700; letter-spacing: .2px;
        padding: .6rem 1.6rem; border: none;
    }

    /* KPI tiles */
    div[data-testid="stMetric"] {
        background: #fff; border: 1px solid #eaecef; border-radius: 14px;
        padding: 1rem 1.15rem;
    }
    div[data-testid="stMetric"] { border-left: 4px solid #2E8B57; }
    div[data-testid="stMetricLabel"] p { color: #667085; font-weight: 600; }
    div[data-testid="stMetricValue"] { font-size: 1.45rem; }

    .footer {
        border-top: 1px solid #eaecef; margin-top: 3.5rem; padding-top: 1.5rem;
        color: #98a2b3; font-size: .88rem; text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt(n):
    return f"{int(n):,}"


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def predict_units(inflation_pct, income, month):
    """Predicted units sold for the given economic inputs."""
    X = pd.DataFrame({
        "Inflation": [inflation_pct / 100],
        "Disposable Income": [income],
        "Month of the Year": [month],
    })
    return int(copy_of_model.predict(X)[0])


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.image("logo-no-background.png", width=150)
st.markdown('<div class="eyebrow">Demand forecasting for manufacturers</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Cutting waste,<br><span>growing profits.</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-sub">Predict demand from three economic signals, then produce '
    'to the forecast instead of guesswork — and cut the waste in between.</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="features">
      <div class="feat">
        <div class="badge">1</div>
        <div class="t">Signals in</div>
        <div class="d">Inflation, disposable income, and the month of the year.</div>
      </div>
      <div class="feat">
        <div class="badge">2</div>
        <div class="t">Forecast</div>
        <div class="d">A trained model predicts how many units you'll sell.</div>
      </div>
      <div class="feat">
        <div class="badge">3</div>
        <div class="t">Resources out</div>
        <div class="d">Raw material, packaging, energy and transport estimates.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Predictor
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Try it</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    inflation = st.number_input('Inflation (%)', min_value=0.0, value=3.0)
with c2:
    disposable_income = st.number_input('Disposable income ($)', value=3000.0)
with c3:
    month_of_year = st.number_input('Month (1–12)', min_value=1, max_value=12, value=6)
st.caption("Results update live as you adjust the inputs.")

# ---------------------------------------------------------------------------
# Forecast (computed on every run, so it's populated on first load)
# ---------------------------------------------------------------------------
units = predict_units(inflation, disposable_income, month_of_year)

st.markdown('<div class="section-label">Forecast</div>', unsafe_allow_html=True)
st.metric(f"Predicted units sold · {MONTHS[month_of_year - 1]}", fmt(units))
st.caption("Estimated resources to produce that volume")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Raw material", f"{fmt(units * 0.142)} kg")
m2.metric("Packaging", f"{fmt(units * 0.028)} kg")
m3.metric("Energy", f"{fmt(units * 0.3)} kWh")
m4.metric("Transport", f"{fmt(units * 0.025)} bags")

# ---------------------------------------------------------------------------
# Seasonal demand across the year (holding inflation & income fixed)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Seasonal demand</div>', unsafe_allow_html=True)
season = pd.DataFrame({
    "Month": MONTHS,
    "Predicted units": [predict_units(inflation, disposable_income, m)
                        for m in range(1, 13)],
})
chart = (
    alt.Chart(season)
    .mark_line(color="#2E8B57", point=alt.OverlayMarkDef(color="#2E8B57"))
    .encode(
        x=alt.X("Month:N", sort=MONTHS, title=None),
        y=alt.Y("Predicted units:Q", title=None),
        tooltip=["Month", "Predicted units"],
    )
    .properties(height=260)
)
st.altair_chart(chart, use_container_width=True)
st.caption("Forecast demand across the year at your current inflation and income levels.")

# ---------------------------------------------------------------------------
# Batch forecast: score every row of an uploaded CSV
# ---------------------------------------------------------------------------
REQUIRED_COLS = ["Inflation", "Disposable Income", "Month of the Year"]

with st.expander("Have your own data? Upload a CSV to forecast every row"):
    st.caption(
        f"CSV must include the columns: {', '.join(REQUIRED_COLS)}. "
        "Inflation is a fraction (e.g. 0.03 for 3%)."
    )
    st.image("screen.png", caption="Expected CSV layout")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        missing = [c for c in REQUIRED_COLS if c not in data.columns]
        if missing:
            st.error(f"Missing required column(s): {', '.join(missing)}")
        else:
            preds = copy_of_model.predict(data[REQUIRED_COLS])
            out = data.copy()
            out["Predicted units"] = preds.round().astype(int)
            out["Raw material (kg)"] = (out["Predicted units"] * 0.142).round().astype(int)
            out["Packaging (kg)"] = (out["Predicted units"] * 0.028).round().astype(int)
            out["Energy (kWh)"] = (out["Predicted units"] * 0.3).round().astype(int)
            out["Transport (bags)"] = (out["Predicted units"] * 0.025).round().astype(int)
            st.success(f"Scored {len(out):,} rows.")
            st.dataframe(out, use_container_width=True)
            st.download_button(
                "Download predictions",
                out.to_csv(index=False),
                file_name="waste_wise_predictions.csv",
                mime="text/csv",
            )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        The Waste Wise · Demand forecasting for manufacturers
    </div>
    """,
    unsafe_allow_html=True,
)
