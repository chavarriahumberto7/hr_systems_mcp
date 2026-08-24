"""
Capa de rutas (Routes / HTTP layer).

Responsabilidad: exponer endpoints HTTP, delegar TODO el trabajo real
a services.py, y traducir excepciones de dominio a codigos de estado
HTTP. Esta capa no contiene logica de negocio ni sabe nada de MCP.

Ejecutar desde la raiz del proyecto con:
    uvicorn api.main:app --reload
"""

from fastapi import FastAPI, HTTPException

from . import services
from .exceptions import (
    EmployeeNotFoundError,
    OrganizationNotFoundError,
    TerminationNotFoundError,
)
from .repository import repository
from .schemas import EmployeeOut, JobOut, ManagerOut, OrganizationOut, TerminationOut

app = FastAPI(
    title="People Systems Mock API",
    description="API REST mock sobre datos CSV ficticios. No conoce MCP.",
    version="0.1.0",
)


@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def read_employee(employee_id: str):
    try:
        return services.get_employee(repository, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/employees/{employee_id}/manager", response_model=ManagerOut)
def read_employee_manager(employee_id: str):
    try:
        return services.get_employee_manager(repository, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/employees/{employee_id}/job", response_model=JobOut)
def read_employee_job(employee_id: str):
    try:
        return services.get_employee_job(repository, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/employees/{employee_id}/termination", response_model=TerminationOut)
def read_employee_termination(employee_id: str):
    try:
        return services.get_employee_termination(repository, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TerminationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/organizations/{organization_id}", response_model=OrganizationOut)
def read_organization(organization_id: str):
    try:
        return services.get_organization(repository, organization_id)
    except OrganizationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
