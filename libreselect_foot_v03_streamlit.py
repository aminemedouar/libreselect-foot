import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from ai_tactics_engine import (
    MatchSimulator,
    Player,
    Tactic,
    Team,
    TacticsRecommendationEngine,
)
from national_teams_db import NATIONAL_TEAMS, list_countries


st.set_page_config(
    page_title="LibreSelect Foot v0.3",
    page_icon="⚽",
    layout="wide",
)


def _players_from_country(country_name: str) -> list[Player]:
    team_data = NATIONAL_TEAMS[country_name]
    return [
        Player(
            name=p["name"],
            position=p["pos"],
            pace=p["pace"],
            passing=p["pass"],
            dribbling=p["drib"],
            shooting=p["shoot"],
            defense=p["def"],
            physical=p["phys"],
            country=country_name,
            overall=p["rating"],
        )
        for p in team_data["players"]
    ]


def _best_eleven(players: list[Player]) -> list[Player]:
    return sorted(players, key=lambda p: p.overall, reverse=True)[:11]


def _build_team(country_name: str, tactic: Tactic | None = None) -> Team:
    players = _best_eleven(_players_from_country(country_name))
    formation = tactic.formation if tactic else NATIONAL_TEAMS[country_name]["formation"]
    return Team(name=country_name, players=players, formation=formation, tactic=tactic)


def _players_table(players: list[Player]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Joueur": p.name,
                "Poste": p.position,
                "OVR": p.overall,
                "Pace": p.pace,
                "Pass": p.passing,
                "Dribble": p.dribbling,
                "Shoot": p.shooting,
                "Def": p.defense,
                "Phys": p.physical,
            }
            for p in sorted(players, key=lambda x: x.overall, reverse=True)
        ]
    )


def _simulate_series(home_team: Team, away_team: Team, n_matches: int) -> dict:
    wins = draws = losses = 0
    home_goals = away_goals = 0

    for i in range(n_matches):
        sim = MatchSimulator(home_team=home_team, away_team=away_team, seed=100 + i)
        hs, as_, _ = sim.simulate()
        home_goals += hs
        away_goals += as_
        if hs > as_:
            wins += 1
        elif hs < as_:
            losses += 1
        else:
            draws += 1

    return {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "avg_home_goals": home_goals / n_matches,
        "avg_away_goals": away_goals / n_matches,
    }


st.title("⚽ LibreSelect Foot — Test des tactiques")
st.caption("Simule et compare des tactiques nationales avec le moteur IA LibreSelect.")

all_countries = list_countries()

with st.sidebar:
    st.header("🎛️ Paramètres")
    home_country = st.selectbox("Sélection nationale", all_countries, index=0)
    default_away = 1 if len(all_countries) > 1 else 0
    away_country = st.selectbox("Adversaire", all_countries, index=default_away)

    if home_country == away_country:
        st.warning("Choisis deux pays différents.")

    n_sims = st.slider("Nombre de simulations", min_value=3, max_value=30, value=10)

engine = TacticsRecommendationEngine(_players_from_country(home_country))
opponent_team = _build_team(away_country)

tab1, tab2, tab3 = st.tabs(
    [
        "🧬 Optimisation IA",
        "⚔️ Test tactique manuel",
        "📊 Comparateur tactiques",
    ]
)

with tab1:
    st.subheader("Recommandation IA contre l'adversaire")
    if st.button("Lancer l'analyse IA", type="primary", disabled=home_country == away_country):
        recommendation = engine.recommend_tactic(opponent_team)

        c1, c2, c3 = st.columns(3)
        c1.metric("Formation recommandée", recommendation["recommended_formation"])
        c2.metric("Tactique recommandée", recommendation["recommended_tactic"])
        c3.metric(
            "Probabilité de victoire",
            f"{recommendation['expected_win_probability'] * 100:.1f}%",
        )

        st.markdown("### 🔍 Analyse de l'adversaire")
        analysis = recommendation["opponent_analysis"]
        st.write(
            {
                "Attaque moyenne": round(analysis["avg_attack"], 2),
                "Défense moyenne": round(analysis["avg_defense"], 2),
                "Vitesse moyenne": round(analysis["avg_pace"], 2),
                "Style détecté": analysis["style"],
            }
        )

        st.markdown("### ✅ Sélection recommandée")
        st.dataframe(_players_table(recommendation["recommended_selection"]), use_container_width=True)

        st.markdown("### 💡 Conseil tactique")
        st.info(recommendation["tactical_advice"])

with tab2:
    st.subheader("Tester une tactique précise")
    tactic_names = [t.name for t in TacticsRecommendationEngine.TACTICS]
    chosen_name = st.selectbox("Tactique à tester", tactic_names)
    chosen_tactic = next(t for t in TacticsRecommendationEngine.TACTICS if t.name == chosen_name)

    if st.button("Simuler cette tactique", disabled=home_country == away_country):
        home_team = _build_team(home_country, chosen_tactic)
        series = _simulate_series(home_team, opponent_team, n_sims)

        a, b, c = st.columns(3)
        a.metric("Victoires", series["wins"])
        b.metric("Nuls", series["draws"])
        c.metric("Défaites", series["losses"])

        st.write(
            {
                f"Buts moyens {home_country}": round(series["avg_home_goals"], 2),
                f"Buts moyens {away_country}": round(series["avg_away_goals"], 2),
            }
        )

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(["Victoires", "Nuls", "Défaites"], [series["wins"], series["draws"], series["losses"]])
        ax.set_title(f"Résultats sur {n_sims} matchs")
        st.pyplot(fig)

        st.markdown("### 📜 Exemple d'événements de match")
        demo_sim = MatchSimulator(home_team=home_team, away_team=opponent_team, seed=42)
        hs, as_, events = demo_sim.simulate()
        st.write(f"Score exemple: **{home_country} {hs} - {as_} {away_country}**")
        st.text("\n".join(events[:25]) if events else "Aucun événement notable.")

with tab3:
    st.subheader("Classement des tactiques disponibles")
    if st.button("Comparer toutes les tactiques", disabled=home_country == away_country):
        rows = []
        for tactic in TacticsRecommendationEngine.TACTICS:
            team = _build_team(home_country, tactic)
            result = _simulate_series(team, opponent_team, n_sims)
            win_rate = result["wins"] / n_sims
            rows.append(
                {
                    "Tactique": tactic.name,
                    "Formation": tactic.formation,
                    "Style": tactic.style,
                    "Win rate": round(win_rate * 100, 1),
                    "V": result["wins"],
                    "N": result["draws"],
                    "D": result["losses"],
                }
            )

        ranking_df = pd.DataFrame(rows).sort_values("Win rate", ascending=False).reset_index(drop=True)
        st.dataframe(ranking_df, use_container_width=True)
        st.success(f"Meilleure tactique actuelle: {ranking_df.iloc[0]['Tactique']}")
