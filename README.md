# People Systems MCP

Proyecto para validar la consistencia de datos de recursos humanos usando archivos CSV como fuente de verdad. La intención inicial del repositorio es modelar un sistema de People Systems con datos de organizaciones, posiciones, empleados y terminaciones, y verificar reglas de negocio básicas con pruebas automatizadas.

## Descripción

Este repositorio contiene un conjunto de datos mock y pruebas de integridad para asegurar que:

- cada identificador sea único
- las referencias entre entidades existan
- las posiciones pertenezcan a organizaciones válidas
- los managers existan y no creen ciclos
- los empleados terminados tengan un registro de terminación
- las fechas de contratación y baja sean consistentes

## Objetivo

Crear una base sólida para un futuro sistema MCP/servicio de datos de recursos humanos, con validaciones automatizadas sobre los datos de ejemplo antes de ampliar la funcionalidad.

## Estructura del proyecto

```text
people-systems-mcp/
├── data/
│   ├── employees.csv
│   ├── organizations.csv
│   ├── positions.csv
│   └── terminations.csv
├── tests/
│   └── test_data_consistency.py
├── .gitignore
├── requirements.txt
├── README.md
└── __init__.py
```

## Archivos de datos

- `organizations.csv`: organizaciones y jerarquía entre ellas
- `positions.csv`: posiciones por organización y nivel de trabajo
- `employees.csv`: empleados, organización, posición, manager y estatus
- `terminations.csv`: registros de terminación por empleado

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

3. Activa el entorno virtual:

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

## Ejecutar pruebas

```bash
pytest tests/test_data_consistency.py -v
```

## Reglas validadas actualmente

- IDs únicos por entidad
- referencias válidas de organizaciones, posiciones y empleados
- validación de `job_level`
- consistencia entre `employees` y `terminations`
- validación de fechas
- prevención de ciclos en la jerarquía de managers
- validación de estatus de empleo

## Estado del proyecto

Este repositorio se encuentra en una fase inicial de validación de datos. La siguiente etapa planeada es expandirlo con servicios MCP, APIs o modelos más estructurados para la gestión de personas y organizaciones.

## Contribución

Puedes contribuir agregando nuevas reglas de negocio, nuevos conjuntos de datos o pruebas más robustas para cubrir escenarios adicionales del sistema.

## Licencia

Este proyecto se distribuye sin una licencia específica por el momento.
