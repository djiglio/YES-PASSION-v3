import json
import glob

# 1. Recupera Roma e Spezia originali da old_season_21.json
with open('old_season_21.json', 'r', encoding='utf-16') as f:
    old_s21 = json.load(f)

old_roma = next((t for t in old_s21['teams'] if 'roma' in t['name'].lower()), None)
old_spezia = next((t for t in old_s21['teams'] if 'spezia' in t['name'].lower()), None)

# Add Potential property if missing
for t in [old_roma, old_spezia]:
    if t:
        for p in t.get('players', []):
            if 'Potential' not in p:
                p['Potential'] = p['Overall']

# 2. Aggiorna season_21.json
with open('data/seasons/season_21.json', 'r', encoding='utf-8') as f:
    s21 = json.load(f)

# Rimuovi le finte Roma e Spezia che avevo iniettato
s21['teams'] = [t for t in s21['teams'] if 'roma' not in t['name'].lower() and 'spezia' not in t['name'].lower()]

# Inserisci quelle vere
if old_roma: s21['teams'].append(old_roma)
if old_spezia: s21['teams'].append(old_spezia)

with open('data/seasons/season_21.json', 'w', encoding='utf-8') as f:
    json.dump(s21, f, indent=2, ensure_ascii=False)

print("Roma e Spezia ripristinate dal vecchio dataset di FIFA 21.")

# 3. Sostituisci i ruoli ADA -> AD e ASA -> AS in TUTTI i file
files = glob.glob('data/seasons/season_*.json')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    modified = False
    for team in data.get('teams', []):
        for player in team.get('players', []):
            if 'Ruolo' in player:
                roles = player['Ruolo'].split(',')
                new_roles = []
                for r in roles:
                    r = r.strip()
                    if r == 'ADA':
                        new_roles.append('AD')
                        modified = True
                    elif r == 'ASA':
                        new_roles.append('AS')
                        modified = True
                    else:
                        new_roles.append(r)
                # Remove duplicates if a player had e.g. "AD, ADA"
                player['Ruolo'] = ', '.join(sorted(list(set(new_roles))))
                
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Ruoli aggiornati in {f}")

print("Tutte le sostituzioni sono state completate.")
