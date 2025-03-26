import csv
from collections import defaultdict

def validar_csv(ruta_archivo, columnas_esperadas):
    """
    Valida un archivo CSV y reporta problemas en las filas.
    
    Args:
        ruta_archivo (str): Ruta del archivo CSV.
        columnas_esperadas (int): Número de columnas esperadas.
    
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
            
            # Verificar valores vacíos o inválidos
            fila_procesada = []
            for j, valor in enumerate(fila):
                valor = valor.strip()
                if not valor:
                    problemas[f"Fila {i}: Columna {j+1} vacía"].append(fila)
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
        resultado = validar_csv(ruta, columnas)
        print(f"Validación de {tabla}:")
        print(f"Total de filas: {resultado['total_filas']}")
        print(f"Filas válidas: {len(resultado['filas_validas'])}")
        print("Problemas encontrados:", resultado["problemas"])