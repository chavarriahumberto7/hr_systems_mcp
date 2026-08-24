"""
Capa de logica de negocio (Business / Service layer).

Aqui viven las reglas de People Systems: como se relaciona un
empleado con su manager, su puesto, su organizacion y su
terminacion. Esta capa habla con el repositorio (repository.py)
pero NO sabe nada de HTTP, JSON, ni FastAPI -- por eso lanza
excepciones de dominio (exceptions.py) en lugar de HTTPException.

Esta separacion es intencional: en la Fase 4, el MCP Tool
get_employee() va a llamar a estas mismas funciones (o a su
version por HTTP en la Fase 5) sin que este archivo cambie.
"""

from .exceptions import (
    EmployeeNotFoundError,
    OrganizationNotFoundError,
    TerminationNotFoundError,
)
from .repository import DataRepository


def get_employee(repo: DataRepository, employee_id: str) -> dict:
    employee = repo.get_employee(employee_id)
    if employee is None:
        raise EmployeeNotFoundError(employee_id)
    return employee


def get_employee_manager(repo: DataRepository, employee_id: str) -> dict:
    """Devuelve el empleado y su manager (o None si no tiene, p.ej. la
    cabeza de la jerarquia). No tener manager NO es un error de
    negocio, asi que no se lanza excepcion en ese caso."""
    employee = get_employee(repo, employee_id)  # valida que el empleado exista
    manager_id = employee["manager_id"]
    manager = repo.get_employee(manager_id) if manager_id else None
    return {"employee_id": employee_id, "manager": manager}


def get_employee_job(repo: DataRepository, employee_id: str) -> dict:
    """Combina el empleado con los datos de su posicion actual."""
    employee = get_employee(repo, employee_id)
    position = repo.get_position(employee["position_id"])
    # position siempre deberia existir por integridad referencial
    # (lo garantiza tests/test_data_consistency.py), pero si algun
    # dia falla, preferimos un error explicito a un KeyError silencioso.
    if position is None:
        raise ValueError(
            f"Data integrity error: position '{employee['position_id']}' "
            f"referenced by employee '{employee_id}' does not exist"
        )
    return {
        "employee_id": employee_id,
        "position_id": position["position_id"],
        "title": position["title"],
        "job_level": position["job_level"],
        "organization_id": position["organization_id"],
    }


def get_employee_termination(repo: DataRepository, employee_id: str) -> dict:
    """Solo tiene sentido si el empleado existe Y tiene un registro de
    terminacion. Ambos casos son 'recurso no encontrado' desde la
    perspectiva de la API, pero con mensajes distintos."""
    get_employee(repo, employee_id)  # valida que el empleado exista
    termination = repo.get_termination(employee_id)
    if termination is None:
        raise TerminationNotFoundError(employee_id)
    return termination


def get_organization(repo: DataRepository, organization_id: str) -> dict:
    organization = repo.get_organization(organization_id)
    if organization is None:
        raise OrganizationNotFoundError(organization_id)
    return organization
