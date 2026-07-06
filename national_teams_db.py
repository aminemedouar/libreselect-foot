"""
🌍 NATIONAL TEAMS DATABASE
Base de données des équipes nationales avec joueurs réels
Support pour 9 pays
"""

NATIONAL_TEAMS = {
    "🇫🇷 France": {
        "coach": "Didier Deschamps",
        "formation": "4-3-3",
        "players": [
            {"name": "Mike Maignan", "pos": "GK", "pace": 78, "pass": 72, "drib": 45, "shoot": 25, "def": 85, "phys": 82, "rating": 85},
            {"name": "William Saliba", "pos": "DEF", "pace": 85, "pass": 72, "drib": 62, "shoot": 35, "def": 88, "phys": 86, "rating": 84},
            {"name": "Dayot Upamecano", "pos": "DEF", "pace": 88, "pass": 75, "drib": 65, "shoot": 40, "def": 89, "phys": 87, "rating": 86},
            {"name": "Benjamin Pavard", "pos": "DEF", "pace": 82, "pass": 76, "drib": 68, "shoot": 45, "def": 85, "phys": 84, "rating": 84},
            {"name": "Théo Hernández", "pos": "DEF", "pace": 88, "pass": 78, "drib": 82, "shoot": 50, "def": 82, "phys": 85, "rating": 85},
            {"name": "Jules Koundé", "pos": "DEF", "pace": 86, "pass": 74, "drib": 70, "shoot": 38, "def": 87, "phys": 85, "rating": 84},
            {"name": "Kylian Mbappé", "pos": "FWD", "pace": 96, "pass": 84, "drib": 92, "shoot": 94, "def": 65, "phys": 88, "rating": 95},
            {"name": "Antoine Griezmann", "pos": "MID", "pace": 85, "pass": 82, "drib": 86, "shoot": 84, "def": 78, "phys": 80, "rating": 86},
            {"name": "N'Golo Kanté", "pos": "MID", "pace": 86, "pass": 81, "drib": 82, "shoot": 72, "def": 90, "phys": 88, "rating": 87},
            {"name": "Eduardo Camavinga", "pos": "MID", "pace": 89, "pass": 80, "drib": 84, "shoot": 76, "def": 87, "phys": 86, "rating": 85},
            {"name": "Karim Benzema", "pos": "FWD", "pace": 82, "pass": 86, "drib": 88, "shoot": 92, "def": 70, "phys": 85, "rating": 91},
            {"name": "Ousmane Dembélé", "pos": "FWD", "pace": 94, "pass": 80, "drib": 93, "shoot": 86, "def": 60, "phys": 82, "rating": 88},
        ]
    },
    
    "🇩🇪 Allemagne": {
        "coach": "Julian Nagelsmann",
        "formation": "4-2-3-1",
        "players": [
            {"name": "Manuel Neuer", "pos": "GK", "pace": 76, "pass": 74, "drib": 50, "shoot": 20, "def": 88, "phys": 85, "rating": 89},
            {"name": "Antonio Rüdiger", "pos": "DEF", "pace": 82, "pass": 72, "drib": 65, "shoot": 35, "def": 90, "phys": 88, "rating": 87},
            {"name": "Mats Hummels", "pos": "DEF", "pace": 80, "pass": 78, "drib": 70, "shoot": 40, "def": 89, "phys": 86, "rating": 86},
            {"name": "Joshua Kimmich", "pos": "MID", "pace": 86, "pass": 88, "drib": 82, "shoot": 72, "def": 85, "phys": 84, "rating": 87},
            {"name": "Leroy Sané", "pos": "MID", "pace": 93, "pass": 82, "drib": 90, "shoot": 82, "def": 55, "phys": 81, "rating": 88},
            {"name": "İlkay Gündoğan", "pos": "MID", "pace": 82, "pass": 90, "drib": 85, "shoot": 80, "def": 70, "phys": 78, "rating": 87},
            {"name": "Kai Havertz", "pos": "FWD", "pace": 88, "pass": 82, "drib": 86, "shoot": 84, "def": 62, "phys": 82, "rating": 87},
            {"name": "Jamal Musiala", "pos": "MID", "pace": 92, "pass": 86, "drib": 91, "shoot": 85, "def": 62, "phys": 80, "rating": 88},
        ]
    },
    
    "🇪🇸 Espagne": {
        "coach": "Luis de la Fuente",
        "formation": "4-3-3",
        "players": [
            {"name": "Unai Simón", "pos": "GK", "pace": 72, "pass": 72, "drib": 40, "shoot": 20, "def": 85, "phys": 80, "rating": 83},
            {"name": "Sergio Busquets", "pos": "MID", "pace": 78, "pass": 95, "drib": 85, "shoot": 30, "def": 85, "phys": 78, "rating": 88},
            {"name": "Pedri González", "pos": "MID", "pace": 85, "pass": 95, "drib": 88, "shoot": 70, "def": 75, "phys": 70, "rating": 86},
            {"name": "Gavi", "pos": "MID", "pace": 87, "pass": 92, "drib": 87, "shoot": 72, "def": 73, "phys": 72, "rating": 84},
            {"name": "Sergio Ramos", "pos": "DEF", "pace": 82, "pass": 88, "drib": 80, "shoot": 30, "def": 92, "phys": 85, "rating": 88},
            {"name": "Ferran Torres", "pos": "FWD", "pace": 91, "pass": 82, "drib": 89, "shoot": 85, "def": 62, "phys": 83, "rating": 87},
            {"name": "Álvaro Morata", "pos": "FWD", "pace": 84, "pass": 80, "drib": 83, "shoot": 86, "def": 62, "phys": 83, "rating": 84},
        ]
    },
    
    "🇮🇹 Italie": {
        "coach": "Luciano Spalletti",
        "formation": "4-3-3",
        "players": [
            {"name": "Gianluigi Donnarumma", "pos": "GK", "pace": 74, "pass": 75, "drib": 48, "shoot": 22, "def": 87, "phys": 83, "rating": 87},
            {"name": "Alessandro Bastoni", "pos": "DEF", "pace": 85, "pass": 82, "drib": 75, "shoot": 35, "def": 88, "phys": 86, "rating": 86},
            {"name": "Leonardo Bonucci", "pos": "DEF", "pace": 80, "pass": 85, "drib": 78, "shoot": 38, "def": 89, "phys": 84, "rating": 86},
            {"name": "Nicolò Barella", "pos": "MID", "pace": 87, "pass": 85, "drib": 83, "shoot": 76, "def": 82, "phys": 85, "rating": 86},
            {"name": "Vinícius Júnior", "pos": "FWD", "pace": 96, "pass": 79, "drib": 90, "shoot": 85, "def": 60, "phys": 84, "rating": 90},
            {"name": "Ciro Immobile", "pos": "FWD", "pace": 85, "pass": 78, "drib": 82, "shoot": 88, "def": 60, "phys": 82, "rating": 84},
        ]
    },
    
    "🇵🇹 Portugal": {
        "coach": "Fernando Santos",
        "formation": "4-3-3",
        "players": [
            {"name": "Rui Patrício", "pos": "GK", "pace": 72, "pass": 70, "drib": 40, "shoot": 20, "def": 85, "phys": 80, "rating": 83},
            {"name": "Pepe", "pos": "DEF", "pace": 80, "pass": 78, "drib": 70, "shoot": 35, "def": 91, "phys": 88, "rating": 87},
            {"name": "Rúben Dias", "pos": "DEF", "pace": 85, "pass": 82, "drib": 72, "shoot": 38, "def": 90, "phys": 86, "rating": 87},
            {"name": "João Cancelo", "pos": "DEF", "pace": 88, "pass": 84, "drib": 84, "shoot": 50, "def": 82, "phys": 84, "rating": 86},
            {"name": "Bruno Fernandes", "pos": "MID", "pace": 86, "pass": 90, "drib": 87, "shoot": 82, "def": 72, "phys": 80, "rating": 88},
            {"name": "Cristiano Ronaldo", "pos": "FWD", "pace": 87, "pass": 82, "drib": 87, "shoot": 93, "def": 65, "phys": 85, "rating": 92},
        ]
    },
    
    "🇦🇷 Argentina": {
        "coach": "Lionel Scaloni",
        "formation": "4-3-3",
        "players": [
            {"name": "Emiliano Martínez", "pos": "GK", "pace": 76, "pass": 72, "drib": 45, "shoot": 22, "def": 86, "phys": 83, "rating": 85},
            {"name": "Cristian Romero", "pos": "DEF", "pace": 88, "pass": 78, "drib": 72, "shoot": 38, "def": 90, "phys": 88, "rating": 87},
            {"name": "Enzo Fernández", "pos": "MID", "pace": 86, "pass": 88, "drib": 84, "shoot": 76, "def": 84, "phys": 85, "rating": 86},
            {"name": "Lionel Messi", "pos": "FWD", "pace": 85, "pass": 92, "drib": 95, "shoot": 92, "def": 70, "phys": 78, "rating": 93},
            {"name": "Ángel Di María", "pos": "FWD", "pace": 88, "pass": 84, "drib": 87, "shoot": 84, "def": 62, "phys": 80, "rating": 86},
        ]
    },
    
    "🇧🇷 Brésil": {
        "coach": "Dorival Júnior",
        "formation": "4-3-3",
        "players": [
            {"name": "Alisson", "pos": "GK", "pace": 76, "pass": 78, "drib": 48, "shoot": 25, "def": 87, "phys": 84, "rating": 89},
            {"name": "Thiago Silva", "pos": "DEF", "pace": 82, "pass": 82, "drib": 75, "shoot": 38, "def": 91, "phys": 85, "rating": 88},
            {"name": "Marquinhos", "pos": "DEF", "pace": 85, "pass": 80, "drib": 72, "shoot": 36, "def": 90, "phys": 87, "rating": 87},
            {"name": "Casemiro", "pos": "MID", "pace": 84, "pass": 82, "drib": 78, "shoot": 70, "def": 88, "phys": 88, "rating": 88},
            {"name": "Vinícius Júnior", "pos": "FWD", "pace": 96, "pass": 79, "drib": 90, "shoot": 85, "def": 60, "phys": 84, "rating": 90},
            {"name": "Neymar", "pos": "FWD", "pace": 89, "pass": 86, "drib": 92, "shoot": 84, "def": 58, "phys": 80, "rating": 88},
        ]
    },
}

def get_team(country_name: str):
    """Récupère une équipe par nom"""
    if country_name in NATIONAL_TEAMS:
        return NATIONAL_TEAMS[country_name]
    return None

def list_countries():
    """Liste tous les pays disponibles"""
    return list(NATIONAL_TEAMS.keys())

def get_best_players_by_position(country_name: str, position: str, count: int = 3):
    """Récupère les meilleurs joueurs par position"""
    team = get_team(country_name)
    if team:
        players = [p for p in team['players'] if p['pos'] == position]
        return sorted(players, key=lambda x: x['rating'], reverse=True)[:count]
    return []
