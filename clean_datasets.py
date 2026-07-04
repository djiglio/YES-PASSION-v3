import pandas as pd
import json
import math
import os

print("Lettura del dataset in corso...")
# Legge solo le righe della Serie A (league_id == 31.0)
iter_csv = pd.read_csv('male_players.csv', iterator=True, chunksize=10000)
df = pd.concat([chunk[chunk['league_id'] == 31.0] for chunk in iter_csv])

print(f"Estratti {len(df)} giocatori della Serie A.")

# Dizionario per tradurre i ruoli da Inglese a Italiano
ROLE_MAP = {
    'GK': 'POR',
    'CB': 'DC',
    'LB': 'TS',
    'RB': 'TD',
    'LWB': 'ASA',
    'RWB': 'ADA',
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
    translated = [ROLE_MAP.get(r, r) for r in roles]
    return ', '.join(translated)

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
    def_roles = ['DC', 'TS', 'TD', 'ADA', 'ASA']
    gk_roles = ['POR']
    
    return {
        "att_ovr": calc_ovr(players, att_roles),
        "mid_ovr": calc_ovr(players, mid_roles),
        "def_ovr": calc_ovr(players, def_roles),
        "gk_ovr": calc_ovr(players, gk_roles)
    }

os.makedirs('data/seasons', exist_ok=True)

# Raggruppa per edizione FIFA
for fifa_version, group in df.groupby('fifa_version'):
    version_int = int(fifa_version)
    season_name = f"20{version_int-1}-20{version_int}" if version_int >= 15 else f"20{version_int-1}-20{version_int}"
    if version_int < 10:
        season_name = f"200{version_int-1}-200{version_int}"
        
    teams_data = []
    
    # Raggruppa per squadra all'interno dell'edizione
    for club_name, club_group in group.groupby('club_name'):
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
                "Age": int(row['age']) if not pd.isna(row['age']) else 25
            })
            
        teams_data.append({
            "id": str(club_name).lower().replace(' ', ''),
            "name": str(club_name),
            "real_points": 50, # Valore di default
            "squad_strength": calculate_squad_strength(players),
            "players": players
        })
        
    season_json = {
        "season_id": str(version_int),
        "season_name": season_name,
        "teams": teams_data
    }
    
    file_path = f'data/seasons/season_{version_int}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(season_json, f, indent=2, ensure_ascii=False)
        
    print(f"Generato {file_path} con {len(teams_data)} squadre.")

print("Tutte le stagioni sono state generate con successo!")
