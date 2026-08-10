import random

from infrastructure.db.db_context import DBContext


class PuzzleRepository:
    def __init__(self):
        self.db = DBContext()

    def get_random_puzzle(self):
        conn = self.db.connect()
        cur = conn.cursor()

        # Brza metoda: Prvo uzmemo ukupan broj redova (brzo radi jer ima indeks)
        # Menjaj 'chess_puzzles' ako se tabela na Supabase zove drugačije
        cur.execute("SELECT COUNT(*) FROM chess_puzzles;")
        total_rows = cur.fetchone()[0]

        if total_rows == 0:
            cur.close()
            conn.close()
            return None

        # Izaberemo nasumičan broj između 0 i ukupnog broja puzli
        random_offset = random.randint(0, total_rows - 1)

        # Skačemo direktno na taj red pomoću OFFSET-a - radi momentalno!
        cur.execute(f"""
            SELECT puzzle_id, fen, moves, rating, themes
            FROM chess_puzzles
            LIMIT 1 OFFSET {random_offset};
        """)

        row = cur.fetchone()

        cur.close()
        conn.close()

        # Vraća tuple: (puzzle_id, fen, moves, rating, themes)
        return row