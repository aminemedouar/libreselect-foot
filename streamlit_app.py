import streamlit as st
from ai_tactics_engine import run_genetic_algorithm
from national_teams_db import get_team_players

st.set_page_config(page_title="LibreSelect Foot", page_icon="⚽", layout="wide")

st.title("⚽ LibreSelect Foot v0.3")
st.subheader("Optimiseur de Sélections Nationales avec IA")

# Sidebar
st.sidebar.header("Paramètres")
country = st.sidebar.selectbox("Pays", ["France", "Brésil", "Argentine", "Maroc", "Autre"])
num_generations = st.sidebar.slider("Générations", 10, 200, 50)

if st.button("🚀 Lancer l'Optimisation IA"):
    with st.spinner("Calcul en cours..."):
        players = get_team_players(country)
        if not players:
            st.error("Aucun joueur disponible pour ce pays pour le moment.")
        else:
            best_team = run_genetic_algorithm(players, num_generations)
            st.success("✅ Sélection optimale trouvée !")
            st.json(best_team)

st.info("Application en cours de migration vers Streamlit Cloud. Version complète bientôt !")
