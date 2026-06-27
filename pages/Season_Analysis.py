import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.load_data import load_matches
from utils.load_data import load_deliveries

# --------------------------
# Load Data
# --------------------------

matches = load_matches()
deliveries = load_deliveries()

st.title("📅 Season Analysis")

st.write("Season-wise IPL Statistics")

st.divider()

# --------------------------
# Season Filter
# --------------------------

season = st.selectbox(
    "Select Season",
    sorted(matches["season"].unique())
)

season_matches = matches[
    matches["season"] == season
]

st.divider()

# --------------------------
# Metrics
# --------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Matches",
        len(season_matches)
    )

with col2:
    st.metric(
        "Teams",
        len(
            pd.concat([
                season_matches["team1"],
                season_matches["team2"]
            ]).unique()
        )
    )

with col3:
    st.metric(
        "Venues",
        season_matches["venue"].nunique()
    )

st.divider()

# --------------------------
# Matches Per Season
# --------------------------

st.subheader("Matches Played Per Season")

matches_per_season = matches.groupby(
    "season"
).size()

fig, ax = plt.subplots(figsize=(12,6))

matches_per_season.plot(
    marker="o",
    linewidth=2,
    ax=ax
)

ax.set_xlabel("Season")
ax.set_ylabel("Matches")

st.pyplot(fig)

plt.close()

# --------------------------
# Toss Decision
# --------------------------

st.subheader("Toss Decision")

decision = season_matches[
    "toss_decision"
].value_counts()

fig, ax = plt.subplots(figsize=(6,6))

decision.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

plt.close()

# --------------------------
# Season Winner
# --------------------------

st.subheader("Champion")

final_match = season_matches.sort_values(
    "date"
).tail(1)

winner = final_match[
    "winner"
].iloc[0]

st.success(
    f"🏆 Champion : {winner}"
)

# --------------------------
# Orange Cap
# --------------------------

st.subheader("Top Run Scorers")

season_ids = season_matches["id"]

season_deliveries = deliveries[
    deliveries["match_id"].isin(
        season_ids
    )
]

runs = season_deliveries.groupby(
    "batsman"
)["batsman_runs"].sum()

runs = runs.sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(12,6))

runs.head(10).plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Runs")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close()

# --------------------------
# Purple Cap
# --------------------------

st.subheader("Top Wicket Takers")

wickets = season_deliveries[
    season_deliveries[
        "dismissal_kind"
    ].notna()
]

wickets = wickets[
    ~wickets[
        "dismissal_kind"
    ].isin(
        [
            "run out",
            "retired hurt",
            "obstructing the field"
        ]
    )
]

wickets = wickets.groupby(
    "bowler"
).size()

wickets = wickets.sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(12,6))

wickets.head(10).plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Wickets")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close()

# --------------------------
# Season Match History
# --------------------------

st.subheader("Matches")

st.dataframe(
    season_matches
)