import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.load_data import load_matches
from utils.load_data import load_deliveries

# -------------------------------
# Load Data
# -------------------------------

matches = load_matches()
deliveries = load_deliveries()

st.title("🏟 Venue Analysis")

st.write("Venue-wise IPL statistics")

st.divider()

# -------------------------------
# Venue Filter
# -------------------------------

venues = sorted(matches["venue"].unique())

selected_venue = st.selectbox(
    "Select Venue",
    venues
)

# -------------------------------
# Matches Played
# -------------------------------

venue_matches = matches[
    matches["venue"] == selected_venue
]

st.subheader("Venue Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Matches",
        len(venue_matches)
    )

with col2:
    st.metric(
        "Teams Played",
        len(
            pd.concat([
                venue_matches["team1"],
                venue_matches["team2"]
            ]).unique()
        )
    )

with col3:
    st.metric(
        "Winners",
        venue_matches["winner"].nunique()
    )

st.divider()

# -------------------------------
# Top Venues
# -------------------------------

st.subheader("Top 10 Venues")

top_venues = matches["venue"].value_counts()

fig, ax = plt.subplots(figsize=(12,6))

top_venues.head(10).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Venue")
ax.set_ylabel("Matches")

plt.xticks(rotation=75)

st.pyplot(fig)

plt.close()

# -------------------------------
# Most Successful Team
# -------------------------------

st.subheader("Most Successful Team")

wins = venue_matches["winner"].value_counts()

if len(wins) > 0:

    st.success(
        f"{wins.index[0]} won {wins.iloc[0]} matches here."
    )

else:

    st.warning("No winner data available.")

# -------------------------------
# First Innings Average
# -------------------------------

merged = deliveries.merge(
    matches[["id","venue"]],
    left_on="match_id",
    right_on="id"
)

venue_data = merged[
    merged["venue"] == selected_venue
]

innings = venue_data.groupby(
    ["match_id","inning"]
)["total_runs"].sum().reset_index()

first = innings[
    innings["inning"] == 1
]

second = innings[
    innings["inning"] == 2
]

avg_first = first["total_runs"].mean()

avg_second = second["total_runs"].mean()

col1,col2 = st.columns(2)

with col1:

    st.metric(
        "Average First Innings",
        f"{avg_first:.2f}"
    )

with col2:

    st.metric(
        "Average Second Innings",
        f"{avg_second:.2f}"
    )

st.divider()

# -------------------------------
# Average Scores by Venue
# -------------------------------

st.subheader("Average Score")

fig,ax=plt.subplots(figsize=(5,5))

ax.bar(
    ["First","Second"],
    [avg_first,avg_second]
)

ax.set_ylabel("Runs")

st.pyplot(fig)

plt.close()

# -------------------------------
# Venue Match History
# -------------------------------

st.subheader("Match History")

st.dataframe(
    venue_matches
)