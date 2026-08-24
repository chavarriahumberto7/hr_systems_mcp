"""
Excepciones de dominio.

Se definen aqui, separadas de FastAPI, a proposito: la capa de
servicio no deberia saber que existe HTTP. Es la capa de rutas
(main.py) la que traduce estas excepciones a codigos de estado HTTP.
Esto es lo que hace posible, mas adelante, reutilizar services.py
desde el MCP Server sin arrastrar dependencias de FastAPI.
"""


class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: str):
        self.employee_id = employee_id
        super().__init__(f"Employee '{employee_id}' not found")


class OrganizationNotFoundError(Exception):
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        super().__init__(f"Organization '{organization_id}' not found")


class TerminationNotFoundError(Exception):
    def __init__(self, employee_id: str):
        self.employee_id = employee_id
        super().__init__(f"No termination record for employee '{employee_id}'")
