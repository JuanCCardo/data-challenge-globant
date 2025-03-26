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
            name VARCHAR(255) NOT NULL,
            datetime TIMESTAMP NOT NULL,
            department_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL
        );
    """)

    # Crear tabla departments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            department VARCHAR(255) NOT NULL
        );
    """)

    # Crear tabla jobs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job VARCHAR(255) NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tablas creadas correctamente")

if __name__ == "__main__":
    init_db()