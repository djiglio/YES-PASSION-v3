import pandas as pd
import json
import os

print("Lettura del dataset FIFA 25 in corso...")
df = pd.read_csv('fifa_fbref_merged.csv', low_memory=False)

# Filtra solo FIFA 25 e Serie A
df = df[(df['fifa_version'] == 25) & (df['league_name'] == 'Serie A')]

# Filtra le squadre ecuadoriane
ecuadorian_teams = ['LDU Quito', 'Barcelona de Guayaquil']
df = df[~df['club_name'].isin(ecuadorian_teams)]

print(f"Estratti {len(df)} giocatori per la Serie A di FIFA 25.")

# Mappatura ruoli originale, convertendo ADA in AD e ASA in AS
ROLE_MAP = {
    'GK': 'POR',
    'CB': 'DC',
    'LB': 'TS',
    'RB': 'TD',
    'LWB': 'AS', # Convertito da ASA a AS
    'RWB': 'AD', # Convertito da ADA a AD
    'CDM': 'CDC',
    'CM': 'CC',
    'CAM': 'COC',
    'LM': 'ES',
    'RM': 'ED',
    'LW': 'AS',
    'RW': 'AD',
    'CF': 'AT',
    'ST': 'ATT'
}

def translate_roles(roles_str):
    if not isinstance(roles_str, str):
        return 'SCONOSCIUTO'
    roles = [r.strip() for r in roles_str.split(',')]
    translated = []
    for r in roles:
        mapped = ROLE_MAP.get(r, r)
        # Assicuriamoci che anche se arriva un ADA/ASA venga convertito
        if mapped == 'ADA': mapped = 'AD'
        if mapped == 'ASA': mapped = 'AS'
        translated.append(mapped)
    
    # Rimuoviamo duplicati
    return ', '.join(sorted(list(set(translated))))

def format_value(value_num):
    if pd.isna(value_num):
        return "€0"
    if value_num >= 1000000:
        return f"€{round(value_num/1000000, 1)}M"
    else:
        return f"€{round(value_num/1000)}K"

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
    def_roles = ['DC', 'TS', 'TD']
    gk_roles = ['POR']
    
    return {
        "att_ovr": calc_ovr(players, att_roles),
        "mid_ovr": calc_ovr(players, mid_roles),
        "def_ovr": calc_ovr(players, def_roles),
        "gk_ovr": calc_ovr(players, gk_roles)
    }

teams_data = []

# Raggruppa per squadra
for club_name, club_group in df.groupby('club_name'):
    players = []
    for _, row in club_group.iterrows():
        val_num = float(row['value_eur']) if not pd.isna(row['value_eur']) else 0.0
        players.append({
            "Nome": row['short_name'],
            "Ruolo": translate_roles(row['player_positions']),
            "Overall": int(row['overall']),
            "Potential": int(row['potential']),
            "Value": format_value(val_num),
            "ValueNum": val_num,
            "Age": int(row['age_fifa']) if not pd.isna(row['age_fifa']) else 25
        })
        
    teams_data.append({
        "id": str(club_name).lower().replace(' ', '').replace('fc', ''),
        "name": str(club_name),
        "real_points": 50, # Valore di default
        "squad_strength": calculate_squad_strength(players),
        "players": players
    })
    
season_json = {
    "season_id": "25",
    "season_name": "2024-2025",
    "teams": teams_data
}

os.makedirs('data/seasons', exist_ok=True)
file_path = 'data/seasons/season_25.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(season_json, f, indent=2, ensure_ascii=False)
    
print(f"Generato {file_path} con {len(teams_data)} squadre.")
