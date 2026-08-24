# People Systems MCP

Proyecto para gestionar datos de recursos humanos usando archivos CSV y una API REST con FastAPI. La versión actual ya está funcionando correctamente y refleja la estructura final de la Fase 3 del proyecto.

## Objetivo

Crear una base modular para People Systems con:

- datos de ejemplo reales y estructurados
- validaciones de integridad sobre CSV
- arquitectura por capas
- API FastAPI funcional para consultar empleados, organizaciones y terminaciones

## Estructura actual del repositorio

```text
people-systems-mcp/
├── api/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── main.py
│   ├── repository.py
│   ├── schemas.py
│   └── services.py
├── data/
│   ├── employees.csv
│   ├── organizations.csv
│   ├── positions.csv
│   └── terminations.csv
├── docs/
├── src/
│   └── people_systems/
│       ├── __init__.py
│       ├── data_loader.py
│       └── validators.py
├── tests/
│   └── test_data_consistency.py
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
├── __init__.py
└── venv/
```

## Capas del proyecto

### API
Carpeta: `api/`

- `api/main.py`: aplica FastAPI y define los endpoints HTTP
- `api/services.py`: lógica de negocio
- `api/repository.py`: acceso a archivos CSV
- `api/schemas.py`: modelos de salida Pydantic
- `api/exceptions.py`: excepciones de dominio

### Datos
Carpeta: `data/`

Contiene los CSV base:

- `employees.csv`
- `organizations.csv`
- `positions.csv`
- `terminations.csv`

### Validaciones
Archivo: `tests/test_data_consistency.py`

Comprueba:

- unicidad de ids
- referencias válidas entre entidades
- validez de `job_level`
- consistencia de `employment_status`
- ausencia de ciclos en managers
- integridad entre empleados y terminaciones
- fechas coherentes

## Endpoints activos

La API ya está funcionando con FastAPI y expone endpoints como:

- `GET /employees/{employee_id}`
- `GET /employees/{employee_id}/manager`
- `GET /employees/{employee_id}/job`
- `GET /employees/{employee_id}/termination`
- `GET /organizations/{organization_id}`

Documentación automática disponible en:

- http://127.0.0.1:8000/docs

## Requisitos

- Python 3.10+
- pip

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/chavarriahumberto7/hr_systems_mcp.git
cd hr_systems_mcp
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

4. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn api.main:app --reload
```

## Ejecutar pruebas

```bash
pytest tests/test_data_consistency.py -v
```

## Dependencias actuales

```txt
pytest==8.3.3
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

## Estado actual

La versión actual ya funciona correctamente con FastAPI y tiene la estructura de proyecto lista para seguir con nuevas fases, por ejemplo:

- MCP tools
- autenticación
- persistencia real
- más endpoints y servicios
- integración con base de datos

## Licencia

Este proyecto se entrega sin una licencia específica definida por el momento.
