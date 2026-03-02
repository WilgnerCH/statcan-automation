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

vector_ids = df["vectorId"].unique()
selected_vector = st.sidebar.selectbox("Select Vector", vector_ids)

filtered_df = df[df["vectorId"] == selected_vector]

# =============================
# Main display
# =============================

st.subheader("Monthly Evolution")

st.line_chart(
    filtered_df.set_index("date")["value"]
)

st.subheader("Raw Data")

st.dataframe(filtered_df.sort_values("date", ascending=False))
