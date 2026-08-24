# People Systems MCP

Proyecto base para validar la consistencia de datos de recursos humanos usando archivos CSV como fuente primaria. La idea es crear una base modular para futuras integraciones MCP, servicios y automatizaciones sobre información de organizaciones, posiciones, empleados y terminaciones.

## Objetivo

Establecer un repositorio limpio con:

- datos de ejemplo realistas
- validaciones de integridad
- pruebas automatizadas
- una estructura de proyecto preparada para crecer

## Estructura del proyecto

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
├── .gitignore
├── README.md
├── requirements.txt
├── __init__.py
└── pytest.ini
```

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

## Ejecución de pruebas

```bash
pytest tests/test_data_consistency.py -v
```

## Validaciones implementadas

La suite actual comprueba:

- unicidad de IDs
- referencias válidas entre organizaciones, posiciones y empleados
- consistencia entre empleado y posición
- validación de `job_level`
- validación de `employment_status`
- control de ciclos en jerarquía de managers
- existencia de registro de terminación para empleados dados de baja
- fechas con formato y lógica coherente

## Estado actual

El proyecto se encuentra en una fase inicial de validación de datos. La estructura ya quedó preparada para expandirse hacia servicios, MCP o lógica más compleja de negocio.

## Próximos pasos sugeridos

- agregar modelos de dominio
- crear capa de servicio
- ampliar validaciones por negocio
- preparar endpoints o MCP tools
- documentar reglas de datos en `docs/`

## Licencia

Este proyecto se entrega sin una licencia específica definida por el momento.
