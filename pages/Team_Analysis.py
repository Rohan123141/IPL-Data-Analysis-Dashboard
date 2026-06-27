import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils.load_data import load_matches

# Load dataset
matches = load_matches()

# Page Title
st.title("👥 Team Analysis")

st.write("This page analyzes IPL team performance.")

st.divider()

# ==========================
# Team Filter
# ==========================

teams = sorted(pd.concat([matches["team1"], matches["team2"]]).unique())

selected_team = st.selectbox(
    "Select Team",
    teams
)

# ==========================
# Team Statistics
# ==========================

team_matches = matches[
    (matches["team1"] == selected_team) |
    (matches["team2"] == selected_team)
]

matches_played = len(team_matches)

matches_won = len(
    team_matches[
        team_matches["winner"] == selected_team
    ]
)

win_percentage = (
    matches_won / matches_played * 100
) if matches_played > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Matches Played",
        matches_played
    )

with col2:
    st.metric(
        "Matches Won",
        matches_won
    )

with col3:
    st.metric(
        "Win %",
        f"{win_percentage:.2f}%"
    )

st.divider()

# ==========================
# Overall Team Wins
# ==========================

st.subheader("Overall Team Wins")

team_wins = matches["winner"].value_counts()

fig, ax = plt.subplots(figsize=(12,6))

team_wins.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Teams")
ax.set_ylabel("Wins")
ax.set_title("Matches Won by Teams")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close()

# ==========================
# Toss Wins
# ==========================

st.subheader("Toss Wins")

toss = matches["toss_winner"].value_counts()

fig, ax = plt.subplots(figsize=(12,6))

toss.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Teams")
ax.set_ylabel("Toss Wins")
ax.set_title("Toss Wins by Teams")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close()

# ==========================
# Toss Decision
# ==========================

st.subheader("Toss Decision")

decision = matches["toss_decision"].value_counts()

fig, ax = plt.subplots(figsize=(6,6))

decision.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

plt.close()

# ==========================
# Team Match History
# ==========================

st.subheader(f"{selected_team} Match History")

st.dataframe(team_matches)