import csv
from collections import defaultdict
from datetime import datetime

def validar_csv(ruta_archivo, columnas_esperadas, tabla):
    """
    Valida un archivo CSV y reporta problemas en las filas.
    
    Args:
        ruta_archivo (str): Ruta del archivo CSV.
        columnas_esperadas (int): Número de columnas esperadas.
        tabla (str): Nombre de la tabla (para personalizar las validaciones).
    
    Returns:
        dict: Resumen de la validación (filas válidas, inválidas, problemas detectados).
    """
    problemas = defaultdict(list)
    filas_validas = []
    
    with open(ruta_archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for i, fila in enumerate(lector, 1):
            # Verificar número de columnas
            if len(fila) != columnas_esperadas:
                problemas[f"Fila {i}: Número incorrecto de columnas"].append(fila)
                continue
            
            # Verificar si la primera columna (id) es numérica y no está vacía
            if not fila[0].strip():
                problemas[f"Fila {i}: Columna 1 (id) vacía"].append(fila)
                continue
            try:
                id_valor = int(fila[0])
            except ValueError:
                problemas[f"Fila {i}: Columna 1 (id) no es numérica"].append(fila)
                continue
            
            # Verificar valores vacíos o inválidos
            fila_procesada = []
            for j, valor in enumerate(fila):
                valor = valor.strip()
                if not valor:
                    problemas[f"Fila {i}: Columna {j+1} vacía"].append(fila)
                # Validaciones específicas para hired_employees
                if tabla == "hired_employees":
                    if j == 2 and valor:  # datetime
                        try:
                            datetime.fromisoformat(valor.replace('Z', '+00:00'))
                        except ValueError:
                            problemas[f"Fila {i}: Columna 3 (datetime) no tiene formato ISO 8601"].append(fila)
                    if j in (3, 4) and valor:  # department_id, job_id
                        try:
                            int(valor)
                        except ValueError:
                            problemas[f"Fila {i}: Columna {j+1} no es numérica"].append(fila)
                fila_procesada.append(valor)
            filas_validas.append(fila_procesada)
    
    return {
        "filas_validas": filas_validas,
        "problemas": dict(problemas),
        "total_filas": i
    }

# Ejemplo de uso
rutas_archivos = {
    "hired_employees": ("data/hired_employees.csv", 5),
    "departments": ("data/departments.csv", 2),
    "jobs": ("data/jobs.csv", 2)
}

if __name__ == "__main__":
    for tabla, (ruta, columnas) in rutas_archivos.items():
        resultado = validar_csv(ruta, columnas, tabla)
        print(f"Validación de {tabla}:")
        print(f"Total de filas: {resultado['total_filas']}")
        print(f"Filas válidas: {len(resultado['filas_validas'])}")
        print("Problemas encontrados:", resultado["problemas"])