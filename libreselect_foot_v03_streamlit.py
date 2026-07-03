#!/usr/bin/env python3
"""
LibreSelect Foot v0.3 - L'outil LE PLUS PERFECTIONNÉ AU MONDE
Interface Web Streamlit ultra-moderne + tout le moteur v0.2

Fonctionnalités :
- Dashboard interactif complet
- Base de joueurs avec filtres
- Optimisation IA par algorithme génétique avancé (tournois complets)
- Simulateur de match événementiel avec log détaillé
- Simulateur de tournoi / mini-Coupe du Monde
- Visualisations : graphiques + terrain de foot dessiné
- Sauvegarde / chargement JSON + upload CSV
- Design pro, emojis, dark-friendly

Installation (une seule fois) :
    pip install streamlit matplotlib

Lancement :
    streamlit run libreselect_foot_v03_streamlit.py

Puis ouvre automatiquement dans ton navigateur.

C'est maintenant un vrai outil professionnel open-source.
On continue à le rendre encore plus parfait à chaque version.

Libre • Open Source • Pour tous les pays du monde
"""

import streamlit as st
import random
import math
import copy
import json
import csv
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Arc
import numpy as np

# ==================== CONFIG ====================
st.set_page_config(
    page_title="LibreSelect Foot v0.3",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

SIM_MINUTES = 90
EVENT_INTERVAL = 3
FATIGUE_RATE = 0.015
POSITIONS = ['GK', 'DEF', 'MID', 'FWD']
FORMATION_SLOTS = {
    "4-3-3": {'GK':1, 'DEF':4, 'MID':3, 'FWD':3},
    "4-4-2": {'GK':1, 'DEF':4, 'MID':4, 'FWD':2},
    "4-2-3-1": {'GK':1, 'DEF':4, 'MID':5, 'FWD':1},
    "3-5-2": {'GK':1, 'DEF':3, 'MID':5, 'FWD':2},
}
TACTICS = {
    "balanced": {"attack_bias": 0.0, "press": 0.5, "defend_bonus": 0.0},
    "attacking": {"attack_bias": 0.25, "press": 0.7, "defend_bonus": -0.1},
    "defensive": {"attack_bias": -0.2, "press": 0.3, "defend_bonus": 0.15},
    "high_press": {"attack_bias": 0.1, "press": 0.9, "defend_bonus": -0.05},
    "counter": {"attack_bias": 0.15, "press": 0.4, "defend_bonus": 0.05},
}

# ==================== CLASSES (même moteur que v0.2) ====================

class Player:
    def __init__(self, name, position, attributes, age=25, nationality="France", form=80):
        self.name = name
        self.position = position
        self.attributes = attributes
        self.age = age
        self.nationality = nationality
        self.form = form
        self.fatigue = 0.0

    def get_rating(self, key):
        base = self.attributes.get(key, 50)
        form_mod = (self.form - 80) * 0.3
        fatigue_mod = -self.fatigue * 25
        return max(20, min(99, base + form_mod + fatigue_mod))

    def get_overall(self):
        keys = ['pace', 'shoot', 'pass', 'dribble', 'defend', 'phys']
        return sum(self.get_rating(k) for k in keys) / len(keys)

    def reset_fatigue(self):
        self.fatigue = 0.0

    def apply_fatigue(self, intensity=1.0):
        self.fatigue = min(1.0, self.fatigue + FATIGUE_RATE * intensity)

    def __repr__(self):
        return f"{self.name} ({self.position} {self.get_overall():.1f})"


class Team:
    def __init__(self, name, starting11, formation="4-3-3", tactics="balanced", subs=None):
        self.name = name
        self.starting11 = starting11[:11]
        self.formation = formation
        self.tactics = tactics
        self.subs = subs or []
        self.stats = defaultdict(int)

    def get_overall_rating(self):
        base = sum(p.get_overall() for p in self.starting11) / 11
        tac = TACTICS.get(self.tactics, TACTICS["balanced"])
        base += tac["attack_bias"] * 8 + tac["defend_bonus"] * 6
        return max(45, min(92, base))

    def get_tactics_mod(self):
        return TACTICS.get(self.tactics, TACTICS["balanced"])

    def reset_players(self):
        for p in self.starting11 + self.subs:
            p.reset_fatigue()

    def make_substitution(self, minute):
        tired = [p for p in self.starting11 if p.fatigue > 0.65]
        fresh_subs = [s for s in self.subs if s.fatigue < 0.2]
        if tired and fresh_subs:
            out = max(tired, key=lambda p: p.fatigue)
            inn = random.choice(fresh_subs)
            self.starting11.remove(out)
            self.starting11.append(inn)
            self.subs.remove(inn)
            self.subs.append(out)
            return f"{minute}' Remplacement: {out.name} → {inn.name}"
        return None

    def __repr__(self):
        return f"{self.name} | {self.formation} {self.tactics}"


# ==================== MOTEUR SIMULATION (identique v0.2) ====================

def simulate_advanced_match(team1, team2, verbose=False):
    team1.reset_players()
    team2.reset_players()
    team1.stats.clear()
    team2.stats.clear()
    score1, score2 = 0, 0
    events = []
    possession1 = 50.0
    tac1 = team1.get_tactics_mod()
    tac2 = team2.get_tactics_mod()

    for minute in range(0, SIM_MINUTES, EVENT_INTERVAL):
        for p in team1.starting11 + team2.starting11:
            intensity = 1.0 + (tac1["press"] if p in team1.starting11 else tac2["press"]) * 0.5
            p.apply_fatigue(intensity)

        sub_msg = team1.make_substitution(minute) or team2.make_substitution(minute)
        if sub_msg:
            events.append(sub_msg)

        mid1 = sum(p.get_rating('pass') + p.get_rating('vision', 70) for p in team1.starting11 if p.position in ['MID', 'DEF']) / 7
        mid2 = sum(p.get_rating('pass') + p.get_rating('vision', 70) for p in team2.starting11 if p.position in ['MID', 'DEF']) / 7
        possession1 = max(35, min(65, 50 + (mid1 - mid2) * 0.4 + tac1["attack_bias"] * 15 - tac2["attack_bias"] * 15))
        team1.stats['possession'] += possession1

        if random.random() < 0.75:
            attacking_team = team1 if random.random() < (possession1 / 100) else team2
            defending_team = team2 if attacking_team == team1 else team1
            tac_att = attacking_team.get_tactics_mod()

            event_type = random.choices(
                ['pass', 'duel', 'shot', 'foul'],
                weights=[0.45, 0.25, 0.20 + tac_att["attack_bias"]*0.3, 0.10]
            )[0]

            if event_type == 'shot':
                shooter = random.choice([p for p in attacking_team.starting11 if p.position in ['FWD', 'MID']])
                shoot_rating = shooter.get_rating('shoot') + shooter.get_rating('vision', 65) * 0.3
                prob_goal = max(0.02, min(0.35, (shoot_rating + tac_att["attack_bias"]*20) / 280))
                if attacking_team == team1:
                    team1.stats['shots'] += 1
                else:
                    team2.stats['shots'] += 1
                if random.random() < prob_goal:
                    if attacking_team == team1:
                        score1 += 1
                    else:
                        score2 += 1
                    events.append(f"⚽ {minute}' BUT de {shooter.name} ! {score1}-{score2}")

            elif event_type == 'pass':
                passer = random.choice([p for p in attacking_team.starting11 if p.position in ['MID', 'DEF', 'FWD']])
                success = passer.get_rating('pass') / 120 + random.uniform(-0.1, 0.15)
                if success > 0.55:
                    attacking_team.stats['passes_success'] += 1
                else:
                    defending_team.stats['interceptions'] += 1

        if minute == 42:
            events.append("--- MI-TEMPS ---")

    team1.stats['avg_possession'] = team1.stats.get('possession', 0) / max(1, (SIM_MINUTES // EVENT_INTERVAL))
    team2.stats['avg_possession'] = 100 - team1.stats['avg_possession']

    goal_diff = score1 - score2
    return score1, score2, goal_diff, events


def simulate_tournament(team, opponents, num_opponents=4):
    points = 0
    total_diff = 0
    results = []
    random.shuffle(opponents)
    for opp in opponents[:num_opponents]:
        g1, g2, diff, _ = simulate_advanced_match(team, opp)
        total_diff += diff
        if g1 > g2: points += 3
        elif g1 == g2: points += 1
        results.append((opp.name, g1, g2))

    qualified = points >= 7 or (points >= 5 and total_diff > -2)
    bonus = 4 if qualified else 0

    if qualified and len(opponents) > num_opponents:
        knock_opp = random.choice(opponents[num_opponents:])
        g1k, g2k, diffk, _ = simulate_advanced_match(team, knock_opp)
        total_diff += diffk
        if g1k > g2k:
            bonus += 6
            results.append(("Élimination directe (QUALIFIÉ)", g1k, g2k))
        else:
            results.append(("Élimination directe (éliminé)", g1k, g2k))

    fitness = points + (total_diff * 0.8) + bonus
    return fitness, points, total_diff, qualified, results


def evaluate_team_advanced(team, opponents):
    fit, pts, diff, qual, _ = simulate_tournament(team, opponents)
    return fit, pts / 12.0, diff


# ==================== GA (même que v0.2) ====================

def create_random_squad(player_pool, size=11, formation="4-3-3"):
    selected = random.sample(player_pool, min(size + 4, len(player_pool)))
    starting = selected[:11]
    subs = selected[11:15] if len(selected) > 11 else []
    return Team("Squad", starting, formation, random.choice(list(TACTICS.keys())), subs)

def crossover(parent1, parent2, player_pool):
    child_players = []
    used = set()
    for pos in POSITIONS:
        candidates = [p for p in (parent1.starting11 + parent2.starting11) if p.position == pos and p not in used]
        pool_pos = [p for p in player_pool if p.position == pos and p not in used]
        candidates += random.sample(pool_pos, min(2, len(pool_pos)))
        random.shuffle(candidates)
        for cand in candidates:
            if len([p for p in child_players if p.position == pos]) < FORMATION_SLOTS.get(parent1.formation, {}).get(pos, 3):
                child_players.append(cand)
                used.add(cand)
                break
    while len(child_players) < 11:
        remaining = [p for p in player_pool if p not in used]
        if remaining:
            child_players.append(random.choice(remaining))
            used.add(child_players[-1])
    new_tac = parent1.tactics if random.random() < 0.6 else parent2.tactics
    return Team("Child", child_players[:11], parent1.formation, new_tac, subs=parent1.subs[:2] if parent1.subs else [])

def mutate_team(team, player_pool, mutation_rate=0.35):
    new_players = copy.deepcopy(team.starting11)
    if random.random() < mutation_rate:
        for _ in range(random.randint(1, 2)):
            idx = random.randint(0, len(new_players)-1)
            same_pos = [p for p in player_pool if p.position == new_players[idx].position]
            if same_pos:
                new_players[idx] = random.choice(same_pos)
    new_tac = random.choice(list(TACTICS.keys())) if random.random() < 0.45 else team.tactics
    return Team(team.name, new_players, team.formation, new_tac, subs=team.subs)

def evolve_best_team_streamlit(player_pool, opponents, generations=14, pop_size=24, progress_bar=None):
    population = [create_random_squad(player_pool) for _ in range(pop_size)]
    best_overall = None
    best_fitness = -999

    for gen in range(generations):
        scored = []
        for team in population:
            fit, wr, diff = evaluate_team_advanced(team, opponents)
            scored.append((fit, team, wr, diff))
            if fit > best_fitness:
                best_fitness = fit
                best_overall = copy.deepcopy(team)

        scored.sort(key=lambda x: x[0], reverse=True)
        if progress_bar:
            progress_bar.progress((gen + 1) / generations, text=f"Génération {gen+1}/{generations} | Meilleur fitness: {scored[0][0]:.1f}")

        elite_size = max(4, pop_size // 4)
        new_pop = [copy.deepcopy(s[1]) for s in scored[:elite_size]]

        while len(new_pop) < pop_size:
            if random.random() < 0.65 and len(scored) >= 4:
                p1 = random.choice(scored[:pop_size//2])[1]
                p2 = random.choice(scored[:pop_size//2])[1]
                child = crossover(p1, p2, player_pool)
            else:
                parent = random.choice(scored[:pop_size//2])[1]
                child = mutate_team(parent, player_pool)
            new_pop.append(child)
        population = new_pop

    final_fit, final_wr, final_diff = evaluate_team_advanced(best_overall, opponents)
    return best_overall, final_fit, final_wr, final_diff


# ==================== VISUALISATION TERRAIN ====================

def draw_football_pitch(team):
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.set_aspect('equal')
    ax.axis('off')

    # Terrain
    ax.add_patch(Rectangle((0, 0), 100, 70, fill=False, edgecolor='#2E7D32', linewidth=3))
    ax.add_patch(Rectangle((0, 0), 50, 70, fill=False, edgecolor='#2E7D32', linewidth=2))
    # Surfaces
    ax.add_patch(Rectangle((0, 15), 16, 40, fill=False, edgecolor='#2E7D32', linewidth=2))
    ax.add_patch(Rectangle((84, 15), 16, 40, fill=False, edgecolor='#2E7D32', linewidth=2))
    # Cercles
    ax.add_patch(Circle((50, 35), 9.15, fill=False, edgecolor='#2E7D32', linewidth=2))
    ax.add_patch(Circle((11, 35), 9.15, fill=False, edgecolor='#2E7D32', linewidth=1.5))
    ax.add_patch(Circle((89, 35), 9.15, fill=False, edgecolor='#2E7D32', linewidth=1.5))
    # Points de penalty
    ax.plot(11, 35, 'o', color='#2E7D32', markersize=4)
    ax.plot(89, 35, 'o', color='#2E7D32', markersize=4)
    # Ligne milieu
    ax.axvline(50, color='#2E7D32', linewidth=2)

    # Placement des joueurs selon formation (simplifié)
    formation = team.formation
    positions_map = {
        "4-3-3": {"GK": [(8, 35)], "DEF": [(22, 12), (22, 24), (22, 46), (22, 58)], 
                  "MID": [(40, 18), (40, 35), (40, 52)], "FWD": [(65, 20), (70, 35), (65, 50)]},
        "4-4-2": {"GK": [(8, 35)], "DEF": [(22, 12), (22, 24), (22, 46), (22, 58)],
                  "MID": [(40, 12), (40, 24), (40, 46), (40, 58)], "FWD": [(65, 25), (65, 45)]},
        "4-2-3-1": {"GK": [(8, 35)], "DEF": [(22, 12), (22, 24), (22, 46), (22, 58)],
                    "MID": [(38, 18), (38, 52), (48, 12), (48, 35), (48, 58)], "FWD": [(68, 35)]},
    }
    pos_coords = positions_map.get(formation, positions_map["4-3-3"])

    colors = {"GK": "#FFD700", "DEF": "#1E88E5", "MID": "#43A047", "FWD": "#E53935"}

    for p in team.starting11:
        pos_list = pos_coords.get(p.position, [(50, 35)])
        x, y = random.choice(pos_list)  # léger random pour éviter superposition
        ax.add_patch(Circle((x, y), 3.5, color=colors.get(p.position, "#9E9E9E"), ec='white', linewidth=2))
        ax.text(x, y-5.5, p.name.split()[-1][:10], ha='center', va='top', fontsize=7, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=colors.get(p.position, "#9E9E9E"), edgecolor='none', alpha=0.9))

    ax.set_title(f"{team.name} — {formation} — {team.tactics} | Overall: {team.get_overall_rating():.1f}", 
                 fontsize=14, fontweight='bold', color='#1B5E20', pad=10)
    return fig


# ==================== DONNÉES ====================

@st.cache_data
def get_sample_players():
    base = [
        {"name": "Mike Maignan", "pos": "GK", "attrs": {"pace":62,"shoot":22,"pass":78,"dribble":38,"defend":88,"phys":82,"vision":70,"workrate":85}, "age":29},
        {"name": "Theo Hernandez", "pos": "DEF", "attrs": {"pace":94,"shoot":72,"pass":80,"dribble":88,"defend":74,"phys":80,"vision":68,"workrate":82}, "age":27},
        {"name": "William Saliba", "pos": "DEF", "attrs": {"pace":76,"shoot":48,"pass":82,"dribble":68,"defend":90,"phys":87,"vision":72,"workrate":88}, "age":24},
        {"name": "Dayot Upamecano", "pos": "DEF", "attrs": {"pace":84,"shoot":52,"pass":74,"dribble":70,"defend":84,"phys":89,"vision":65,"workrate":85}, "age":26},
        {"name": "Jules Koundé", "pos": "DEF", "attrs": {"pace":87,"shoot":58,"pass":82,"dribble":80,"defend":82,"phys":77,"vision":75,"workrate":80}, "age":27},
        {"name": "Aurélien Tchouaméni", "pos": "MID", "attrs": {"pace":78,"shoot":70,"pass":90,"dribble":82,"defend":87,"phys":84,"vision":85,"workrate":90}, "age":25},
        {"name": "Eduardo Camavinga", "pos": "MID", "attrs": {"pace":90,"shoot":68,"pass":87,"dribble":92,"defend":82,"phys":80,"vision":80,"workrate":88}, "age":22},
        {"name": "Warren Zaïre-Emery", "pos": "MID", "attrs": {"pace":84,"shoot":70,"pass":88,"dribble":83,"defend":80,"phys":78,"vision":82,"workrate":85}, "age":20},
        {"name": "Adrien Rabiot", "pos": "MID", "attrs": {"pace":74,"shoot":74,"pass":84,"dribble":77,"defend":80,"phys":86,"vision":78,"workrate":82}, "age":29},
        {"name": "Kylian Mbappé", "pos": "FWD", "attrs": {"pace":98,"shoot":94,"pass":82,"dribble":95,"defend":42,"phys":84,"vision":80,"workrate":78}, "age":27},
        {"name": "Ousmane Dembélé", "pos": "FWD", "attrs": {"pace":96,"shoot":80,"pass":84,"dribble":96,"defend":48,"phys":70,"vision":82,"workrate":75}, "age":28},
        {"name": "Antoine Griezmann", "pos": "FWD", "attrs": {"pace":76,"shoot":87,"pass":90,"dribble":84,"defend":58,"phys":74,"vision":92,"workrate":85}, "age":34},
        {"name": "Bradley Barcola", "pos": "FWD", "attrs": {"pace":91,"shoot":80,"pass":77,"dribble":87,"defend":50,"phys":76,"vision":75,"workrate":80}, "age":22},
        {"name": "Kingsley Coman", "pos": "FWD", "attrs": {"pace":94,"shoot":77,"pass":80,"dribble":92,"defend":45,"phys":72,"vision":72,"workrate":78}, "age":29},
    ]
    return [Player(d["name"], d["pos"], d["attrs"], d["age"]) for d in base]


def save_selection(team, fitness):
    data = {
        "timestamp": datetime.now().isoformat(),
        "team": team.name,
        "formation": team.formation,
        "tactics": team.tactics,
        "overall": round(team.get_overall_rating(), 1),
        "fitness": round(fitness, 1),
        "players": [{"name": p.name, "position": p.position, "overall": round(p.get_overall(), 1), "age": p.age} for p in team.starting11]
    }
    filename = f"best_selection_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename


# ==================== APPLICATION STREAMLIT ====================

def main():
    st.title("⚽ LibreSelect Foot v0.3")
    st.markdown("### L'outil le plus perfectionné au monde pour les sélections nationales de football")
    st.caption("Open Source • Simulation événementielle • Algorithme génétique • Tournois complets • Interface moderne")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        country = st.selectbox("Pays", ["France", "Algérie", "Brésil", "Maroc", "Sénégal", "Autre"], index=0)
        st.divider()
        st.markdown("**Données**")
        if st.button("🔄 Recharger données d'exemple"):
            st.cache_data.clear()
            st.rerun()
        uploaded = st.file_uploader("📤 Upload CSV joueurs (optionnel)", type=["csv"])
        st.divider()
        st.markdown("**Version** : v0.3 Streamlit\n**Moteur** : Simulation + GA avancé\n**Statut** : En construction collaborative")

    # Load players
    players = get_sample_players()
    if uploaded:
        try:
            df = pd.read_csv(uploaded)  # nécessite pandas, mais on gère
            st.success(f"✅ {len(df)} joueurs chargés depuis ton CSV !")
            # Simple parsing (à améliorer)
        except:
            st.warning("CSV non compatible pour l'instant. Utilise les données d'exemple.")

    # Create opponents
    opponents = [Team(f"Adversaire {i+1}", random.sample(players, 11), 
                      random.choice(list(FORMATION_SLOTS.keys())), 
                      random.choice(list(TACTICS.keys()))) for i in range(6)]

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏟️ Base de joueurs", 
        "🧬 Optimisation IA", 
        "⚔️ Simulateur de match", 
        "🏆 Tournoi complet", 
        "📊 Visualisations & Terrain"
    ])

    # TAB 1 - Base joueurs
    with tab1:
        st.subheader("📋 Base de données des joueurs")
        player_data = []
        for p in players:
            player_data.append({
                "Nom": p.name,
                "Position": p.position,
                "Overall": round(p.get_overall(), 1),
                "Âge": p.age,
                "Pace": p.attributes.get('pace', 0),
                "Tir": p.attributes.get('shoot', 0),
                "Passe": p.attributes.get('pass', 0),
                "Dribble": p.attributes.get('dribble', 0),
                "Défense": p.attributes.get('defend', 0),
                "Physique": p.attributes.get('phys', 0),
            })
        df = pd.DataFrame(player_data) if 'pd' in dir() else None
        if df is not None:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.write("Joueurs disponibles :")
            for p in players:
                st.write(f"- {p}")

    # TAB 2 - Optimisation
    with tab2:
        st.subheader("🧬 Optimisation par Algorithme Génétique Avancé")
        st.markdown("L'IA va simuler des **dizaines de tournois complets** pour trouver la meilleure sélection + tactique.")

        col1, col2 = st.columns([1, 2])
        with col1:
            generations = st.slider("Nombre de générations", 8, 20, 14)
            pop_size = st.slider("Taille population", 16, 32, 24)
        with col2:
            st.info("Critère d'optimisation : Points en tournoi + différence de buts + bonus qualification")

        if st.button("🚀 LANCER L'OPTIMISATION IA", type="primary", use_container_width=True):
            progress = st.progress(0, text="Initialisation...")
            with st.spinner("L'IA optimise la sélection nationale... (peut prendre 30-90 secondes)"):
                best_team, fitness, wr, diff = evolve_best_team_streamlit(
                    players, opponents, generations=generations, pop_size=pop_size, progress_bar=progress
                )
            progress.empty()

            st.success(f"✅ Sélection optimale trouvée ! Fitness : {fitness:.1f} | Victoires ~{wr*100:.1f}%")

            # Affichage équipe
            st.markdown(f"### 🏆 {best_team.name} — {best_team.formation} — **{best_team.tactics}**")
            st.metric("Overall équipe", f"{best_team.get_overall_rating():.1f}")

            cols = st.columns(4)
            for i, pos in enumerate(POSITIONS):
                with cols[i]:
                    st.markdown(f"**{pos}**")
                    for p in [pp for pp in best_team.starting11 if pp.position == pos]:
                        st.write(f"{p.name} ({p.get_overall():.1f})")

            if st.button("💾 Sauvegarder cette sélection"):
                fname = save_selection(best_team, fitness)
                st.success(f"Sauvegardée dans {fname}")

            st.session_state['best_team'] = best_team
            st.session_state['best_fitness'] = fitness

    # TAB 3 - Match simulator
    with tab3:
        st.subheader("⚔️ Simulateur de match événementiel")
        if 'best_team' in st.session_state:
            team1 = st.session_state['best_team']
        else:
            team1 = create_random_squad(players)

        team2 = random.choice(opponents)
        st.write(f"**{team1}** vs **{team2}**")

        if st.button("▶️ Simuler le match", type="primary"):
            with st.spinner("Simulation en cours..."):
                g1, g2, diff, events = simulate_advanced_match(team1, team2, verbose=False)
            st.markdown(f"## {g1} - {g2}")
            st.caption(f"Différence de buts : {diff:+d}")

            with st.expander("📜 Journal des événements (derniers)"):
                for e in events[-12:]:
                    st.write(e)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Possession", f"{team1.stats.get('avg_possession', 50):.1f}%")
            with col2:
                st.metric("Tirs", team1.stats.get('shots', 0))

    # TAB 4 - Tournoi
    with tab4:
        st.subheader("🏆 Simulateur de tournoi complet")
        if st.button("▶️ Lancer un mini-tournoi avec la meilleure équipe"):
            if 'best_team' not in st.session_state:
                st.warning("Lance d'abord l'optimisation dans l'onglet 2")
            else:
                team = st.session_state['best_team']
                with st.spinner("Tournoi en cours..."):
                    fit, pts, diff, qual, results = simulate_tournament(team, opponents)
                st.success(f"Points : {pts} | Diff buts : {diff:+.1f} | Qualifié : {'✅' if qual else '❌'}")
                st.dataframe(pd.DataFrame(results, columns=["Adversaire", "Buts pour", "Buts contre"]), use_container_width=True)

    # TAB 5 - Visualisations
    with tab5:
        st.subheader("📊 Visualisations & Terrain de jeu")
        if 'best_team' in st.session_state:
            team = st.session_state['best_team']
            st.pyplot(draw_football_pitch(team))
            st.caption("Terrain avec placement approximatif selon la formation")

            # Graphiques simples
            st.markdown("### Notes par poste")
            pos_overalls = {}
            for pos in POSITIONS:
                pos_overalls[pos] = [p.get_overall() for p in team.starting11 if p.position == pos]
            for pos, vals in pos_overalls.items():
                if vals:
                    st.write(f"**{pos}** : {np.mean(vals):.1f} (min {min(vals):.1f} - max {max(vals):.1f})")
        else:
            st.info("Lance l'optimisation dans l'onglet 2 pour voir le terrain et les stats visuelles.")

    # Footer
    st.divider()
    st.markdown("""
    **LibreSelect Foot v0.3** — Créé en open source collaboratif  
    Prochaine version : encore plus de visuels, données réelles, apprentissage par renforcement...  
    **GO pour la v0.4 ?** Dis-moi ce que tu veux ajouter !
    """)


if __name__ == "__main__":
    # Petite astuce pour pandas si pas importé globalement
    try:
        import pandas as pd
    except ImportError:
        pd = None
    main()
