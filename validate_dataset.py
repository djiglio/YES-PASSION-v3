import json, glob

files = glob.glob('data/seasons/season_*.json')
files.sort()

valid_roles = {'POR', 'DC', 'TS', 'TD', 'ASA', 'ADA', 'CDC', 'CC', 'COC', 'ES', 'ED', 'AS', 'AD', 'AT', 'ATT'}
all_teams = set()
roles_found = set()
anomalies = []

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        teams = data.get('teams', [])
        
        # Check team count
        if len(teams) != 20:
            anomalies.append(f"{f} ha {len(teams)} squadre invece di 20")
            
        for t in teams:
            all_teams.add(t['name'])
            for p in t.get('players', []):
                roles = [r.strip() for r in p['Ruolo'].split(',')]
                for r in roles:
                    roles_found.add(r)
                    if r not in valid_roles:
                        anomalies.append(f"Ruolo non valido '{r}' nel giocatore {p['Nome']} in {f}")

print('Squadre uniche trovate in tutte le stagioni:')
for team in sorted(list(all_teams)):
    print(f"- {team}")

print('\nRuoli trovati in tutte le stagioni:')
print(sorted(list(roles_found)))

print('\nAnomalie:')
if not anomalies:
    print("Nessuna anomalia trovata!")
else:
    for a in anomalies[:20]:
        print(a)
    if len(anomalies) > 20:
        print(f"... e altre {len(anomalies) - 20} anomalie")
