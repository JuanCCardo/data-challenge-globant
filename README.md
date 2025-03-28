# Globant's Data Engineering Coding Challenge

Este repositorio contiene mi solución al reto de Data Engineering de Globant. La solución incluye una API REST para migrar datos desde archivos CSV a una base de datos PostgreSQL, métricas específicas mediante consultas SQL, y un despliegue en Azure.

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y Ejecución Local](#instalación-y-ejecución-local)
- [Despliegue en Azure](#despliegue-en-azure)
- [Endpoints](#endpoints)
- [Notas](#notas)

## Estructura del Proyecto

- **`app.py`**: Código principal de la API FastAPI.
- **`db.py`**: Funciones para la conexión a la base de datos.
- **`init_db.py`**: Script para inicializar las tablas en la base de datos.
- **`test/test_api.py`**: Pruebas automatizadas con `pytest`.
- **`data/`**: Carpeta con los archivos CSV:
  - `departments.csv`
  - `jobs.csv`
  - `hired_employees.csv`
- **`Dockerfile`**: Archivo para construir la imagen Docker de la API.
- **`docker-compose.yml`**: Archivo para orquestar la API y la base de datos con Docker Compose.

## Requisitos

- Python 3.9+
- Docker y Docker Compose
- Una cuenta de Azure con una suscripción activa

## Instalación y Ejecución Local

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/JuanCCardo/data-challenge-globant.git
   cd data-challenge-globant

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt

4. **Levanta los contenedores con Docker Compose:**
   ```bash
   docker-compose up --build

5. **LInicializa la base de datos:**
Accede al contenedor de la API:
   ```bash
   docker-compose exec api bash
    
Ejecutar:
python init_db.py

6. Accede a la API:
Abre tu navegador y ve a http://localhost:8000/docs para probar los endpoints.

7. Ejecuta las pruebas automatizadas:
Dentro del contenedor de la API, ejecuta:
   ```bash
   pytest test/test_api.py -v


## Despliegue en Azure

La API está desplegada en Azure App Service, y la base de datos está en Azure Database for PostgreSQL. Sigue estos pasos para replicar el despliegue:

### 1. Crea un grupo de recursos

En el Azure Portal, busca **"Resource groups"** y crea uno con la siguiente configuración:

- **Nombre:** `GlobantChallengeRG`  
- **Región:** `West US`

### 2. Crea un servidor PostgreSQL

- **Servicio:** Azure Database for PostgreSQL Flexible Server  
- **Nombre:** `globantdbserver`  
- **Región:** `West US`  
- **Versión:** `16`  
- **Tipo:** `Burstable`, tamaño `B1ms`  
- **Usuario administrador:** `postgres`  
- **Contraseña:** `xxxxx`  
- **Método de conexión:** Public access  
- **Configuración adicional:**  
  - Habilita acceso desde tu IP  
  - Permite conexiones desde otros servicios de Azure  
- **Base de datos inicial:** `globant_db`

### 3. Crea un Azure Container Registry

- **Nombre:** `globantacr`  
- **Configuración:**  
  - Habilita la opción **Admin user**  
  - Anota las credenciales generadas (usuario y contraseña del registry)
