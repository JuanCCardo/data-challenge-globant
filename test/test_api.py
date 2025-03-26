from fastapi.testclient import TestClient
from app import app

cliente = TestClient(app)

def test_cargar_csv():
    respuesta = cliente.post("/cargar-csv/departments")
    assert respuesta.status_code == 200
    assert respuesta.json()["mensaje"].startswith("Datos de departments.csv cargados")

def test_insertar_lote():
    datos = [
        {
            "id": 5001,
            "name": "Usuario de Prueba",
            "datetime": "2021-08-01T10:00:00Z",
            "department_id": 1,
            "job_id": 1
        },
        {
            "id": 5002,
            "name": "",
            "datetime": "",
            "department_id": "",
            "job_id": ""
        }
    ]
    respuesta = cliente.post("/insertar-lote", json=datos)
    assert respuesta.status_code == 200
    assert respuesta.json()["mensaje"].startswith("2 empleados insertados")

def test_contrataciones_por_trimestre():
    respuesta = cliente.get("/contrataciones-por-trimestre")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

def test_departamentos_sobre_promedio():
    respuesta = cliente.get("/departamentos-sobre-promedio")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)