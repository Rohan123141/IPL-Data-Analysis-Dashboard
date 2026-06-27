import streamlit as st

st.set_page_config(
    page_title="IPL Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏏 IPL Data Analysis Dashboard")

st.markdown("""
Welcome to the **IPL Data Analysis Dashboard**.

👈 Use the **sidebar** to navigate between different analysis pages.

This project includes:

- 👥 Team Analysis
- 🏏 Player Analysis
- 🏟 Venue Analysis
- 📅 Season Analysis
- 🏏 Batting Analysis
- 🎯 Bowling Analysis
""")