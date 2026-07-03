#!/usr/bin/env python3
"""
LibreSelect Foot v0.4 - Version Professionnelle
Interface sérieuse, multi-pays, extensible.

Créé avec passion par un Franco-Algérien pour la FAF 
et tous les pays qui veulent progresser sérieusement.
"""

import streamlit as st
import random
from collections import defaultdict

st.set_page_config(
    page_title="LibreSelect Foot v0.4",
    page_icon="⚽",
    layout="wide"
)

# ==================== DONNÉES PAR PAYS ====================

def get_players_by_country():
    players = {
        "France": [
            {"name": "Mike Maignan", "pos": "GK", "overall": 85},
            {"name": "Theo Hernandez", "pos": "DEF", "overall": 84},
            {"name": "William Saliba", "pos": "DEF", "overall": 86},
            {"name": "Dayot Upamecano", "pos": "DEF", "overall": 82},
            {"name": "Jules Koundé", "pos": "DEF", "overall": 83},
            {"name": "Aurélien Tchouaméni", "pos": "MID", "overall": 85},
            {"name": "Eduardo Camavinga", "pos": "MID", "overall": 84},
            {"name": "Warren Zaïre-Emery", "pos": "MID", "overall": 81},
            {"name": "Adrien Rabiot", "pos": "MID", "overall": 80},
            {"name": "Kylian Mbappé", "pos": "FWD", "overall": 91},
            {"name": "Ousmane Dembélé", "pos": "FWD", "overall": 83},
            {"name": "Antoine Griezmann", "pos": "FWD", "overall": 82},
            {"name": "Bradley Barcola", "pos": "FWD", "overall": 80},
        ],
        "Algérie": [
            {"name": "Riyad Mahrez", "pos": "FWD", "overall": 85},
            {"name": "Ismaël Bennacer", "pos": "MID", "overall": 82},
            {"name": "Sofiane Feghouli", "pos": "MID", "overall": 79},
            {"name": "Youcef Atal", "pos": "DEF", "overall": 78},
            {"name": "Aïssa Mandi", "pos": "DEF", "overall": 80},
            {"name": "Houssem Aouar", "pos": "MID", "overall": 81},
            {"name": "Mohamed El Amine Amoura", "pos": "FWD", "overall": 79},
            {"name": "Andy Delort", "pos": "FWD", "overall": 78},
        ],
        "Brésil": [
            {"name": "Alisson", "pos": "GK", "overall": 89},
            {"name": "Marquinhos", "pos": "DEF", "overall": 85},
            {"name": "Thiago Silva", "pos": "DEF", "overall": 84},
            {"name": "Casemiro", "pos": "MID", "overall": 86},
            {"name": "Neymar", "pos": "FWD", "overall": 89},
            {"name": "Vinicius Jr", "pos": "FWD", "overall": 87},
            {"name": "Rodrygo", "pos": "FWD", "overall": 83},
        ],
        "Argentine": [
            {"name": "Emiliano Martínez", "pos": "GK", "overall": 86},
            {"name": "Nicolás Otamendi", "pos": "DEF", "overall": 81},
            {"name": "Rodrigo De Paul", "pos": "MID", "overall": 82},
            {"name": "Enzo Fernández", "pos": "MID", "overall": 84},
            {"name": "Lionel Messi", "pos": "FWD", "overall": 91},
            {"name": "Julián Álvarez", "pos": "FWD", "overall": 83},
        ],
    }
    return players

# ==================== INTERFACE ====================

st.title("LibreSelect Foot v0.4")
st.markdown("**Outil professionnel de sélection nationale** — Open Source")

countries = list(get_players_by_country().keys())
selected_country = st.selectbox("Choisir un pays", countries, index=0)

players = get_players_by_country()[selected_country]

st.subheader(f"Pool de joueurs — {selected_country}")

# Affichage simple des joueurs
for p in players:
    st.write(f"- {p['name']} ({p['pos']}) — {p['overall']}")

st.divider()

# Simulation basique d'optimisation
if st.button("Lancer l'optimisation IA"):
    st.success(f"Optimisation terminée pour {selected_country} !")
    st.write("Meilleure sélection simulée (version simplifiée v0.4) :")
    best = random.sample(players, min(11, len(players)))
    for p in best:
        st.write(f"• {p['name']} ({p['pos']})")

st.divider()

# Message personnel (Franco-Algérien pour la FAF et la FFF)
st.markdown("---")
st.markdown(
    "**Créé par un Franco-Algérien pour la FAF et la FFF** — au service du football des deux rives. "
    "Open source, sérieux, et fait pour progresser."
)

st.caption("v0.4 — Version professionnelle | extensible à tous les pays du monde")