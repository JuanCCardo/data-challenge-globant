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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)