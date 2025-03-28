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

### 4. Sube la imagen Docker

- **NoAutentica Docker con ACR:*
   ```bash
   docker login globantacr.azurecr.io

Usa las credenciales del paso anterior.
- Construye y sube la imagen:
   ```bash
   docker build -t globantacr.azurecr.io/globant-api:latest .
   docker push globantacr.azurecr.io/globant-api:latest

### 5. Crear un App Service

**Busca "App Services" y crea uno nuevo**:
   - En el Azure Portal, busca "App Services" y selecciona "Create" para crear uno nuevo.

**Configura el App Service**:
   - Nombre: `globant-api-juanc1808`
   - Publish: `Docker Container`
   - Operating System: `Linux`
   - Region: `West US`
   - App Service Plan: Crea uno nuevo con:
     - Nombre: `GlobantAppServicePlan`
     - SKU: `B1`
   - Image Source: `Azure Container Registry`
   - Registry: `globantacr`
   - Image: `globant-api`
   - Tag: `latest`

### 6. Configura las variables de entorno


**Configura las variables de entorno**:
   - En el Azure Portal, ve a la sección "Configuration" del App Service y añade las siguientes variables:
     - `POSTGRES_HOST`: `globantdbserver.postgres.database.azure.com`
     - `POSTGRES_PORT`: `5432`
     - `POSTGRES_USER`: `postgres`
     - `POSTGRES_PASSWORD`: `XXXXX`
     - `POSTGRES_DB`: `globant_db`

### 7. Accede a la API

**Accede a la API**:
   - En el App Service, busca la URL (por ejemplo, `https://globant-api-juanc1808.azurewebsites.net`).
   - Abre la URL con `/docs` (por ejemplo, `https://globant-api-juanc1808.azurewebsites.net/docs`).


## Endpoints
La API ofrece los siguientes endpoints, accesibles en http://localhost:8000/docs localmente o en la URL del App Service tras el despliegue:

- POST /cargar-csv/{nombre_tabla}
Carga datos desde un archivo CSV a la base de datos.
Ejemplo: /cargar-csv/departments

-POST /insertar-lote
Inserta una lista de empleados en la base de datos.

Ejemplo de cuerpo de la solicitud:
   ```bash
   [{"id": 1, "name": "John Doe", "datetime": "2021-05-01T10:00:00Z", "department_id": 1, "job_id": 1}]


- GET /contrataciones-por-trimestre
Obtiene el número de empleados contratados por trimestre en 2021.

- GET /departamentos-sobre-promedio
Obtiene los departamentos que contrataron más empleados que el promedio en 2021.


## Notas
- **Archivos CSV:** Para que el endpoint /cargar-csv/{nombre_tabla} funcione en el despliegue, los archivos CSV (departments.csv, jobs.csv, hired_employees.csv) deben estar disponibles dentro del contenedor o subidos a un almacenamiento en la nube como Azure Blob Storage.
- **Seguridad en producción:** En un entorno de producción, configura reglas de firewall más estrictas para la base de datos y utiliza una red privada (e.g., Azure Virtual Network) para mayor seguridad.
- **Pruebas:** Las pruebas en test/test_api.py verifican la carga de datos CSV y la inserción de empleados en lotes. Asegúrate de ejecutarlas para validar la funcionalidad.