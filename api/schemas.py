"""
Esquemas de respuesta (Pydantic).

Estos modelos son el "contrato" publico de la API: definen
exactamente que campos devuelve cada endpoint y de que tipo son.
FastAPI los usa para serializar a JSON y para generar la
documentacion automatica en /docs.
"""

from pydantic import BaseModel


class EmployeeOut(BaseModel):
    employee_id: str
    name: str
    country: str
    organization_id: str
    position_id: str
    manager_id: str | None
    employment_status: str
    hire_date: str


class ManagerOut(BaseModel):
    employee_id: str
    manager: EmployeeOut | None


class JobOut(BaseModel):
    employee_id: str
    position_id: str
    title: str
    job_level: str
    organization_id: str


class TerminationOut(BaseModel):
    employee_id: str
    termination_date: str
    termination_reason: str
    termination_type: str
    last_working_day: str


class OrganizationOut(BaseModel):
    organization_id: str
    name: str
    country: str
    parent_organization_id: str | None
