import os
import pandas as pd
import numpy as np
from supabase import create_client, Client
import time
import math

SUPABASE_URL = "https://clnqodiqdawmcvawqxwt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsbnFvZGlxZGF3bWN2YXdxeHd0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjMyMTczNCwiZXhwIjoyMDk3ODk3NzM0fQ.u_3subxorTmTF60ToWu_nHjtSTQ4KZusENUIEz9uW6E"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Tronco la tabella...")
# Attenzione: se neq non va, proveremo altri metodi
try:
    # Deleteremo a blocchi se neq non va.
    supabase.table('players_history').delete().neq('id', 0).execute()
    print("Tabella svuotata!")
except Exception as e:
    print("Errore nello svuotamento, proseguo sperando sia gia vuota o lo farai a mano:", e)

print("Lettura del dataset in corso...")
df = pd.read_csv('final_merged_players.csv')
df = df.replace({np.nan: None})
records = df.to_dict('records')

total_records = len(records)
print(f"Trovati {total_records} giocatori da importare.")

CHUNK_SIZE = 5000
chunks = math.ceil(total_records / CHUNK_SIZE)

print(f"Inizio caricamento su Supabase in {chunks} blocchi da {CHUNK_SIZE} righe...")

for i in range(chunks):
    start_idx = i * CHUNK_SIZE
    end_idx = min((i + 1) * CHUNK_SIZE, total_records)
    chunk_data = records[start_idx:end_idx]
    
    success = False
    retries = 3
    while not success and retries > 0:
        try:
            supabase.table('players_history').insert(chunk_data).execute()
            print(f"[{i+1}/{chunks}] Inserite righe da {start_idx} a {end_idx-1} con successo!")
            success = True
        except Exception as e:
            print(f"Errore nel blocco {i+1}: {e}. Ritento...")
            retries -= 1
            time.sleep(2)

print("Caricamento completato!")
