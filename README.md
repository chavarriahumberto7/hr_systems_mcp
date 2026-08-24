# People Systems MCP

Proyecto para gestionar y validar información de recursos humanos mediante archivos CSV y una capa HTTP con FastAPI. La estructura actual representa la Fase 3 del proyecto: datos, reglas de negocio, repositorio y API REST separadas por responsabilidades.

## Objetivo

Construir una base modular para People Systems con:

- validación de integridad de datos
- separación por capas (repository, service, API)
- pruebas automatizadas sobre los CSV
- una base lista para evolucionar hacia MCP o servicios más complejos

## Arquitectura actual

```text
people-systems-mcp/
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
├── __init__.py
├── exceptions.py
├── main.py
├── repository.py
├── schemas.py
├── services.py
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
└── venv/
```

## Capas del proyecto

### 1. Repository
Archivo: `repository.py`

- carga los CSV desde `data/`
- construye índices por ID
- expone acceso centralizado a empleados, organizaciones, posiciones y terminaciones

### 2. Services
Archivo: `services.py`

- contiene la lógica de negocio
- valida existencia de registros
- combina datos de diferentes entidades
- lanza excepciones de dominio, no HTTP

### 3. API / HTTP
Archivo: `main.py`

- expone endpoints con FastAPI
- delega la lógica a `services.py`
- transforma errores de dominio a `HTTPException`

### 4. Schemas
Archivo: `schemas.py`

- define los contratos de salida Pydantic
- usados por FastAPI para serializar respuestas y documentación

### 5. Exceptions
Archivo: `exceptions.py`

- concentra errores del dominio
- mantiene la capa de negocio desacoplada de FastAPI

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

## Ejecución de la API

```bash
uvicorn main:app --reload
```

Luego abre:

- http://127.0.0.1:8000/docs

## Ejecución de pruebas

```bash
pytest tests/test_data_consistency.py -v
```

## Validaciones actuales

La suite comprueba:

- unicidad de ids
- integridad de referencias internas
- autenticidad de managers
- ausencia de ciclos jerárquicos
- validación de `job_level`
- validación de `employment_status`
- coherencia entre empleados y terminaciones
- fechas válidas y lógicas

## Dependencias del proyecto

```txt
pytest==8.3.3
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

## Estado del proyecto

La Fase 3 ya quedó implementada con arquitectura por capas y acceso HTTP funcional. El proyecto está listo para seguir con una nueva etapa, por ejemplo:

- MCP tools
- validaciones de dominio más elaboradas
- persistencia real (DB)
- endpoints adicionales
- autenticación y seguridad

## Licencia

Este proyecto se entrega sin una licencia específica definida por el momento.
