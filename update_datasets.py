import json
import glob
import re

files = glob.glob('data/seasons/*.json')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for team in data.get('teams', []):
        # Override specific names
        if team['name'] == 'AC Milan':
            team['name'] = 'Milan'
        if team['name'] == 'Hellas Verona FC':
            team['name'] = 'Hellas Verona'
            
        # Generate abbr
        clean_name = re.sub(r'[^A-Za-z]', '', team['name']).upper()
        
        # Ensure overrides are exactly as requested
        if team['name'] == 'Milan':
            team['abbr'] = 'MIL'
        elif team['name'] == 'Hellas Verona':
            team['abbr'] = 'HEL'
        else:
            team['abbr'] = clean_name[:3]
            
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated all seasons with team abbreviations.")
