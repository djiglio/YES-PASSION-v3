import os
import pandas as pd
import numpy as np
from supabase import create_client, Client
import time
import math

# ==========================================
# 1. INSERISCI QUI LE TUE CHIAVI SUPABASE
# ==========================================
SUPABASE_URL = "https://clnqodiqdawmcvawqxwt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsbnFvZGlxZGF3bWN2YXdxeHd0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjMyMTczNCwiZXhwIjoyMDk3ODk3NzM0fQ.u_3subxorTmTF60ToWu_nHjtSTQ4KZusENUIEz9uW6E"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 2. CARICAMENTO E PULIZIA DATI
# ==========================================
print("Lettura del dataset in corso...")
df = pd.read_csv('final_merged_players.csv')

# Assicuriamoci che i NaN di Pandas diventino None per il JSON di Supabase
df = df.replace({np.nan: None})
# Rinomina la colonna se c'è un indice residuo o per sicurezza
# Convertiamo il dataframe in una lista di dizionari
records = df.to_dict('records')

total_records = len(records)
print(f"Trovati {total_records} giocatori da importare.")

# ==========================================
# 3. CARICAMENTO A BLOCCHI (CHUNKS)
# ==========================================
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
            # Esegue l'inserimento
            response = supabase.table('players_history').insert(chunk_data).execute()
            print(f"[{i+1}/{chunks}] Inserite righe da {start_idx} a {end_idx-1} con successo!")
            success = True
        except Exception as e:
            print(f"Errore nel blocco {i+1}: {e}. Ritento... ({retries} tentativi rimasti)")
            retries -= 1
            time.sleep(2)
            
    if not success:
        print(f"ATTENZIONE: Fallito l'inserimento del blocco {i+1}. Procedo col successivo, ma i dati andranno controllati.")

print("Caricamento completato!")
