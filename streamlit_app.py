from itertools import combinations

import pandas as pd
import streamlit as st

from ai_tactics_engine import MatchReport, MatchSimulator, Player, TacticsRecommendationEngine, Team
from national_teams_db import get_team, list_countries


@st.cache_data
def build_players(country_name: str) -> list[Player]:
    team_data = get_team(country_name)
    if team_data is None:
        return []

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
def build_team(country_name: str) -> Team | None:
    team_data = get_team(country_name)
    if team_data is None:
        return None

    return Team(
        name=country_name,
        players=build_players(country_name),
        formation=team_data["formation"],
    )


def clone_team(country_name: str, tactic_name: str | None = None) -> Team:
    base_team = build_team(country_name)
    if base_team is None:
        raise ValueError(f"Équipe introuvable: {country_name}")

    tactic = next(
        (candidate for candidate in TacticsRecommendationEngine.TACTICS if candidate.name == tactic_name),
        None,
    )

    return Team(
        name=base_team.name,
        players=list(base_team.players),
        formation=tactic.formation if tactic else base_team.formation,
        tactic=tactic,
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


def sorted_players_dataframe(players: list[Player]) -> pd.DataFrame:
    return players_dataframe(players).sort_values(["Poste", "Note"], ascending=[True, False])


def team_profile(team: Team) -> dict[str, float]:
    return {
        "Note moyenne": round(team.overall_rating, 1),
        "Vitesse": round(sum(player.pace for player in team.players) / len(team.players), 1),
        "Passe": round(sum(player.passing for player in team.players) / len(team.players), 1),
        "Dribble": round(sum(player.dribbling for player in team.players) / len(team.players), 1),
        "Tir": round(sum(player.shooting for player in team.players) / len(team.players), 1),
        "Défense": round(sum(player.defense for player in team.players) / len(team.players), 1),
        "Physique": round(sum(player.physical for player in team.players) / len(team.players), 1),
    }


def team_profile_chart(team: Team) -> pd.DataFrame:
    profile = team_profile(team)
    return pd.DataFrame({"Valeur": list(profile.values())[1:]}, index=list(profile.keys())[1:])


def position_distribution(team: Team) -> pd.DataFrame:
    counts = (
        players_dataframe(team.players)["Poste"]
        .value_counts()
        .reindex(["GK", "DEF", "MID", "FWD"], fill_value=0)
    )
    return counts.to_frame(name="Joueurs")


@st.cache_data
def list_all_players() -> pd.DataFrame:
    all_rows = []
    for country in list_countries():
        for player in build_players(country):
            all_rows.append(
                {
                    "Pays": country,
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
            )
    return pd.DataFrame(all_rows)


def simulate_match_result(
    home_country: str,
    away_country: str,
    home_tactic_name: str | None = None,
    away_tactic_name: str | None = None,
    seed: int | None = None,
) -> tuple[Team, Team, int, int, list[str]]:
    home_team = clone_team(home_country, home_tactic_name)
    away_team = clone_team(away_country, away_tactic_name)
    simulator = MatchSimulator(home_team, away_team, seed=seed)
    home_score, away_score, events = simulator.simulate()
    return home_team, away_team, home_score, away_score, events


def resolve_knockout_winner(home_team: Team, away_team: Team, home_score: int, away_score: int) -> tuple[str, str]:
    if home_score > away_score:
        return home_team.name, "Victoire dans le temps réglementaire"
    if away_score > home_score:
        return away_team.name, "Victoire dans le temps réglementaire"

    home_shootout_score = round(
        sum(player.shooting + player.physical for player in home_team.players) / len(home_team.players),
        2,
    )
    away_shootout_score = round(
        sum(player.shooting + player.physical for player in away_team.players) / len(away_team.players),
        2,
    )

    if home_shootout_score >= away_shootout_score:
        return home_team.name, "Victoire aux tirs au but"
    return away_team.name, "Victoire aux tirs au but"


def simulate_tournament(country_names: list[str], seed: int | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    standings = {
        country: {
            "Équipe": country,
            "MJ": 0,
            "V": 0,
            "N": 0,
            "D": 0,
            "BP": 0,
            "BC": 0,
            "Diff": 0,
            "Pts": 0,
        }
        for country in country_names
    }
    match_seed = seed or 0

    for home_country, away_country in combinations(country_names, 2):
        home_team, away_team, home_score, away_score, _ = simulate_match_result(
            home_country,
            away_country,
            seed=match_seed,
        )
        match_seed += 1

        home_row = standings[home_country]
        away_row = standings[away_country]
        home_row["MJ"] += 1
        away_row["MJ"] += 1
        home_row["BP"] += home_score
        home_row["BC"] += away_score
        away_row["BP"] += away_score
        away_row["BC"] += home_score

        if home_score > away_score:
            home_row["V"] += 1
            home_row["Pts"] += 3
            away_row["D"] += 1
        elif away_score > home_score:
            away_row["V"] += 1
            away_row["Pts"] += 3
            home_row["D"] += 1
        else:
            home_row["N"] += 1
            away_row["N"] += 1
            home_row["Pts"] += 1
            away_row["Pts"] += 1

    standings_df = pd.DataFrame(standings.values())
    standings_df["Diff"] = standings_df["BP"] - standings_df["BC"]
    standings_df = standings_df.sort_values(
        ["Pts", "Diff", "BP", "Équipe"], ascending=[False, False, False, True]
    ).reset_index(drop=True)

    semifinalists = standings_df.head(4)["Équipe"].tolist()
    knockout_rows = []

    semi_1 = simulate_match_result(semifinalists[0], semifinalists[3], seed=match_seed)
    match_seed += 1
    semi_1_winner, semi_1_decision = resolve_knockout_winner(*semi_1[:2], semi_1[2], semi_1[3])
    knockout_rows.append(
        {
            "Tour": "Demi-finale 1",
            "Match": f"{semi_1[0].name} vs {semi_1[1].name}",
            "Score": f"{semi_1[2]} - {semi_1[3]}",
            "Vainqueur": semi_1_winner,
            "Décision": semi_1_decision,
        }
    )

    semi_2 = simulate_match_result(semifinalists[1], semifinalists[2], seed=match_seed)
    match_seed += 1
    semi_2_winner, semi_2_decision = resolve_knockout_winner(*semi_2[:2], semi_2[2], semi_2[3])
    knockout_rows.append(
        {
            "Tour": "Demi-finale 2",
            "Match": f"{semi_2[0].name} vs {semi_2[1].name}",
            "Score": f"{semi_2[2]} - {semi_2[3]}",
            "Vainqueur": semi_2_winner,
            "Décision": semi_2_decision,
        }
    )

    final_match = simulate_match_result(semi_1_winner, semi_2_winner, seed=match_seed)
    final_winner, final_decision = resolve_knockout_winner(*final_match[:2], final_match[2], final_match[3])
    knockout_rows.append(
        {
            "Tour": "Finale",
            "Match": f"{final_match[0].name} vs {final_match[1].name}",
            "Score": f"{final_match[2]} - {final_match[3]}",
            "Vainqueur": final_winner,
            "Décision": final_decision,
        }
    )

    return standings_df, pd.DataFrame(knockout_rows)


def render_overview(countries: list[str]) -> None:
    all_players = list_all_players()
    average_rating = round(all_players["Note"].mean(), 1) if not all_players.empty else 0.0
    st.subheader("Vue d'ensemble")
    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Sélections", len(countries))
    metric_2.metric("Joueurs disponibles", len(all_players))
    metric_3.metric("Note moyenne globale", average_rating)
    st.caption("Explore les joueurs, optimise une sélection, simule des matchs et lance un mini-tournoi.")


def render_players_tab(countries: list[str]) -> None:
    st.subheader("🏟️ Base de joueurs")
    all_players = list_all_players()
    selected_countries = st.multiselect("Pays", countries, default=countries[:3])
    positions = st.multiselect("Postes", ["GK", "DEF", "MID", "FWD"], default=["GK", "DEF", "MID", "FWD"])
    min_rating = st.slider("Note minimum", min_value=0, max_value=100, value=80)

    filtered = all_players[
        all_players["Pays"].isin(selected_countries)
        & all_players["Poste"].isin(positions)
        & (all_players["Note"] >= min_rating)
    ].sort_values(["Note", "Pays"], ascending=[False, True])

    st.dataframe(filtered, width="stretch", hide_index=True)

    if not filtered.empty:
        st.bar_chart(filtered.groupby("Pays")["Note"].mean().sort_values(ascending=False))


def render_optimization_tab(countries: list[str]) -> None:
    st.subheader("🧬 Optimisation IA")
    selected_country = st.selectbox("Sélection à optimiser", countries, key="opt_country")
    available_opponents = [country for country in countries if country != selected_country]
    selected_opponent = st.selectbox("Adversaire à analyser", available_opponents, key="opt_opponent")

    selected_team = clone_team(selected_country)
    opponent_team = clone_team(selected_opponent)

    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("**Effectif disponible**")
        st.dataframe(sorted_players_dataframe(selected_team.players), width="stretch", hide_index=True)
    with right_col:
        st.markdown("**Profil adverse**")
        st.dataframe(sorted_players_dataframe(opponent_team.players), width="stretch", hide_index=True)

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

        st.json(
            {
                "Style estimé": recommendation["opponent_analysis"]["style"],
                "Attaque moyenne": round(recommendation["opponent_analysis"]["avg_attack"], 1),
                "Défense moyenne": round(recommendation["opponent_analysis"]["avg_defense"], 1),
                "Vitesse moyenne": round(recommendation["opponent_analysis"]["avg_pace"], 1),
            }
        )
        st.markdown("**Sélection recommandée**")
        st.dataframe(
            sorted_players_dataframe(recommendation["recommended_selection"]),
            width="stretch",
            hide_index=True,
        )
        st.markdown("**Conseils tactiques**")
        st.text(recommendation["tactical_advice"])
        st.markdown("**Match simulé**")
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


def render_match_tab(countries: list[str]) -> None:
    st.subheader("⚔️ Simulateur de match")
    home_country = st.selectbox("Équipe à domicile", countries, key="match_home")
    away_country = st.selectbox(
        "Équipe à l'extérieur",
        [country for country in countries if country != home_country],
        key="match_away",
    )
    tactic_names = [tactic.name for tactic in TacticsRecommendationEngine.TACTICS]
    home_tactic = st.selectbox("Tactique domicile", ["Tactique par défaut"] + tactic_names, key="home_tactic")
    away_tactic = st.selectbox("Tactique extérieur", ["Tactique par défaut"] + tactic_names, key="away_tactic")
    seed = st.number_input("Seed de simulation", min_value=0, value=7, step=1)

    if st.button("🎮 Simuler le match"):
        home_team, away_team, home_score, away_score, events = simulate_match_result(
            home_country,
            away_country,
            None if home_tactic == "Tactique par défaut" else home_tactic,
            None if away_tactic == "Tactique par défaut" else away_tactic,
            int(seed),
        )

        score_col1, score_col2, score_col3 = st.columns(3)
        score_col1.metric(home_team.name, home_score)
        score_col2.metric("Score final", f"{home_score} - {away_score}")
        score_col3.metric(away_team.name, away_score)

        st.markdown("**Rapport complet**")
        st.text(MatchReport.generate(home_team, away_team, home_score, away_score, events))


def render_tournament_tab(countries: list[str]) -> None:
    st.subheader("🏆 Tournoi complet")
    selected_countries = st.multiselect(
        "Sélections engagées",
        countries,
        default=countries[:4],
        max_selections=min(8, len(countries)),
    )
    seed = st.number_input("Seed du tournoi", min_value=0, value=21, step=1, key="tournament_seed")

    if len(selected_countries) < 4:
        st.info("Choisis au moins 4 sélections pour lancer le tournoi.")
        return

    if st.button("🏁 Lancer le tournoi"):
        standings_df, knockout_df = simulate_tournament(selected_countries, int(seed))
        st.markdown("**Classement de la phase de groupes**")
        st.dataframe(standings_df, width="stretch", hide_index=True)
        st.markdown("**Tableau final**")
        st.dataframe(knockout_df, width="stretch", hide_index=True)
        st.success(f"Champion simulé : {knockout_df.iloc[-1]['Vainqueur']}")


def render_visualizations_tab(countries: list[str]) -> None:
    st.subheader("📊 Visualisations")
    selected_country = st.selectbox("Pays à visualiser", countries, key="viz_country")
    selected_team = clone_team(selected_country)

    profile_col, position_col = st.columns(2)
    with profile_col:
        st.markdown("**Forces moyennes de l'équipe**")
        st.bar_chart(team_profile_chart(selected_team))
    with position_col:
        st.markdown("**Répartition par poste**")
        st.bar_chart(position_distribution(selected_team))

    top_players = (
        players_dataframe(selected_team.players)[["Joueur", "Note"]]
        .sort_values("Note", ascending=False)
        .head(5)
        .set_index("Joueur")
    )
    st.markdown("**Top 5 joueurs**")
    st.bar_chart(top_players)


def main() -> None:
    st.set_page_config(page_title="LibreSelect Foot", page_icon="⚽", layout="wide")

    countries = list_countries()

    st.title("⚽ LibreSelect Foot")
    st.markdown("**Optimiseur IA de Sélections nationales**")
    st.caption("Application activée : données, optimisation IA, simulation de match, tournoi et visualisations.")

    if len(countries) < 2:
        st.warning("Ajoute au moins deux sélections nationales pour lancer une analyse comparative.")
        st.stop()

    render_overview(countries)
    players_tab, optimization_tab, match_tab, tournament_tab, visualization_tab = st.tabs(
        [
            "🏟️ Base de joueurs",
            "🧬 Optimisation IA",
            "⚔️ Simulateur de match",
            "🏆 Tournoi complet",
            "📊 Visualisations",
        ]
    )

    with players_tab:
        render_players_tab(countries)
    with optimization_tab:
        render_optimization_tab(countries)
    with match_tab:
        render_match_tab(countries)
    with tournament_tab:
        render_tournament_tab(countries)
    with visualization_tab:
        render_visualizations_tab(countries)


if __name__ == "__main__":
    main()
