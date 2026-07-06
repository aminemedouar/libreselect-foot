import pandas as pd
import streamlit as st

from ai_tactics_engine import MatchReport, MatchSimulator, Player, TacticsRecommendationEngine, Team
from national_teams_db import get_team, list_countries


@st.cache_data
def build_players(country_name: str) -> list[Player]:
    team_data = get_team(country_name)
    return [
        Player(
            name=player["name"],
            position=player["pos"],
            pace=player["pace"],
            passing=player["pass"],
            dribbling=player["drib"],
            shooting=player["shoot"],
            defense=player["def"],
            physical=player["phys"],
            country=country_name,
            overall=player["rating"],
        )
        for player in team_data["players"]
    ]


@st.cache_data
def build_team(country_name: str) -> Team:
    team_data = get_team(country_name)
    return Team(
        name=country_name,
        players=build_players(country_name),
        formation=team_data["formation"],
    )


def players_dataframe(players: list[Player]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Joueur": player.name,
                "Poste": player.position,
                "Note": player.overall,
                "Vitesse": player.pace,
                "Passe": player.passing,
                "Dribble": player.dribbling,
                "Tir": player.shooting,
                "Défense": player.defense,
                "Physique": player.physical,
            }
            for player in players
        ]
    )


st.set_page_config(page_title="LibreSelect Foot", page_icon="⚽", layout="wide")

countries = list_countries()

st.title("⚽ LibreSelect Foot")
st.markdown("**Optimiseur IA de sélections nationales**")
st.caption("Choisis un pays, analyse l'adversaire et lance une simulation tactique.")

selected_country = st.selectbox("Sélection à optimiser", countries, index=0)
available_opponents = [country for country in countries if country != selected_country]
selected_opponent = st.selectbox("Adversaire à analyser", available_opponents, index=0)

selected_team = build_team(selected_country)
opponent_team = build_team(selected_opponent)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Effectif disponible")
    st.dataframe(
        players_dataframe(selected_team.players).sort_values(["Poste", "Note"], ascending=[True, False]),
        use_container_width=True,
        hide_index=True,
    )

with right_col:
    st.subheader("Adversaire")
    st.dataframe(
        players_dataframe(opponent_team.players).sort_values(["Poste", "Note"], ascending=[True, False]),
        use_container_width=True,
        hide_index=True,
    )

if st.button("🚀 Lancer l'analyse IA", type="primary"):
    with st.spinner("Simulation des tactiques en cours..."):
        engine = TacticsRecommendationEngine(selected_team.players)
        recommendation = engine.recommend_tactic(opponent_team)
        simulated_team = Team(
            name=selected_team.name,
            players=recommendation["recommended_selection"],
            formation=recommendation["recommended_formation"],
        )
        simulator = MatchSimulator(simulated_team, opponent_team)
        home_score, away_score, events = simulator.simulate()

    st.success("Analyse terminée.")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Formation recommandée", recommendation["recommended_formation"])
    metric_col2.metric("Tactique recommandée", recommendation["recommended_tactic"])
    metric_col3.metric(
        "Probabilité de victoire",
        f"{recommendation['expected_win_probability'] * 100:.1f}%",
    )

    st.subheader("Lecture de l'adversaire")
    opponent_analysis = recommendation["opponent_analysis"]
    st.write(
        {
            "Style estimé": opponent_analysis["style"],
            "Attaque moyenne": round(opponent_analysis["avg_attack"], 1),
            "Défense moyenne": round(opponent_analysis["avg_defense"], 1),
            "Vitesse moyenne": round(opponent_analysis["avg_pace"], 1),
        }
    )

    st.subheader("Sélection recommandée")
    st.dataframe(
        players_dataframe(recommendation["recommended_selection"]).sort_values(
            ["Poste", "Note"], ascending=[True, False]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Conseils tactiques")
    st.text(recommendation["tactical_advice"])

    st.subheader("Match simulé")
    st.text(
        MatchReport.generate(
            simulated_team,
            opponent_team,
            home_score,
            away_score,
            events,
            recommendation,
        )
    )
