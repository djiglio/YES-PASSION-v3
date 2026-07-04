import json
import glob
import re

files = glob.glob('data/seasons/*.json')
teams = set()

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for team in data['teams']:
            teams.add(team['name'])

for name in sorted(teams):
    # Remove non-alphabetic characters and convert to upper, then take first 3
    clean_name = re.sub(r'[^A-Za-z]', '', name).upper()
    abbr = clean_name[:3]
    print(f"{name} -> {abbr}")
