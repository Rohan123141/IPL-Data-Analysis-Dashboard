import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_deliveries

deliveries = load_deliveries()

st.title("🏏 Batting Analytics")

st.markdown(
    "League-wide batting statistics and rankings."
)

st.divider()
st.subheader("🏆 Top 10 Batsmen")

runs = deliveries.groupby(
    "batsman"
)["batsman_runs"].sum().reset_index()

runs = runs.rename(
    columns={"batsman_runs":"Runs"}
)

runs = runs.sort_values(
    "Runs",
    ascending=False
)

fig = px.bar(
    runs.head(10),
    x="batsman",
    y="Runs",
    color="Runs",
    title="Top 10 Run Scorers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("⚡ Highest Strike Rate")

legal = deliveries[
    deliveries["wide_runs"] == 0
]

runs = legal.groupby(
    "batsman"
)["batsman_runs"].sum()

balls = legal.groupby(
    "batsman"
).size()

strike = (
    runs / balls
) * 100

stats = pd.DataFrame({

    "Runs":runs,

    "Balls":balls,

    "Strike Rate":strike

})

stats = stats[
    stats["Balls"] >= 500
]

stats = stats.sort_values(
    "Strike Rate",
    ascending=False
)

fig = px.bar(

    stats.head(10),

    y=stats.head(10).index,

    x="Strike Rate",

    orientation="h",

    color="Strike Rate",

    title="Highest Strike Rate"

)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("🏏 Best Batting Average")

runs = deliveries.groupby(
    "batsman"
)["batsman_runs"].sum()

outs = deliveries[
    deliveries["player_dismissed"].notna()
]["player_dismissed"].value_counts()

stats = pd.DataFrame({

    "Runs":runs,

    "Outs":outs

}).fillna(0)

stats = stats[
    stats["Runs"] >= 1000
]

stats = stats[
    stats["Outs"] > 0
]

stats["Average"] = (

    stats["Runs"] /

    stats["Outs"]

)

stats = stats.sort_values(

    "Average",

    ascending=False

)

fig = px.bar(

    stats.head(10),

    y=stats.head(10).index,

    x="Average",

    orientation="h",

    color="Average",

    title="Highest Batting Average"

)

st.plotly_chart(

    fig,

    use_container_width=True

)
st.subheader("💥 Most Sixes")

sixes = deliveries[
    deliveries["batsman_runs"]==6
]

top = sixes[
    "batsman"
].value_counts().reset_index()

top.columns=[
    "Player",
    "Sixes"
]

fig = px.bar(

    top.head(10),

    x="Player",

    y="Sixes",

    color="Sixes",

    title="Most Sixes"

)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("🏏 Most Fours")

fours = deliveries[
    deliveries["batsman_runs"]==4
]

top = fours[
    "batsman"
].value_counts().reset_index()

top.columns=[
    "Player",
    "Fours"
]

fig = px.bar(

    top.head(10),

    x="Player",

    y="Fours",

    color="Fours",

    title="Most Fours"

)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("📊 Run Distribution")

distribution = deliveries[
    "batsman_runs"
].value_counts().sort_index()

distribution = distribution.reset_index()

distribution.columns=[

    "Runs",

    "Frequency"

]

fig = px.bar(

    distribution,

    x="Runs",

    y="Frequency",

    color="Frequency",

    title="Run Distribution"

)

st.plotly_chart(

    fig,

    use_container_width=True

)
st.subheader("🔥 Highest Individual Scores")

scores = deliveries.groupby(

    ["match_id","batsman"]

)["batsman_runs"].sum().reset_index()

scores = scores.sort_values(

    "batsman_runs",

    ascending=False

)

fig = px.bar(

    scores.head(10),

    x="batsman",

    y="batsman_runs",

    color="batsman_runs",

    title="Highest Individual Scores"

)

st.plotly_chart(

    fig,

    use_container_width=True

)
