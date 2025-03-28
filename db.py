# db.py
import os
import psycopg2
import time

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "globant_db"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "JuCarSua/1808"), 
                host=os.getenv("POSTGRES_HOST", "globantdbserver.postgres.database.azure.com"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                sslmode="require"
            )
            return conn
        except Exception as e:
            print(f"Error conexión al database: {e}")
            retries -= 1
            if retries == 0:
                return None
            print(f"Reintentando conexión... ({5 - retries}/5)")
            time.sleep(2)
    return None