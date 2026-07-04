import json
import os

# Load season 21
with open('data/seasons/season_21.json', 'r', encoding='utf-8') as f:
    s21 = json.load(f)

# Load season 20 for Roma
with open('data/seasons/season_20.json', 'r', encoding='utf-8') as f:
    s20 = json.load(f)
roma = next(t for t in s20['teams'] if 'roma' in t['name'].lower())

# Load season 22 for Spezia
with open('data/seasons/season_22.json', 'r', encoding='utf-8') as f:
    s22 = json.load(f)
spezia = next(t for t in s22['teams'] if 'spezia' in t['name'].lower())

# Add to season 21
s21['teams'].append(roma)
s21['teams'].append(spezia)

# Save season 21
with open('data/seasons/season_21.json', 'w', encoding='utf-8') as f:
    json.dump(s21, f, indent=2, ensure_ascii=False)

print("Aggiunte Roma e Spezia a season_21.json. Ora ci sono 20 squadre.")
