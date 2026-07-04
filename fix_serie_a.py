import pandas as pd

italian_teams = [
    'Udinese', 'Sassuolo', 'Juventus', 'Milan', 'Roma', 'Hellas Verona', 'Empoli',
    'Torino', 'Atalanta', 'Bologna', 'Lazio', 'Fiorentina', 'Napoli', 'Como',
    'Inter', 'Frosinone', 'Cagliari', 'Genoa', 'Salernitana', 'Lecce', 'Monza',
    'AC Milan', 'Parma', 'Hellas Verona FC', 'Venezia', 'Sampdoria', 'Spezia',
    'Crotone', 'Benevento', 'SPAL', 'Chievo Verona', 'Palermo', 'Pescara',
    'Carpi', 'Cesena', 'Brescia', 'Catania', 'Siena', 'Livorno', 'Novara', 'Bari', 'Reggina', 'Cremonese'
]

print("Reading CSV...")
df = pd.read_csv('final_merged_players.csv')

def fix_serie_a(row):
    if row['lega'] == 'Serie A':
        # If the team is not in the known Italian list, rename it
        if row['squadra'] not in italian_teams:
            return 'Serie A Brasil'
    return row['lega']

df['lega'] = df.apply(fix_serie_a, axis=1)

print("Saving CSV...")
df.to_csv('final_merged_players.csv', index=False, encoding='utf-8')
print("Done!")
