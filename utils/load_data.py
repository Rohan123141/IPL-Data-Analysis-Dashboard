import pandas as pd
import streamlit as st


@st.cache_data
def load_matches():
    return pd.read_csv("data/matches.csv")


@st.cache_data
def load_deliveries():
    return pd.read_csv("data/deliveries.csv")