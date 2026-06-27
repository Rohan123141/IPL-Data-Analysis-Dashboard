import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_deliveries

deliveries = load_deliveries()

st.title("🎯 Bowling Analytics")

st.markdown("League-wide bowling statistics and rankings.")

st.divider()
st.subheader("🏆 Highest Wicket Takers")

valid = deliveries[
    deliveries["dismissal_kind"].notna()
]

valid = valid[
    ~valid["dismissal_kind"].isin(
        [
            "run out",
            "retired hurt",
            "obstructing the field"
        ]
    )
]

wickets = valid.groupby(
    "bowler"
).size().reset_index(name="Wickets")

wickets = wickets.sort_values(
    "Wickets",
    ascending=False
)

fig = px.bar(
    wickets.head(10),
    x="bowler",
    y="Wickets",
    color="Wickets",
    title="Top 10 Wicket Takers"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("💰 Best Economy Rate")

legal = deliveries[
    (deliveries["wide_runs"] == 0) &
    (deliveries["noball_runs"] == 0)
]

runs = deliveries.groupby(
    "bowler"
)["total_runs"].sum()

balls = legal.groupby(
    "bowler"
).size()

economy = runs / (balls / 6)

stats = pd.DataFrame({
    "Runs": runs,
    "Balls": balls,
    "Economy": economy
}).fillna(0)

stats = stats[
    stats["Balls"] >= 300
]

stats = stats.sort_values(
    "Economy"
)

fig = px.bar(
    stats.head(10),
    x="Economy",
    y=stats.head(10).index,
    orientation="h",
    color="Economy",
    title="Best Economy Rate"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🏏 Best Bowling Average")

stats["Wickets"] = wickets.set_index(
    "bowler"
)["Wickets"]

stats = stats.fillna(0)

stats = stats[
    stats["Wickets"] > 0
]

stats["Average"] = (
    stats["Runs"] /
    stats["Wickets"]
)

stats = stats.sort_values(
    "Average"
)

fig = px.bar(
    stats.head(10),
    x="Average",
    y=stats.head(10).index,
    orientation="h",
    color="Average",
    title="Best Bowling Average"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("⚡ Bowling Strike Rate")

stats["Strike Rate"] = (
    stats["Balls"] /
    stats["Wickets"]
)

stats = stats.sort_values(
    "Strike Rate"
)

fig = px.bar(
    stats.head(10),
    x="Strike Rate",
    y=stats.head(10).index,
    orientation="h",
    color="Strike Rate",
    title="Best Bowling Strike Rate"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("⚪ Dot Ball Percentage")

dot = legal[
    legal["total_runs"] == 0
]

dot = dot.groupby(
    "bowler"
).size()

dot_percentage = (
    dot / balls
) * 100

dot_stats = pd.DataFrame({
    "Dot %": dot_percentage
}).fillna(0)

dot_stats = dot_stats.sort_values(
    "Dot %",
    ascending=False
)

fig = px.bar(
    dot_stats.head(10),
    x="Dot %",
    y=dot_stats.head(10).index,
    orientation="h",
    color="Dot %",
    title="Highest Dot Ball Percentage"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🏏 Maiden Overs")

overs = legal.groupby(
    ["match_id", "inning", "bowler", "over"]
)["total_runs"].sum().reset_index()

maidens = overs[
    overs["total_runs"] == 0
]

maidens = maidens.groupby(
    "bowler"
).size().reset_index(name="Maidens")

maidens = maidens.sort_values(
    "Maidens",
    ascending=False
)

fig = px.bar(
    maidens.head(10),
    x="bowler",
    y="Maidens",
    color="Maidens",
    title="Most Maiden Overs"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🔥 Best Bowling Figures")

figures = valid.groupby(
    ["match_id", "bowler"]
).size().reset_index(name="Wickets")

figures = figures.sort_values(
    "Wickets",
    ascending=False
)

fig = px.bar(
    figures.head(10),
    x="bowler",
    y="Wickets",
    color="Wickets",
    title="Best Bowling Figures"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("📋 Top 20 Bowlers")

st.dataframe(
    wickets.head(20),
    use_container_width=True
)