from db import get_db_connection

def init_db():
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    # Crear tabla hired_employees
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hired_employees (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            datetime TIMESTAMP,
            department_id INTEGER,
            job_id INTEGER
        );
    """)

    # Crear tabla departments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            department VARCHAR(255)
        );
    """)

    # Crear tabla jobs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job VARCHAR(255)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tablas creadas correctamente")

if __name__ == "__main__":
    init_db()