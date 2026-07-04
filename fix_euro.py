import glob
import json

files = glob.glob('data/seasons/season_*.json')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    modified = False
    for t in data.get('teams', []):
        for p in t.get('players', []):
            if 'Value' in p:
                val_str = p['Value']
                # If there's a weird character before the number, replace the whole non-digit prefix with €
                # Sometimes it's â‚¬, sometimes something else
                # We can just check if it starts with something other than '€'
                if not val_str.startswith('€'):
                    # Find the first digit
                    for i, char in enumerate(val_str):
                        if char.isdigit():
                            p['Value'] = '€' + val_str[i:]
                            modified = True
                            break

    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Aggiornati i valori in {f}")

print("Finito!")
