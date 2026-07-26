import os
import psycopg2
from dotenv import load_dotenv

# Ovo učitava tvoj .env fajl gde se nalazi DATABASE_URL
load_dotenv()

class DBContext:

    def connect(self):
        # Samo proslediš ceo string iz .env-a i to je to
        return psycopg2.connect(os.getenv("DATABASE_URL"))