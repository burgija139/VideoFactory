import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# Podesi tvoje podatke za LOKALNU bazu
LOCAL_DB = {
    "dbname": "postgres",
    "user": "dusan_admin",
    "password": "pedri8-messi10", # Unesi svoju lozinku za lokalni Postgres
    "host": "localhost",
    "port": "5432"
}

# Supabase DATABASE_URL iz tvoje .env datoteke
SUPABASE_URL = os.getenv("DATABASE_URL")

if not SUPABASE_URL:
    print("Greška: DATABASE_URL nije pronađen u .env fajlu!")
    exit(1)

# Ovde definišemo filter - promeni 92 na 95 ako želiš da budeš još bezbedniji sa prostorom
POPULARITY_LIMIT = 92
RATING_LIMIT = 600

print("⏳ Povezujem se na lokalnu bazu i izvlačim puzle...")
try:
    local_conn = psycopg2.connect(**LOCAL_DB)
    local_cur = local_conn.cursor()
    
    # Izvlačimo podatke sa lokala prema tvom filteru
    local_cur.execute(f"""
        SELECT puzzle_id, fen, moves, rating, rating_deviation, popularity, nb_plays, themes, game_url, opening_tags
        FROM puzzles
        WHERE popularity >= {POPULARITY_LIMIT} AND rating >= {RATING_LIMIT};
    """)
    
    puzzles_data = local_cur.fetchall()
    total_puzzles = len(puzzles_data)
    print(f"✅ Uspešno izvučeno {total_puzzles} zagonetki sa lokala.")
    
    local_cur.close()
    local_conn.close()
except Exception as e:
    print(f"Greška pri čitanju sa lokalne baze: {e}")
    exit(1)

print("🚀 Povezujem se na Supabase i započinjem uvoz...")
try:
    supabase_conn = psycopg2.connect(SUPABASE_URL)
    supabase_cur = supabase_conn.cursor()
    
    # Upit za masovni insert na Supabase (menjaj 'chess_puzzles' ako ti se tabela gore zove drugačije)
    insert_query = """
        INSERT INTO chess_puzzles (puzzle_id, fen, moves, rating, rating_deviation, popularity, nb_plays, themes, game_url, opening_tags)
        VALUES %s
        ON CONFLICT (puzzle_id) DO NOTHING;
    """
    
    # Šaljemo u paketima od po 5000 komada da ne preopteretimo mrežu i memoriju
    batch_size = 5000
    for i in range(0, total_puzzles, batch_size):
        batch = puzzles_data[i:i+batch_size]
        execute_values(supabase_cur, insert_query, batch)
        supabase_conn.commit()
        print(f"📦 Ubačeno {i + len(batch)} / {total_puzzles} puzli na Cloud...")
        
    supabase_cur.close()
    supabase_conn.close()
    print("🎉 Migracija uspešno završena! Tvoj Supabase je spreman za VideoFactory.")

except Exception as e:
    print(f"Greška pri upisu na Supabase: {e}")