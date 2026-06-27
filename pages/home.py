import streamlit as st

from utils.load_data import load_matches
from utils.load_data import load_deliveries


matches = load_matches()
deliveries = load_deliveries()

st.title("🏠 Home")

st.write(
    """
Welcome to the IPL Dashboard.

This dashboard analyzes IPL matches from multiple seasons.

Use the sidebar to navigate through different sections.
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Matches",
        len(matches)
    )

with col2:
    st.metric(
        "Total Teams",
        matches["winner"].nunique()
    )

with col3:
    st.metric(
        "Total Players",
        deliveries["batsman"].nunique()
    )

with col4:
    st.metric(
        "Total Venues",
        matches["venue"].nunique()
    )

st.divider()

st.subheader("Dataset Preview")

st.dataframe(matches.head(10))

st.divider()

st.subheader("Matches Per Season")

season = matches.groupby("season").size()

st.line_chart(season)