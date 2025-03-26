from fastapi import FastAPI, HTTPException
import csv
from db import get_db_connection

app = FastAPI()

def insertar_datos_desde_csv(nombre_tabla: str, ruta_archivo: str):
    """
    Inserta datos desde un archivo CSV en la base de datos sin omitir filas.
    
    Args:
        nombre_tabla (str): Nombre de la tabla donde se insertarán los datos.
        ruta_archivo (str): Ruta del archivo CSV.
    
    Returns:
        dict: Mensaje de éxito con estadísticas.
    """
    conexion = get_db_connection()
    if conexion is None:
        raise HTTPException(status_code=500, detail="Fallo al conectar con la base de datos")

    cursor = conexion.cursor()
    filas_insertadas = 0
    filas_con_problemas = []

    try:
        with open(ruta_archivo, 'r') as archivo:
            lector = csv.reader(archivo)
            for i, fila in enumerate(lector, 1):
                if nombre_tabla == "hired_employees":
                    # Asegurar el número correcto de columnas
                    while len(fila) < 5:
                        fila.append('')
                    try:
                        # Convertir valores numéricos, permitiendo NULL si están vacíos
                        id_empleado = int(fila[0]) if fila[0].strip() else None
                        name = fila[1].strip() if fila[1].strip() else None
                        datetime_valor = fila[2].strip() if fila[2].strip() else None
                        department_id = int(fila[3]) if fila[3].strip() else None
                        job_id = int(fila[4]) if fila[4].strip() else None
                        
                        # Insertar la fila, incluso si hay valores vacíos
                        cursor.execute(
                            "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                            (id_empleado, name, datetime_valor, department_id, job_id)
                        )
                        filas_insertadas += 1
                    except ValueError as e:
                        filas_con_problemas.append(f"Fila {i}: Error de conversión - {str(e)}: {fila}")
                
                elif nombre_tabla == "departments":
                    while len(fila) < 2:
                        fila.append('')
                    try:
                        id_departamento = int(fila[0]) if fila[0].strip() else None
                        department = fila[1].strip() if fila[1].strip() else None
                        cursor.execute(
                            "INSERT INTO departments (id, department) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                            (id_departamento, department)
                        )
                        filas_insertadas += 1
                    except ValueError as e:
                        filas_con_problemas.append(f"Fila {i}: Error de conversión - {str(e)}: {fila}")
                
                elif nombre_tabla == "jobs":
                    while len(fila) < 2:
                        fila.append('')
                    try:
                        id_trabajo = int(fila[0]) if fila[0].strip() else None
                        job = fila[1].strip() if fila[1].strip() else None
                        cursor.execute(
                            "INSERT INTO jobs (id, job) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                            (id_trabajo, job)
                        )
                        filas_insertadas += 1
                    except ValueError as e:
                        filas_con_problemas.append(f"Fila {i}: Error de conversión - {str(e)}: {fila}")
                
                else:
                    raise HTTPException(status_code=400, detail="Nombre de tabla inválido")
        
        conexion.commit()
        mensaje = f"Datos de {nombre_tabla}.csv cargados: {filas_insertadas} filas insertadas"
        if filas_con_problemas:
            mensaje += f", {len(filas_con_problemas)} filas con problemas: {filas_con_problemas}"
        return {"mensaje": mensaje}
    
    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

@app.post("/cargar-csv/{nombre_tabla}")
def cargar_csv(nombre_tabla: str):
    """
    Endpoint para cargar datos desde un archivo CSV a la base de datos.

    Args:
        nombre_tabla (str): Nombre de la tabla donde se insertarán los datos.

    Returns:
        dict: Mensaje de éxito si los datos se cargan correctamente.

    Raises:
        HTTPException: Si el nombre de la tabla no es válido.
    """
    rutas_archivos = {
        "hired_employees": "data/hired_employees.csv",
        "departments": "data/departments.csv",
        "jobs": "data/jobs.csv"
    }
    if nombre_tabla not in rutas_archivos:
        raise HTTPException(status_code=400, detail="Nombre de tabla inválido")
    return insertar_datos_desde_csv(nombre_tabla, rutas_archivos[nombre_tabla])

@app.post("/insertar-lote")
def insertar_lote(empleados: list[dict]):
    """
    Endpoint para insertar una lista de empleados en la base de datos.

    Args:
        empleados (list[dict]): Lista de diccionarios con los datos de los empleados.

    Returns:
        dict: Mensaje de éxito si los datos se insertan correctamente.

    Raises:
        HTTPException: Si se intenta insertar más de 1000 filas a la vez.
    """
    if len(empleados) > 1000:
        raise HTTPException(status_code=400, detail="No se pueden insertar más de 1000 filas a la vez")
    
    conexion = get_db_connection()
    if conexion is None:
        raise HTTPException(status_code=500, detail="Fallo al conectar con la base de datos")

    cursor = conexion.cursor()
    filas_insertadas = 0
    filas_con_problemas = []

    try:
        for i, empleado in enumerate(empleados, 1):
            try:
                # Verificar que todas las claves necesarias estén presentes
                if not all(key in empleado for key in ["id", "name", "datetime", "department_id", "job_id"]):
                    filas_con_problemas.append(f"Registro {i}: Faltan claves - {empleado}")
                    continue
                try:
                    id_empleado = int(empleado["id"]) if empleado["id"] else None
                    departamento_id = int(empleado["department_id"]) if empleado["department_id"] else None
                    trabajo_id = int(empleado["job_id"]) if empleado["job_id"] else None
                except (ValueError, TypeError):
                    filas_con_problemas.append(f"Registro {i}: Error de conversión - {empleado}")
                    continue
                name = empleado["name"].strip() if empleado["name"] and empleado["name"].strip() else None
                datetime_valor = empleado["datetime"].strip() if empleado["datetime"] and empleado["datetime"].strip() else None
                
                cursor.execute(
                    "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                    (id_empleado, name, datetime_valor, departamento_id, trabajo_id)
                )
                filas_insertadas += 1
            except Exception as e:
                filas_con_problemas.append(f"Registro {i}: Error - {str(e)}: {empleado}")
        
        conexion.commit()
        mensaje = f"{filas_insertadas} empleados insertados exitosamente"
        if filas_con_problemas:
            mensaje += f", {len(filas_con_problemas)} registros con problemas: {filas_con_problemas}"
        return {"mensaje": mensaje}
    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

def obtener_contrataciones_por_trimestre():
    """
    Obtiene el número de empleados contratados por cada trabajo y departamento en 2021, dividido por trimestre.

    Returns:
        list: Lista de diccionarios con las contrataciones por trimestre.

    Raises:
        HTTPException: Si hay un error al conectar a la base de datos o al ejecutar la consulta.
    """
    conexion = get_db_connection()
    if conexion is None:
        raise HTTPException(status_code=500, detail="Fallo al conectar con la base de datos")

    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT 
                COALESCE(d.department, 'Unknown') as department,
                COALESCE(j.job, 'Unknown') as job,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) as Q1,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) as Q2,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) as Q3,
                SUM(CASE WHEN EXTRACT(MONTH FROM e.datetime) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) as Q4
            FROM hired_employees e
            LEFT JOIN departments d ON e.department_id = d.id
            LEFT JOIN jobs j ON e.job_id = j.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.department, j.job
            ORDER BY COALESCE(d.department, 'Unknown'), COALESCE(j.job, 'Unknown');
        """)
        filas = cursor.fetchall()
        resultado = [
            {
                "departamento": fila[0],
                "trabajo": fila[1],
                "Q1": int(fila[2]),
                "Q2": int(fila[3]),
                "Q3": int(fila[4]),
                "Q4": int(fila[5])
            }
            for fila in filas
        ]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

@app.get("/contrataciones-por-trimestre")
def contrataciones_por_trimestre():
    """
    Endpoint para obtener las contrataciones por trimestre en 2021.

    Returns:
        list: Lista de diccionarios con las contrataciones por trimestre.
    """
    return obtener_contrataciones_por_trimestre()

def obtener_departamentos_sobre_promedio():
    """
    Obtiene los departamentos que contrataron más empleados que el promedio en 2021.

    Returns:
        list: Lista de diccionarios con los departamentos que superan el promedio.

    Raises:
        HTTPException: Si hay un error al conectar a la base de datos o al ejecutar la consulta.
    """
    conexion = get_db_connection()
    if conexion is None:
        raise HTTPException(status_code=500, detail="Fallo al conectar con la base de datos")

    cursor = conexion.cursor()
    try:
        # Calcular el promedio de contrataciones en 2021
        cursor.execute("""
            SELECT AVG(cuenta_contrataciones)
            FROM (
                SELECT COUNT(*) as cuenta_contrataciones
                FROM hired_employees
                WHERE EXTRACT(YEAR FROM datetime) = 2021
                GROUP BY department_id
            ) as subconsulta;
        """)
        promedio_contrataciones = cursor.fetchone()[0]

        # Obtener departamentos por encima del promedio
        cursor.execute("""
            SELECT 
                COALESCE(d.id, 0) as id,
                COALESCE(d.department, 'Unknown') as department,
                COUNT(e.id) as contratados
            FROM hired_employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.id, d.department
            HAVING COUNT(e.id) > %s
            ORDER BY contratados DESC;
        """, (promedio_contrataciones,))
        filas = cursor.fetchall()
        resultado = [
            {
                "id": fila[0],
                "departamento": fila[1],
                "contratados": int(fila[2])
            }
            for fila in filas
        ]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

@app.get("/departamentos-sobre-promedio")
def departamentos_sobre_promedio():
    """
    Endpoint para obtener los departamentos con contrataciones por encima del promedio en 2021.

    Returns:
        list: Lista de diccionarios con los departamentos que superan el promedio.
    """
    return obtener_departamentos_sobre_promedio()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)