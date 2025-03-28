# Globant's Data Engineering Coding Challenge

Este repositorio contiene mi solución al reto de Data Engineering de Globant. La solución incluye una API REST para migrar datos desde archivos CSV a una base de datos PostgreSQL, métricas específicas mediante consultas SQL, y un despliegue en Azure.

## Estructura del Proyecto

- `app.py`: Código principal de la API FastAPI.
- `db.py`: Funciones para la conexión a la base de datos.
- `init_db.py`: Script para inicializar las tablas en la base de datos.
- `test/test_api.py`: Pruebas automatizadas con `pytest`.
- `data/`: Carpeta con los archivos CSV (`departments.csv`, `jobs.csv`, `hired_employees.csv`).
- `Dockerfile`: Archivo para construir la imagen Docker de la API.
- `docker-compose.yml`: Archivo para orquestar la API y la base de datos con Docker Compose.

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

Despliegue en Azure
La API está desplegada en Azure App Service, y la base de datos está en Azure Database for PostgreSQL. Sigue estos pasos para replicar el despliegue:

Crea un grupo de recursos:
En el Azure Portal, busca "Resource groups" y crea uno llamado GlobantChallengeRG en la región "West US".
Crea un servidor PostgreSQL:
Busca "Azure Database for PostgreSQL" y crea un "Flexible Server".
Configura:
Nombre: globantdbserver
Región: "West US"
Versión: 16
Compute + storage: "Burstable", "B1ms"
Admin username: postgres
Password: Caballo123!
Connectivity method: "Public access"
Habilita acceso desde tu IP y desde servicios de Azure.
Crea una base de datos llamada globant_db.
Crea un Azure Container Registry:
Busca "Container Registries" y crea uno llamado globantacr.
Habilita el "Admin user" y anota las credenciales.

Sube la imagen Docker:
Autentica Docker:
bash

Contraer

Ajuste

Copiar
docker login globantacr.azurecr.io
Construye y sube la imagen:
bash

Contraer

Ajuste

Copiar
docker build -t globantacr.azurecr.io/globant-api:latest .
docker push globantacr.azurecr.io/globant-api:latest

Crea un App Service:
Busca "App Services" y crea uno.
Configura:
Nombre: globant-api-juanc1808
Publish: "Docker Container"
Operating System: "Linux"
Region: "West US"
App Service Plan: Crea uno nuevo ("GlobantAppServicePlan", "B1")
Image Source: "Azure Container Registry"
Registry: globantacr
Image: globant-api
Tag: latest

Configura las variables de entorno:
POSTGRES_HOST: globantdbserver.postgres.database.azure.com
POSTGRES_PORT: 5432
POSTGRES_USER: postgres
POSTGRES_PASSWORD: Caballo123!
POSTGRES_DB: globant_db

Endpoints
POST /cargar-csv/{nombre_tabla}: Carga datos desde un archivo CSV a la base de datos.
POST /insertar-lote: Inserta una lista de empleados en la base de datos.
GET /contrataciones-por-trimestre: Obtiene el número de empleados contratados por trimestre en 2021.
GET /departamentos-sobre-promedio: Obtiene los departamentos que contrataron más empleados que el promedio en 2021.
Notas
Los archivos CSV deben estar disponibles dentro del contenedor o subidos a un almacenamiento en la nube (como Azure Blob Storage) para que el endpoint /cargar-csv/{nombre_tabla} funcione en el despliegue.
En un entorno de producción, se deberían configurar reglas de firewall más estrictas para la base de datos y usar una red privada.