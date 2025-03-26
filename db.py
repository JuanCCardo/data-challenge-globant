import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="globant_db",
            user="postgres",
            password="caballo",
            host="localhost",
            port="5434"
        )
        return conn
    except Exception as e:
        print(f"Error conexión al database: {e}")
        return None