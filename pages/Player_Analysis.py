import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import (
    load_matches,
    load_deliveries
)

matches = load_matches()
deliveries = load_deliveries()

st.title("👤 Player Profile")

st.markdown(
    "Search any IPL player and view complete career statistics."
)
players = sorted(deliveries["batsman"].unique())

selected_player = st.selectbox(
    "Select Player",
    players
)

player = deliveries[
    deliveries["batsman"] == selected_player
]
runs = player["batsman_runs"].sum()

balls = len(
    player[
        player["wide_runs"] == 0
    ]
)

dismissals = len(
    deliveries[
        deliveries["player_dismissed"] == selected_player
    ]
)

average = (
    runs / dismissals
) if dismissals > 0 else runs

strike_rate = (
    runs / balls * 100
) if balls > 0 else 0

fours = len(
    player[
        player["batsman_runs"] == 4
    ]
)

sixes = len(
    player[
        player["batsman_runs"] == 6
    ]
)

highest_score = player.groupby(
    "match_id"
)["batsman_runs"].sum().max()
col1,col2,col3,col4 = st.columns(4)

col1.metric("Runs",runs)

col2.metric("Average",f"{average:.2f}")

col3.metric(
    "Strike Rate",
    f"{strike_rate:.2f}"
)

col4.metric(
    "Highest Score",
    highest_score
)

col5,col6,col7 = st.columns(3)

col5.metric(
    "Balls Faced",
    balls
)

col6.metric(
    "Fours",
    fours
)

col7.metric(
    "Sixes",
    sixes
)
season = matches[
    ["id","season"]
]

player_runs = player.merge(
    season,
    left_on="match_id",
    right_on="id"
)
season_runs = player_runs.groupby(
    "season"
)["batsman_runs"].sum().reset_index()
fig = px.line(
    season_runs,
    x="season",
    y="batsman_runs",
    markers=True,
    title="Runs by Season"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
distribution = player[
    "batsman_runs"
].value_counts().sort_index()

distribution = distribution.reset_index()

distribution.columns = [
    "Runs",
    "Frequency"
]
fig = px.bar(
    distribution,
    x="Runs",
    y="Frequency",
    title="Run Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("Career Summary")

st.write(f"""
**Player:** {selected_player}

**Runs:** {runs}

**Average:** {average:.2f}

**Strike Rate:** {strike_rate:.2f}

**Highest Score:** {highest_score}

**Balls Faced:** {balls}
""")
st.subheader(
    "Ball by Ball Data"
)

st.dataframe(player)
