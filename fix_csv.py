import pandas as pd

def fix_encoding(s):
    if not isinstance(s, str):
        return s
    try:
        return s.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s

print("Reading CSV...")
df = pd.read_csv('final_merged_players.csv')

print("Fixing nome_giocatore...")
df['nome_giocatore'] = df['nome_giocatore'].apply(fix_encoding)

print("Fixing nazionalita...")
df['nazionalita'] = df['nazionalita'].apply(fix_encoding)

print("Fixing squadra...")
df['squadra'] = df['squadra'].apply(fix_encoding)

print("Saving CSV...")
df.to_csv('final_merged_players.csv', index=False, encoding='utf-8')
print("Done!")
