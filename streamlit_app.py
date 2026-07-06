import streamlit as st

st.set_page_config(page_title="LibreSelect Foot", page_icon="⚽", layout="wide")

st.title("⚽ LibreSelect Foot")
st.markdown("**Optimiseur IA de Sélections Nationales de Football**")

st.sidebar.header("Configuration")
pays = st.sidebar.selectbox("Sélectionne ton pays", ["France", "Maroc", "Brésil", "Argentine", "Espagne"])
generations = st.sidebar.slider("Nombre de générations", 20, 100, 50)

if st.button("🚀 Lancer l'optimisation génétique"):
    st.info("Simulation en cours avec Grok AI...")
    # Simulation simple pour tester le déploiement
    st.success(f"✅ Meilleure sélection pour {pays} générée en {generations} générations !")
    st.balloons()

st.caption("App déployée avec l'aide de Grok • Version de test")
