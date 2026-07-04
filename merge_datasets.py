import pandas as pd
import numpy as np
import unicodedata

def remove_accents(input_str):
    if pd.isna(input_str):
        return ""
    return unicodedata.normalize('NFKD', str(input_str)).encode('ASCII', 'ignore').decode('utf-8')

def format_season(val):
    try:
        start_year = 2000 + int(float(val)) - 1
        return f"{start_year}-{start_year+1}"
    except:
        return val

def format_season_fbref(val):
    try:
        s = str(int(val))
        if len(s) == 4:
            start_year = 2000 + int(s[:2])
            end_year = 2000 + int(s[2:])
            return f"{start_year}-{end_year}"
    except:
        pass
    return val

def format_value(val):
    if pd.isna(val) or str(val).strip() == '':
        return ""
    try:
        v = float(val)
        if v == 0:
            return "€0"
        if v >= 1_000_000:
            return f"€{v/1_000_000:g}M"
        elif v >= 1_000:
            return f"€{v/1_000:g}K"
        return f"€{v:g}"
    except:
        return str(val)

def generate_abbreviations(teams):
    abbrevs = {}
    used_abbrevs = set()
    
    ignore_words = {'fc', 'cf', 'sc', 'cd', 'as', 'ud', 'ac', 'rc', 'de', 'la', 'us', 'sv', 'sp', 'ca', 'sd', 'afc', 'fk', 'sk', 'nk', 'jk', 'fsv', 'tsg', 'vfl', 'ssv', 'sv', 'tus', 'bsc', 'fsv', 'sg', '1.', '2.', '3.'}
    
    for original_team in sorted(teams):
        if not isinstance(original_team, str):
            continue
            
        clean_name = remove_accents(original_team).upper()
        words = [w for w in clean_name.replace('-', ' ').replace('.', ' ').split() if w.lower() not in ignore_words and len(w) > 0]
        
        if not words:
            words = [w for w in clean_name.replace('-', ' ').replace('.', ' ').split() if len(w) > 0]
        
        if not words:
            continue
            
        if len(words) >= 3:
            cand = words[0][0] + words[1][0] + words[2][0]
        elif len(words) == 2:
            if len(words[1]) >= 2:
                cand = words[0][0] + words[1][:2]
            else:
                cand = (words[0][:2] + words[1][0]).ljust(3, 'A')
        else:
            cand = words[0][:3].ljust(3, 'A')
            
        original_cand = cand
        idx = 1
        while cand in used_abbrevs:
            full_str = "".join(words)
            if idx + 2 < len(full_str):
                cand = full_str[0] + full_str[idx] + full_str[idx+1]
                idx += 1
            else:
                cand = f"{original_cand[:2]}{idx}"
                idx += 1
        
        abbrevs[original_team] = cand
        used_abbrevs.add(cand)
        
    return abbrevs

def clean_team_name(name):
    if pd.isna(name): return name
    return str(name).strip()
    
def clean_league_name(name):
    if pd.isna(name): return name
    return str(name).strip()

def map_roles(positions_str):
    if pd.isna(positions_str): return ""
    
    role_map = {
        'GK': 'POR',
        'CB': 'DC', 'LCB': 'DC', 'RCB': 'DC',
        'LB': 'TS', 'LWB': 'TS',
        'RB': 'TD', 'RWB': 'TD',
        'CDM': 'CDC', 'LDM': 'CDC', 'RDM': 'CDC',
        'CM': 'CC', 'LCM': 'CC', 'RCM': 'CC',
        'CAM': 'COC', 'LAM': 'COC', 'RAM': 'COC',
        'LM': 'ES',
        'RM': 'ED',
        'LW': 'AS',
        'RW': 'AD',
        'ST': 'ATT', 'LS': 'ATT', 'RS': 'ATT',
        'CF': 'AT', 'LF': 'AT', 'RF': 'AT'
    }
    
    # Positions are usually comma separated like "RW, ST, LW"
    raw_positions = str(positions_str).replace(' ', '').split(',')
    mapped_roles = []
    for rp in raw_positions:
        if rp in role_map:
            mapped_roles.append(role_map[rp])
    
    # Remove duplicates preserving order
    seen = set()
    final_roles = [x for x in mapped_roles if not (x in seen or seen.add(x))]
    
    return " ".join(final_roles)

def contains_all_words(search_str, target_str):
    if not search_str or not target_str:
        return False
    # ignore initials with dots
    words = [w for w in search_str.replace('.', ' ').split() if len(w) > 1]
    if not words:
        words = [w for w in search_str.replace('.', ' ').split()]
    target_words = target_str.replace('.', ' ').split()
    return all(w in target_words for w in words)

def fix_encoding(s):
    if not isinstance(s, str): return s
    try:
        return s.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s

print("Loading data...")
df_hist = pd.read_csv(r'C:\Users\Edoardo\OneDrive\Desktop\YES PASSION - v2 multiplayer\male_players.csv', encoding='latin1', low_memory=False)
df_hist['short_name'] = df_hist['short_name'].apply(fix_encoding)
df_hist['long_name'] = df_hist['long_name'].apply(fix_encoding)
df_hist['nationality_name'] = df_hist['nationality_name'].apply(fix_encoding)
df_hist['club_name'] = df_hist['club_name'].apply(fix_encoding)

df_new = pd.read_csv(r'C:\Users\Edoardo\OneDrive\Desktop\YES PASSION - v2 multiplayer\fifa_fbref_merged.csv', low_memory=False)
df_new = df_new[df_new['season'] == 2425].copy()

print("Formatting data...")
df_hist['stagione'] = df_hist['fifa_version'].apply(format_season)
df_hist['squadra'] = df_hist['club_name'].apply(clean_team_name)
df_hist['lega'] = df_hist['league_name'].apply(clean_league_name)
df_hist['valore_di_mercato'] = df_hist['value_eur'].apply(format_value)
df_hist['eta'] = df_hist['age'].apply(lambda x: str(int(x)) if pd.notna(x) else "")
df_hist['id_univoco_giocatore'] = df_hist['player_id']
df_hist['nome_giocatore'] = df_hist['short_name']
df_hist['nazionalita'] = df_hist['nationality_name']
df_hist['ruolo'] = df_hist['player_positions'].apply(map_roles)

df_new['stagione'] = df_new['season'].apply(format_season_fbref)
df_new['squadra'] = df_new['club_name'].apply(clean_team_name)
df_new['lega'] = df_new['league_name'].apply(clean_league_name)
df_new['valore_di_mercato'] = df_new['value_eur'].apply(format_value)
df_new['eta'] = df_new['age_fifa'].apply(lambda x: str(int(x)) if pd.notna(x) else "")
df_new['nazionalita'] = df_new['nationality_name']
df_new['ruolo'] = df_new['player_positions'].apply(map_roles)

print("Matching players...")
historical_players = {}
historical_players_by_nat = {}

for _, row in df_hist.drop_duplicates(subset=['player_id']).iterrows():
    p_id = row['player_id']
    s_name = row['short_name']
    l_name = row['long_name']
    nat = row['nationality_name']
    
    if not pd.notna(nat):
        continue
        
    nat_lower = str(nat).lower()
    if nat_lower not in historical_players_by_nat:
        historical_players_by_nat[nat_lower] = []
        
    s_clean = remove_accents(str(s_name)).lower() if pd.notna(s_name) else ""
    l_clean = remove_accents(str(l_name)).lower() if pd.notna(l_name) else ""
    
    historical_players_by_nat[nat_lower].append({
        'p_id': p_id,
        's_name': s_name,
        's_clean': s_clean,
        'l_clean': l_clean
    })
    
    if s_clean:
        historical_players[(s_clean, nat_lower)] = (p_id, s_name)
    if l_clean:
        historical_players[(l_clean, nat_lower)] = (p_id, s_name)

max_id = df_hist['player_id'].max() if not df_hist.empty else 0

new_ids = []
new_names = []

for _, row in df_new.iterrows():
    s_name = row['short_name']
    l_name = row['long_name']
    p_name = row['player']
    nat = row['nationality_name']
    
    matched = False
    
    s_clean = remove_accents(str(s_name)).lower() if pd.notna(s_name) else ""
    l_clean = remove_accents(str(l_name)).lower() if pd.notna(l_name) else ""
    p_clean = remove_accents(str(p_name)).lower() if pd.notna(p_name) else ""
    nat_lower = str(nat).lower() if pd.notna(nat) else ""
    
    # Try exact matches
    for check_n in [s_clean, l_clean, p_clean]:
        if not matched and check_n and (check_n, nat_lower) in historical_players:
            new_ids.append(historical_players[(check_n, nat_lower)][0])
            new_names.append(historical_players[(check_n, nat_lower)][1])
            matched = True
            break
            
    # Fallback fuzzy match
    if not matched and nat_lower in historical_players_by_nat:
        for hist_p in historical_players_by_nat[nat_lower]:
            h_s = hist_p['s_clean']
            h_l = hist_p['l_clean']
            
            # Word by word inclusion
            if (s_clean and contains_all_words(s_clean, h_l)) or \
               (l_clean and contains_all_words(l_clean, h_l)) or \
               (p_clean and contains_all_words(p_clean, h_l)) or \
               (h_s and contains_all_words(h_s, s_clean)) or \
               (h_s and contains_all_words(h_s, l_clean)) or \
               ('vini' in s_clean and 'jr' in s_clean and 'vinicius' in h_l and 'junior' in h_l):
                new_ids.append(hist_p['p_id'])
                new_names.append(hist_p['s_name'])
                matched = True
                break
            
    if not matched:
        max_id += 1
        new_ids.append(max_id)
        if pd.notna(s_name) and " " in str(s_name):
            parts = str(s_name).split()
            if len(parts) >= 2 and len(parts[0]) > 1:
                s_name = f"{parts[0][0]}. {' '.join(parts[1:])}"
        new_names.append(s_name)

df_new['id_univoco_giocatore'] = new_ids
df_new['nome_giocatore'] = new_names

cols = ['stagione', 'id_univoco_giocatore', 'nome_giocatore', 'squadra', 'lega', 'overall', 'valore_di_mercato', 'eta', 'nazionalita', 'ruolo']
df_hist_final = df_hist[cols].copy()
df_new_final = df_new[cols].copy()

final_df = pd.concat([df_hist_final, df_new_final], ignore_index=True)

print("Generating abbreviations...")
all_teams = final_df['squadra'].dropna().unique()
abbrevs = generate_abbreviations(all_teams)
final_df['abbreviazione_squadra'] = final_df['squadra'].map(abbrevs)

print("Calculating potential...")
final_df = final_df.sort_values(['id_univoco_giocatore', 'stagione'])
final_df['next_overall'] = final_df.groupby('id_univoco_giocatore')['overall'].shift(-1)

def calculate_potential(row):
    if pd.notna(row['next_overall']):
        return row['next_overall']
    try:
        age = int(row['eta'])
    except:
        return row['overall']
    if age >= 32:
        return row['overall'] - 3
    elif age <= 19:
        return row['overall'] + 2
    else:
        return row['overall']

final_df['potenziale'] = final_df.apply(calculate_potential, axis=1)
final_df['potenziale'] = final_df['potenziale'].astype(int, errors='ignore')
final_df = final_df.drop(columns=['next_overall'])

final_cols = ['stagione', 'id_univoco_giocatore', 'nome_giocatore', 'ruolo', 'squadra', 'abbreviazione_squadra', 'lega', 'overall', 'potenziale', 'valore_di_mercato', 'eta', 'nazionalita']
final_df = final_df[final_cols]

final_df = final_df.drop_duplicates()

print("Saving final dataset...")
final_df.to_csv(r'C:\Users\Edoardo\OneDrive\Desktop\YES PASSION - v2 multiplayer\final_merged_players.csv', index=False, encoding='utf-8')
print("Done!")
