import streamlit as st
import pandas as pd

st.set_page_config(page_title="Brazil–Canada Trade Dashboard", layout="wide")

st.title("Brazil–Canada Trade Dashboard")
st.markdown("Data source: Statistics Canada (automated monthly update)")

# =============================
# Load dataset
# =============================

df = pd.read_csv("data/trade_data.csv")
df["date"] = pd.to_datetime(df["date"])

# =============================
# Sidebar filters
# =============================

st.sidebar.header("Filters")

vector_ids = sorted(df["vectorId"].unique())
selected_vector = st.sidebar.selectbox("Select Vector", vector_ids)

filtered_df = df[df["vectorId"] == selected_vector]
filtered_df = filtered_df.sort_values("date")

# =============================
# Last 5 years filter
# =============================

five_years_ago = pd.Timestamp.today() - pd.DateOffset(years=5)
filtered_df = filtered_df[filtered_df["date"] >= five_years_ago]

# =============================
# KPIs (Safe Version)
# =============================

if len(filtered_df) >= 2:
    latest_value = filtered_df.iloc[-1]["value"]
    previous_value = filtered_df.iloc[-2]["value"]
    delta_value = latest_value - previous_value
else:
    latest_value = filtered_df.iloc[-1]["value"]
    delta_value = 0

st.metric(
    label="Latest Month Value",
    value=f"{latest_value:,.2f}",
    delta=f"{delta_value:,.2f}"
)

# =============================
# Chart
# =============================

st.subheader("Monthly Evolution (Last 5 Years)")

st.line_chart(
    filtered_df.set_index("date")["value"]
)

# =============================
# Raw Data
# =============================

with st.expander("See Raw Data"):
    st.dataframe(filtered_df.sort_values("date", ascending=False))
