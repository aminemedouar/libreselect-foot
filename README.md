# ⚽ LibreSelect Foot

**L'outil le plus perfectionné au monde pour les sélections nationales de football**

Simulation événementielle avancée • Algorithme génétique intelligent • Interface web moderne Streamlit • Open Source (usage non-commercial)

[![License: Non-Commercial](https://img.shields.io/badge/License-Non--Commercial-blue.svg)](LICENSE)

---

## 🌟 Vision

LibreSelect Foot est un projet open source collaboratif qui vise à créer **le logiciel de référence mondial** pour optimiser les sélections nationales de football.

Grâce à :
- Un **moteur de simulation de match ultra-réaliste** (événements minute par minute, fatigue, remplacements, tactiques)
- Un **algorithme génétique avancé** qui teste des milliers de combinaisons en simulant des tournois complets
- Une **interface web moderne** (Streamlit)
- Des données par pays et une architecture extensible

...tu peux trouver en quelques clics la **meilleure sélection + tactique** pour ton pays !

---

## 🚀 Installation & Lancement (v0.3)

### Prérequis
```bash
pip install -r requirements.txt
```

### Lancement
```bash
git clone https://github.com/TON-USERNAME/libreselect-foot.git
cd libreselect-foot
streamlit run streamlit_app.py
```

L'application s'ouvre automatiquement dans ton navigateur.

---

## ✨ Fonctionnalités principales (v0.3)

| Onglet | Description |
|--------|-------------|
| 🏟️ Base de joueurs | Tableau interactif de tous les joueurs avec filtres |
| 🧬 Optimisation IA | Lance l'algorithme génétique → obtient la sélection optimale + tactique en 30-90s |
| ⚔️ Simulateur de match | Simule un match complet avec événements détaillés (buts, passes, duels, remplacements) |
| 🏆 Tournoi complet | Simule une phase de groupes + élimination directe |
| 📊 Visualisations | Terrain de foot dessiné + stats par poste |

**Points forts du moteur :**
- Simulation événementielle (passes, tirs, duels, fautes)
- Fatigue des joueurs + remplacements automatiques
- Impact réel des tactiques (attacking, high_press, counter...)
- Évaluation par **tournoi complet** (pas juste un match)
- Crossover intelligent par position dans l'algorithme génétique

---

## 📜 Licence

**Usage strictement non-commercial uniquement.**

Voir le fichier [LICENSE](LICENSE) pour les termes complets.

Tu peux :
- Utiliser, modifier, partager pour tes projets personnels, recherches, éducation, communauté
- Contribuer au projet

Tu ne peux **pas** :
- Vendre le logiciel
- L'utiliser dans un produit commercial
- Le proposer en SaaS payant
- Toute forme de monétisation sans autorisation écrite des contributeurs

Pour une licence commerciale, ouvre une issue sur GitHub.

---

## 🛠️ Comment contribuer

1. Fork le repo
2. Crée une branche (`git checkout -b feature/ma-super-idee`)
3. Améliore le code (nouveau moteur, meilleurs visuels, vraies données, etc.)
4. Ouvre une Pull Request

Idées bienvenues pour les prochaines versions :
- Intégration de vraies données (FBref, etc.)
- Plus de visuels (heatmaps, animations)
- Simulation complète de Coupe du Monde
- Apprentissage par renforcement pour les tactiques
- Support multilingue
- Export PDF des rapports

---

## 📁 Structure du projet

```
libreselect-foot/
├── streamlit_app.py                    # Application web principale
├── ai_tactics_engine.py                # Moteur de simulation et recommandation IA
├── national_teams_db.py                # Base de données des sélections nationales
├── LICENSE                             # Licence non-commerciale
├── README.md
└── (futurs) data/, models/, etc.
```

Les versions précédentes (v0.1 & v0.2) sont disponibles dans l'historique ou sur demande.

---

## 🙏 Remerciements

Créé de manière collaborative entre humains et IA (Grok) dans un esprit 100% open source et libre.

**Allons-y : on rend cet outil le plus perfectionné du monde, ensemble.**

---

**LibreSelect Foot** — Pour que chaque pays ait accès à la meilleure sélection possible.

⚽🌍🚀

*Si tu utilises ce projet, star le repo et dis-le nous !*
