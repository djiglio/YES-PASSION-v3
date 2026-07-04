import json
import math

# --- FUNZIONI DI SUPPORTO ---

def calc_ovr(players, roles):
    selected = [p for p in players if any(r in p['Ruolo'] for r in roles)]
    if not selected:
        return 75
    selected.sort(key=lambda x: x['Overall'], reverse=True)
    top = selected[:4] if len(selected) > 4 else selected
    return int(round(sum(p['Overall'] for p in top) / len(top)))

def calculate_squad_strength(players):
    att_roles = ['ATT', 'AS', 'AD', 'AT']
    mid_roles = ['COC', 'CC', 'CDC', 'ES', 'ED']
    def_roles = ['DC', 'TS', 'TD', 'ADA', 'ASA']
    gk_roles = ['POR']
    
    return {
        "att_ovr": calc_ovr(players, att_roles),
        "mid_ovr": calc_ovr(players, mid_roles),
        "def_ovr": calc_ovr(players, def_roles),
        "gk_ovr": calc_ovr(players, gk_roles)
    }

def format_value(value_num):
    if value_num >= 1000000:
        return f"€{round(value_num/1000000, 1)}M"
    else:
        return f"€{round(value_num/1000)}K"

def build_team(id, name, real_points, players_data):
    players = []
    for p in players_data:
        val_num = p[3]
        players.append({
            "Nome": p[0],
            "Ruolo": p[1],
            "Overall": p[2],
            "Value": format_value(val_num),
            "ValueNum": float(val_num),
            "Age": p[4]
        })
    
    return {
        "id": id,
        "name": name,
        "real_points": real_points,
        "squad_strength": calculate_squad_strength(players),
        "players": players
    }

# ================= FC 25 ================= #

teams_25 = [
    build_team('inter', 'Inter', 94, [
        ('L. Martínez', 'ATT', 89, 100000000, 26),
        ('N. Barella', 'CC, CDC', 87, 85000000, 27),
        ('A. Bastoni', 'DC', 87, 80000000, 25),
        ('H. Çalhanoğlu', 'CDC, CC', 86, 60000000, 30),
        ('Y. Sommer', 'POR', 86, 15000000, 35),
        ('M. Thuram', 'ATT, AS', 85, 65000000, 26),
        ('F. Dimarco', 'TS, ES', 84, 55000000, 26),
        ('B. Pavard', 'DC, TD', 84, 45000000, 28),
        ('H. Mkhitaryan', 'CC, COC', 83, 10000000, 35),
        ('S. de Vrij', 'DC', 83, 20000000, 32),
        ('P. Zieliński', 'CC, COC', 83, 35000000, 30),
        ('D. Dumfries', 'ED, TD', 82, 30000000, 28),
        ('M. Darmian', 'TD, DC', 81, 5000000, 34),
        ('D. Frattesi', 'CC', 81, 40000000, 24),
        ('M. Taremi', 'ATT', 81, 20000000, 31)
    ]),
    build_team('milan', 'Milan', 75, [
        ('M. Maignan', 'POR', 87, 65000000, 28),
        ('Rafael Leão', 'AS, ATT', 86, 90000000, 25),
        ('T. Hernández', 'TS', 86, 75000000, 26),
        ('F. Tomori', 'DC', 84, 50000000, 26),
        ('C. Pulisic', 'AD, COC', 83, 45000000, 25),
        ('I. Bennacer', 'CDC, CC', 83, 35000000, 26),
        ('R. Loftus-Cheek', 'CC, COC', 82, 30000000, 28),
        ('T. Reijnders', 'CC', 82, 35000000, 25),
        ('S. Chukwueze', 'AD', 81, 30000000, 25),
        ('Á. Morata', 'ATT', 82, 25000000, 31),
        ('M. Thiaw', 'DC', 80, 30000000, 22),
        ('P. Kalulu', 'DC, TD', 79, 25000000, 24),
        ('D. Calabria', 'TD', 79, 15000000, 27),
        ('S. Pavlović', 'DC', 79, 25000000, 23),
        ('Y. Fofana', 'CC, CDC', 80, 35000000, 25)
    ]),
    build_team('juventus', 'Juventus', 71, [
        ('Bremer', 'DC', 86, 60000000, 27),
        ('D. Vlahović', 'ATT', 84, 65000000, 24),
        ('Douglas Luiz', 'CC, CDC', 84, 55000000, 26),
        ('T. Koopmeiners', 'CC, COC', 84, 60000000, 26),
        ('M. Di Gregorio', 'POR', 83, 30000000, 26),
        ('F. Chiesa', 'AS, AD, ATT', 83, 45000000, 26),
        ('Danilo', 'DC, TD', 82, 10000000, 32),
        ('A. Rabiot', 'CC', 82, 35000000, 29),
        ('K. Yildiz', 'AT, COC', 80, 40000000, 19),
        ('M. Locatelli', 'CDC, CC', 81, 30000000, 26),
        ('F. Gatti', 'DC', 80, 25000000, 26),
        ('A. Cambiaso', 'TS, TD, ED', 80, 30000000, 24),
        ('K. Thuram', 'CC', 80, 35000000, 23),
        ('W. McKennie', 'CC, ED', 79, 20000000, 25),
        ('A. Milik', 'ATT', 79, 10000000, 30)
    ]),
    build_team('napoli', 'Napoli', 53, [
        ('K. Kvaratskhelia', 'AS', 85, 75000000, 23),
        ('A. Buongiorno', 'DC', 82, 40000000, 25),
        ('A. Zambo Anguissa', 'CC, CDC', 82, 35000000, 28),
        ('S. Lobotka', 'CDC, CC', 83, 30000000, 29),
        ('G. Di Lorenzo', 'TD', 83, 25000000, 30),
        ('A. Meret', 'POR', 81, 20000000, 27),
        ('M. Politano', 'AD', 80, 15000000, 30),
        ('R. Rrahmani', 'DC', 80, 20000000, 30),
        ('M. Olivera', 'TS', 79, 15000000, 26),
        ('R. Lukaku', 'ATT', 82, 30000000, 31),
        ('G. Raspadori', 'AT, ATT', 79, 25000000, 24),
        ('C. Ngonge', 'AD, ATT', 78, 15000000, 24),
        ('J. Lindstrøm', 'COC, AS', 78, 18000000, 24),
        ('L. Spinazzola', 'TS, ES', 79, 10000000, 31),
        ('S. McTominay', 'CC', 81, 30000000, 27)
    ]),
    build_team('atalanta', 'Atalanta', 69, [
        ('A. Lookman', 'AT, AS', 83, 45000000, 26),
        ('M. de Roon', 'CDC, CC', 81, 15000000, 33),
        ('Éderson', 'CC, CDC', 82, 40000000, 24),
        ('M. Pašalić', 'COC, CC', 81, 25000000, 29),
        ('G. Scamacca', 'ATT', 82, 35000000, 25),
        ('C. De Ketelaere', 'COC, AT', 81, 35000000, 23),
        ('M. Carnesecchi', 'POR', 81, 30000000, 24),
        ('S. Kolašinac', 'DC, TS', 80, 10000000, 31),
        ('B. Djimsiti', 'DC', 80, 12000000, 31),
        ('I. Hien', 'DC', 79, 20000000, 25),
        ('M. Ruggeri', 'ES, TS', 78, 18000000, 21),
        ('D. Zappacosta', 'ED, TD', 79, 10000000, 32),
        ('J. Musso', 'POR', 79, 8000000, 30),
        ('N. Zaniolo', 'AD, COC', 79, 15000000, 24),
        ('M. Retegui', 'ATT', 80, 25000000, 25)
    ]),
    build_team('roma', 'Roma', 63, [
        ('P. Dybala', 'AT, COC', 86, 50000000, 30),
        ('L. Pellegrini', 'COC, CC', 83, 40000000, 28),
        ('G. Mancini', 'DC', 82, 35000000, 28),
        ('E. Ndicka', 'DC', 81, 30000000, 24),
        ('B. Cristante', 'CDC, CC', 81, 25000000, 29),
        ('S. El Shaarawy', 'AS, ES', 80, 10000000, 31),
        ('L. Paredes', 'CDC, CC', 80, 15000000, 30),
        ('M. Svilar', 'POR', 80, 20000000, 24),
        ('M. Soulé', 'AD, COC', 80, 35000000, 21),
        ('A. Dovbyk', 'ATT', 83, 45000000, 27),
        ('Angeliño', 'TS', 79, 15000000, 27),
        ('Z. Çelik', 'TD', 78, 10000000, 27),
        ('M. Hummels', 'DC', 85, 10000000, 35),
        ('M. Hermoso', 'DC', 82, 25000000, 29),
        ('A. Saelemaekers', 'ED, ES', 78, 15000000, 25)
    ]),
    build_team('lazio', 'Lazio', 61, [
        ('M. Zaccagni', 'AS', 82, 35000000, 29),
        ('I. Provedel', 'POR', 82, 25000000, 30),
        ('Alessio Romagnoli', 'DC', 81, 20000000, 29),
        ('M. Guendouzi', 'CC, CDC', 81, 25000000, 25),
        ('T. Castellanos', 'ATT', 80, 25000000, 25),
        ('Patric', 'DC', 79, 10000000, 31),
        ('N. Rovella', 'CDC, CC', 79, 20000000, 22),
        ('M. Vecino', 'CC, CDC', 78, 8000000, 32),
        ('A. Marušić', 'TD, TS', 78, 8000000, 31),
        ('Manuel Lazzari', 'TD, ED', 78, 8000000, 30),
        ('T. Noslin', 'ATT, AS', 77, 15000000, 24),
        ('G. Castrovilli', 'CC, COC', 77, 12000000, 27),
        ('B. Dia', 'ATT', 79, 15000000, 27),
        ('N. Casale', 'DC', 78, 15000000, 26),
        ('G. Isaksen', 'AD', 77, 12000000, 23)
    ]),
    build_team('fiorentina', 'Fiorentina', 60, [
        ('A. Guðmundsson', 'AT, COC', 81, 30000000, 27),
        ('L. Beltrán', 'ATT, AT', 79, 25000000, 23),
        ('C. Biraghi', 'TS', 79, 10000000, 31),
        ('L. Martínez Quarta', 'DC', 79, 15000000, 28),
        ('D. De Gea', 'POR', 82, 10000000, 33),
        ('R. Mandragora', 'CC, CDC', 78, 12000000, 27),
        ('Dodô', 'TD', 79, 18000000, 25),
        ('P. Terracciano', 'POR', 79, 8000000, 34),
        ('M. Pongračić', 'DC', 78, 15000000, 26),
        ('A. Barák', 'COC, CC', 77, 10000000, 29),
        ('R. Gosens', 'ES, TS', 80, 15000000, 30),
        ('Y. Adli', 'CC', 77, 12000000, 23),
        ('J. Ikoné', 'AD', 77, 12000000, 26),
        ('M. Kean', 'ATT', 78, 18000000, 24),
        ('R. Sottil', 'AS', 76, 10000000, 25)
    ])
]

# Serie A Teams FC 25 filler
other_teams = ['Torino', 'Bologna', 'Genoa', 'Monza', 'Hellas Verona', 'Lecce', 'Udinese', 'Cagliari', 'Empoli', 'Parma', 'Como', 'Venezia']
for idx, name in enumerate(other_teams):
    teams_25.append(build_team(name.lower().replace(' ', ''), name, 40, [
        (f'{name} GK', 'POR', 77, 6000000, 25),
        (f'{name} CB1', 'DC', 77, 6000000, 26),
        (f'{name} CB2', 'DC', 76, 5000000, 24),
        (f'{name} RB', 'TD', 76, 5000000, 24),
        (f'{name} LB', 'TS', 76, 5000000, 25),
        (f'{name} CDM', 'CDC', 77, 6000000, 26),
        (f'{name} CM1', 'CC', 76, 5000000, 25),
        (f'{name} CM2', 'CC', 75, 4000000, 24),
        (f'{name} CAM', 'COC', 77, 8000000, 27),
        (f'{name} ST1', 'ATT', 78, 10000000, 28),
        (f'{name} ST2', 'ATT', 76, 6000000, 25),
        (f'{name} LW', 'AS', 76, 6000000, 26),
        (f'{name} RW', 'AD', 75, 5000000, 24),
        (f'{name} CB3', 'DC', 74, 3000000, 23),
        (f'{name} CM3', 'CC', 74, 3000000, 22)
    ]))

season_25 = {
    "season_id": "25",
    "season_name": "2024-2025",
    "teams": teams_25
}

with open('data/seasons/season_25.json', 'w', encoding='utf-8') as f:
    json.dump(season_25, f, indent=2, ensure_ascii=False)


# ================= FC 24 ================= #
# Utilizzo una copia di FC 25 con qualche aggiustamento (es. Salernitana, Frosinone, Sassuolo)
teams_24 = [ t for t in teams_25[:8] ]
other_teams_24 = ['Torino', 'Bologna', 'Genoa', 'Monza', 'Hellas Verona', 'Lecce', 'Udinese', 'Cagliari', 'Empoli', 'Frosinone', 'Sassuolo', 'Salernitana']
for idx, name in enumerate(other_teams_24):
    teams_24.append(build_team(name.lower().replace(' ', ''), name, 40, [
        (f'{name} GK', 'POR', 77, 6000000, 25),
        (f'{name} CB1', 'DC', 77, 6000000, 26),
        (f'{name} CB2', 'DC', 76, 5000000, 24),
        (f'{name} RB', 'TD', 76, 5000000, 24),
        (f'{name} LB', 'TS', 76, 5000000, 25),
        (f'{name} CDM', 'CDC', 77, 6000000, 26),
        (f'{name} CM1', 'CC', 76, 5000000, 25),
        (f'{name} CM2', 'CC', 75, 4000000, 24),
        (f'{name} CAM', 'COC', 77, 8000000, 27),
        (f'{name} ST1', 'ATT', 78, 10000000, 28),
        (f'{name} ST2', 'ATT', 76, 6000000, 25),
        (f'{name} LW', 'AS', 76, 6000000, 26),
        (f'{name} RW', 'AD', 75, 5000000, 24),
        (f'{name} CB3', 'DC', 74, 3000000, 23),
        (f'{name} CM3', 'CC', 74, 3000000, 22)
    ]))

season_24 = {
    "season_id": "24",
    "season_name": "2023-2024",
    "teams": teams_24
}

with open('data/seasons/season_24.json', 'w', encoding='utf-8') as f:
    json.dump(season_24, f, indent=2, ensure_ascii=False)

print("Scraping simulato e generazione dei dataset FC 24 e FC 25 completata con successo.")
