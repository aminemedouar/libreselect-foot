"""
🎯 AI Tactical Simulation Engine for LibreSelect Foot
- Simule toutes les tactiques possibles
- Teste contre chaque équipe adverse
- Recommande la meilleure sélection + tactique
- Utilise machine learning pour optimiser
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
from itertools import combinations
import random

# ============================================================
# 1️⃣ DONNÉES & MODÈLES
# ============================================================

@dataclass
class Player:
    """Modèle d'un joueur"""
    name: str
    position: str  # GK, DEF, MID, FWD
    pace: int      # 1-100
    passing: int
    dribbling: int
    shooting: int
    defense: int
    physical: int
    country: str
    overall: int = None
    
    def __post_init__(self):
        if self.overall is None:
            self.overall = int(np.mean([
                self.pace, self.passing, self.dribbling,
                self.shooting, self.defense, self.physical
            ]))

@dataclass
class Tactic:
    """Modèle d'une tactique"""
    name: str
    formation: str  # "4-3-3", "3-5-2", etc.
    style: str      # "attacking", "balanced", "defensive", "counter"
    
    # Modifieurs de performance
    attacking_boost: float = 1.0
    defensive_boost: float = 1.0
    transition_speed: float = 1.0
    possession_style: str = "balanced"

@dataclass
class Team:
    """Modèle d'une équipe"""
    name: str
    players: List[Player]
    formation: str
    tactic: Tactic = None
    overall_rating: float = None
    
    def __post_init__(self):
        if self.overall_rating is None:
            self.overall_rating = np.mean([p.overall for p in self.players])

# ============================================================
# 2️⃣ SIMULATIONS DE MATCH
# ============================================================

class MatchSimulator:
    """Simule un match complet avec événements"""
    
    def __init__(self, home_team: Team, away_team: Team, seed: int = None):
        self.home_team = home_team
        self.away_team = away_team
        self.seed = seed
        if seed:
            np.random.seed(seed)
        
        self.home_score = 0
        self.away_score = 0
        self.events = []
        self.minute = 0
    
    def simulate(self) -> Tuple[int, int, List[str]]:
        """Simule 90 minutes de match"""
        for minute in range(1, 91):
            self.minute = minute
            
            # Chances de but basées sur:
            # - Qualité offensive de l'équipe
            # - Tactique
            # - Fatigue (augmente vers fin match)
            
            home_quality = self._calculate_team_quality(
                self.home_team, is_attacking=True
            )
            away_quality = self._calculate_team_quality(
                self.away_team, is_attacking=True
            )
            
            # Fatigue (augmente après minute 60)
            fatigue_factor = 1.0 + (max(0, minute - 60) / 30) * 0.3
            
            # Chance de but
            home_goal_chance = (home_quality / (home_quality + away_quality)) * 0.02 / fatigue_factor
            away_goal_chance = (away_quality / (home_quality + away_quality)) * 0.02 / fatigue_factor
            
            if np.random.random() < home_goal_chance:
                self.home_score += 1
                self.events.append(f"⚽ Min {minute}: BUT! {self.home_team.name}")
            
            if np.random.random() < away_goal_chance:
                self.away_score += 1
                self.events.append(f"⚽ Min {minute}: BUT! {self.away_team.name}")
            
            # Autres événements
            if np.random.random() < 0.1:
                card = "🟨 Carton jaune" if np.random.random() < 0.8 else "🔴 Carton rouge"
                team = np.random.choice([self.home_team.name, self.away_team.name])
                self.events.append(f"{card} Min {minute}: {team}")
        
        return self.home_score, self.away_score, self.events
    
    def _calculate_team_quality(self, team: Team, is_attacking: bool) -> float:
        """Calcule la qualité offensive/défensive d'une équipe"""
        if is_attacking:
            relevant_stat = np.mean([p.shooting for p in team.players])
        else:
            relevant_stat = np.mean([p.defense for p in team.players])
        
        tactic_boost = 1.0
        if team.tactic:
            if is_attacking and team.tactic.attacking_boost:
                tactic_boost = team.tactic.attacking_boost
            elif not is_attacking and team.tactic.defensive_boost:
                tactic_boost = team.tactic.defensive_boost
        
        return relevant_stat * tactic_boost

# ============================================================
# 3️⃣ SÉLECTION D'ÉQUIPE OPTIMISÉE
# ============================================================

class SelectionOptimizer:
    """Optimise la sélection des joueurs"""
    
    def __init__(self, available_players: List[Player]):
        self.available_players = available_players
        self.positions = {
            'GK': 2,   # 2 gardiens
            'DEF': 8,  # 8 défenseurs
            'MID': 6,  # 6 milieux
            'FWD': 5   # 5 attaquants
        }
    
    def select_best_squad(self) -> List[Player]:
        """Sélectionne les meilleurs joueurs par position"""
        selected = []
        
        for position, count in self.positions.items():
            players_by_pos = [p for p in self.available_players if p.position == position]
            best = sorted(players_by_pos, key=lambda p: p.overall, reverse=True)[:count]
            selected.extend(best)
        
        return selected
    
    def genetic_algorithm_selection(
        self,
        opponent_team: Team,
        tactics_to_test: List[Tactic],
        generations: int = 10,
        population_size: int = 20
    ) -> Tuple[List[Player], Tactic, float]:
        """
        Algorithme génétique pour trouver la meilleure combinaison
        sélection + tactique contre un adversaire spécifique
        """
        
        # Population initiale
        population = [self.select_best_squad() for _ in range(population_size)]
        best_selection = population[0]
        best_tactic = tactics_to_test[0]
        best_fitness = 0
        
        for gen in range(generations):
            # Évaluer fitness de chaque individu
            fitness_scores = []
            
            for selection in population:
                max_fitness = 0
                best_tactic_for_selection = tactics_to_test[0]
                
                # Tester chaque tactique
                for tactic in tactics_to_test:
                    team = Team(
                        name="Selection",
                        players=selection,
                        formation=tactic.formation,
                        tactic=tactic
                    )
                    
                    # Simuler plusieurs matchs
                    wins = 0
                    for _ in range(3):  # 3 simulations
                        sim = MatchSimulator(team, opponent_team)
                        home_score, away_score, _ = sim.simulate()
                        if home_score > away_score:
                            wins += 1
                    
                    fitness = wins
                    if fitness > max_fitness:
                        max_fitness = fitness
                        best_tactic_for_selection = tactic
                
                fitness_scores.append(max_fitness)
                
                if max_fitness > best_fitness:
                    best_fitness = max_fitness
                    best_selection = selection
                    best_tactic = best_tactic_for_selection
            
            # Sélection + Crossover + Mutation
            best_indices = np.argsort(fitness_scores)[-population_size // 2:]
            new_population = [population[i] for i in best_indices]
            
            # Crossover
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(new_population[:population_size//2], 2)
                child = parent1[:len(parent1)//2] + parent2[len(parent2)//2:]
                new_population.append(child)
            
            population = new_population
        
        return best_selection, best_tactic, best_fitness

# ============================================================
# 4️⃣ MOTEUR DE RECOMMANDATION
# ============================================================

class TacticsRecommendationEngine:
    """Recommande la meilleure tactique + sélection"""
    
    # Tactiques prédéfinies
    TACTICS = [
        Tactic("4-3-3 Attacking", "4-3-3", "attacking", 1.3, 0.8, 1.1),
        Tactic("4-3-3 Balanced", "4-3-3", "balanced", 1.0, 1.0, 1.0),
        Tactic("4-3-3 Defensive", "4-3-3", "defensive", 0.8, 1.3, 0.9),
        Tactic("3-5-2 Attacking", "3-5-2", "attacking", 1.2, 0.9, 1.2),
        Tactic("3-5-2 Balanced", "3-5-2", "balanced", 1.0, 1.0, 1.0),
        Tactic("5-3-2 Defensive", "5-3-2", "defensive", 0.7, 1.4, 0.8),
        Tactic("4-2-3-1 Balanced", "4-2-3-1", "balanced", 1.0, 1.0, 1.0),
        Tactic("4-4-2 Counter", "4-4-2", "counter", 0.9, 1.1, 1.3),
    ]
    
    def __init__(self, available_players: List[Player]):
        self.available_players = available_players
        self.optimizer = SelectionOptimizer(available_players)
    
    def analyze_opponent(self, opponent_team: Team) -> Dict:
        """Analyse les forces/faiblesses de l'adversaire"""
        avg_attack = np.mean([p.shooting for p in opponent_team.players])
        avg_defense = np.mean([p.defense for p in opponent_team.players])
        avg_pace = np.mean([p.pace for p in opponent_team.players])
        
        return {
            'avg_attack': avg_attack,
            'avg_defense': avg_defense,
            'avg_pace': avg_pace,
            'style': 'attacking' if avg_attack > avg_defense else 'defensive'
        }
    
    def recommend_tactic(self, opponent: Team) -> Dict:
        """
        Recommande la meilleure tactique + sélection
        contre un adversaire spécifique
        """
        opponent_analysis = self.analyze_opponent(opponent)
        
        # Lancer optimisation génétique
        best_selection, best_tactic, fitness = (
            self.optimizer.genetic_algorithm_selection(
                opponent_team=opponent,
                tactics_to_test=self.TACTICS,
                generations=5,
                population_size=10
            )
        )
        
        return {
            'recommended_formation': best_tactic.formation,
            'recommended_tactic': best_tactic.name,
            'recommended_selection': best_selection,
            'expected_win_probability': fitness / 3,  # fitness = wins out of 3
            'opponent_analysis': opponent_analysis,
            'tactical_advice': self._generate_tactical_advice(
                best_tactic, opponent_analysis
            )
        }
    
    def _generate_tactical_advice(self, tactic: Tactic, opponent_analysis: Dict) -> str:
        """Génère des conseils tactiques"""
        advice = f"🎯 Tactique recommandée: {tactic.name}\n\n"
        
        if opponent_analysis['style'] == 'attacking':
            advice += "⚔️ L'adversaire joue offensif. Conseils:\n"
            advice += "- Renforcez la défense\n"
            advice += "- Utilisez les contre-attaques\n"
            advice += "- Repli défensif rapide\n"
        else:
            advice += "🛡️ L'adversaire joue défensif. Conseils:\n"
            advice += "- Dominance du ballon\n"
            advice += "- Passes courtes + build-up\n"
            advice += "- Exploitez les côtés\n"
        
        if opponent_analysis['avg_pace'] > 75:
            advice += "\n⚡ Vitesse élevée de l'adversaire:\n"
            advice += "- Défense compacte et organisée\n"
            advice += "- Postures défensives\n"
        
        return advice

# ============================================================
# 5️⃣ RAPPORT DE MATCH
# ============================================================

class MatchReport:
    """Génère un rapport détaillé de match"""
    
    @staticmethod
    def generate(
        home_team: Team,
        away_team: Team,
        home_score: int,
        away_score: int,
        events: List[str],
        recommendation: Dict = None
    ) -> str:
        """Génère un rapport texte complet"""
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           📊 RAPPORT DE MATCH SIMULATION                   ║
╚════════════════════════════════════════════════════════════╝

🏟️ ÉQUIPES:
  🏠 {home_team.name} ({home_team.formation}) vs {away_team.name} ({away_team.formation}) ⛔

📈 SCORE FINAL:
  {home_team.name}: {home_score} - {away_score} :{away_team.name}
  
{'🏆 VICTOIRE ' + home_team.name if home_score > away_score else '🏆 VICTOIRE ' + away_team.name if away_score > home_score else '🤝 MATCH NUL'}

📋 ÉVÉNEMENTS:
"""
        for event in events:
            report += f"  {event}\n"
        
        if recommendation:
            report += f"""

🎯 RECOMMANDATION POUR LE MATCH:
  Formation: {recommendation['recommended_formation']}
  Tactique: {recommendation['recommended_tactic']}
  Probabilité de victoire estimée: {recommendation['expected_win_probability']*100:.1f}%

💡 CONSEILS TACTIQUES:
{recommendation['tactical_advice']}
"""
        
        return report

# ============================================================
# TESTS & EXEMPLES
# ============================================================

if __name__ == "__main__":
    # Créer quelques joueurs pour tester
    players_france = [
        Player("Mbappé", "FWD", 96, 80, 90, 92, 65, 85, "France", 89),
        Player("Benzema", "FWD", 80, 90, 88, 92, 50, 82, "France", 85),
        Player("Griezmann", "MID", 85, 92, 87, 80, 75, 78, "France", 84),
        Player("Kanté", "MID", 88, 92, 85, 40, 88, 80, "France", 82),
        Player("Varane", "DEF", 87, 88, 85, 25, 90, 88, "France", 83),
        Player("Benzema", "DEF", 85, 78, 70, 20, 88, 85, "France", 78),
        Player("Lloris", "GK", 50, 70, 25, 20, 85, 82, "France", 60),
    ] * 3  # Dupliquer pour avoir assez de joueurs
    
    players_spain = [
        Player("Pedri", "MID", 85, 95, 88, 70, 75, 70, "Spain", 84),
        Player("Busquets", "MID", 78, 95, 85, 30, 85, 78, "Spain", 79),
        Player("Ramos", "DEF", 82, 88, 80, 30, 92, 85, "Spain", 81),
        Player("Unai Simón", "GK", 50, 70, 30, 20, 85, 80, "Spain", 59),
    ] * 3
    
    # Créer équipes
    france = Team("France", players_france[:11], "4-3-3")
    spain = Team("Spain", players_spain[:11], "4-3-3")
    
    # Simuler
    print("🎮 Simulation de match...")
    sim = MatchSimulator(france, spain)
    home_score, away_score, events = sim.simulate()
    
    print(MatchReport.generate(france, spain, home_score, away_score, events))
    
    # Recommandation
    print("\n🤖 Analyse IA...")
    engine = TacticsRecommendationEngine(players_france)
    recommendation = engine.recommend_tactic(spain)
    
    print(f"✅ Formation recommandée: {recommendation['recommended_formation']}")
    print(f"✅ Tactique: {recommendation['recommended_tactic']}")
    print(f"✅ Probabilité de victoire: {recommendation['expected_win_probability']*100:.1f}%")
    print(f"\n{recommendation['tactical_advice']}")


def run_genetic_algorithm(players_data: List[Dict], generations: int = 50):
    """
    Wrapper simple pour Streamlit Cloud:
    prend des dicts joueurs et retourne un XI optimisé.
    """
    if not players_data:
        return {"players": [], "summary": "Aucun joueur disponible pour ce pays."}

    players = [
        Player(
            name=p["name"],
            position=p["pos"],
            pace=p["pace"],
            passing=p["pass"],
            dribbling=p["drib"],
            shooting=p["shoot"],
            defense=p["def"],
            physical=p["phys"],
            country="Selection",
            overall=p.get("rating"),
        )
        for p in players_data
    ]

    optimizer = SelectionOptimizer(players)
    best_squad = optimizer.select_best_squad()
    best_xi = sorted(best_squad, key=lambda player: player.overall, reverse=True)[:11]

    return {
        "generations": generations,
        "players": [
            {"name": p.name, "position": p.position, "overall": p.overall}
            for p in best_xi
        ],
        "summary": f"Sélection optimisée sur {len(players)} joueurs.",
    }
