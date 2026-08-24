"""
Pruebas de consistencia para los datos mock de People Systems.

Estas pruebas NO validan MCP ni FastAPI todavia (eso llega en fases
posteriores). Solo validan que los CSV en data/ sean internamente
coherentes: que las claves foraneas existan, que no haya duplicados,
y que las reglas de negocio basicas (por ejemplo, que un empleado
Terminated tenga su registro de terminacion) se cumplan.

Ejecutar desde la raiz del proyecto con:
    pytest tests/test_data_consistency.py -v
"""

import csv
from datetime import datetime
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def organizations():
    return load_csv("organizations.csv")


@pytest.fixture(scope="module")
def positions():
    return load_csv("positions.csv")


@pytest.fixture(scope="module")
def employees():
    return load_csv("employees.csv")


@pytest.fixture(scope="module")
def terminations():
    return load_csv("terminations.csv")


# ---------------------------------------------------------------------
# organizations.csv
# ---------------------------------------------------------------------

def test_organization_ids_are_unique(organizations):
    ids = [org["organization_id"] for org in organizations]
    assert len(ids) == len(set(ids)), "Hay organization_id duplicados"


def test_organization_parent_references_are_valid(organizations):
    org_ids = {org["organization_id"] for org in organizations}
    for org in organizations:
        parent = org["parent_organization_id"]
        if parent:
            assert parent in org_ids, (
                f"{org['organization_id']} referencia un parent inexistente: {parent}"
            )


# ---------------------------------------------------------------------
# positions.csv
# ---------------------------------------------------------------------

def test_position_ids_are_unique(positions):
    ids = [pos["position_id"] for pos in positions]
    assert len(ids) == len(set(ids)), "Hay position_id duplicados"


def test_position_organization_references_are_valid(positions, organizations):
    org_ids = {org["organization_id"] for org in organizations}
    for pos in positions:
        assert pos["organization_id"] in org_ids, (
            f"{pos['position_id']} referencia una organizacion inexistente"
        )


VALID_JOB_LEVELS = {"Junior", "Mid", "Senior", "Executive"}


def test_position_job_level_is_valid(positions):
    for pos in positions:
        assert pos["job_level"] in VALID_JOB_LEVELS, (
            f"{pos['position_id']} tiene job_level invalido: {pos['job_level']}"
        )


# ---------------------------------------------------------------------
# employees.csv
# ---------------------------------------------------------------------

def test_employee_ids_are_unique(employees):
    ids = [emp["employee_id"] for emp in employees]
    assert len(ids) == len(set(ids)), "Hay employee_id duplicados"


def test_employee_organization_references_are_valid(employees, organizations):
    org_ids = {org["organization_id"] for org in organizations}
    for emp in employees:
        assert emp["organization_id"] in org_ids, (
            f"{emp['employee_id']} referencia una organizacion inexistente"
        )


def test_employee_position_references_are_valid(employees, positions):
    position_ids = {pos["position_id"] for pos in positions}
    for emp in employees:
        assert emp["position_id"] in position_ids, (
            f"{emp['employee_id']} referencia una posicion inexistente"
        )


def test_employee_position_matches_employee_organization(employees, positions):
    """Regla de negocio: la organizacion de la posicion debe coincidir
    con la organizacion del empleado que la ocupa."""
    position_org = {pos["position_id"]: pos["organization_id"] for pos in positions}
    for emp in employees:
        expected_org = position_org[emp["position_id"]]
        assert emp["organization_id"] == expected_org, (
            f"{emp['employee_id']} esta en {emp['organization_id']} pero su "
            f"posicion {emp['position_id']} pertenece a {expected_org}"
        )


def test_employee_manager_references_are_valid(employees):
    employee_ids = {emp["employee_id"] for emp in employees}
    for emp in employees:
        manager_id = emp["manager_id"]
        if manager_id:
            assert manager_id in employee_ids, (
                f"{emp['employee_id']} referencia un manager inexistente: {manager_id}"
            )
            assert manager_id != emp["employee_id"], (
                f"{emp['employee_id']} no puede ser su propio manager"
            )


def test_no_circular_management_chains(employees):
    """Sigue la cadena manager_id -> manager_id y falla si hay un ciclo."""
    manager_of = {emp["employee_id"]: emp["manager_id"] for emp in employees}
    for start_id in manager_of:
        seen = set()
        current = start_id
        while current:
            if current in seen:
                pytest.fail(f"Ciclo de management detectado empezando en {start_id}")
            seen.add(current)
            current = manager_of.get(current)


VALID_EMPLOYMENT_STATUSES = {"Active", "Terminated"}


def test_employment_status_is_valid(employees):
    for emp in employees:
        assert emp["employment_status"] in VALID_EMPLOYMENT_STATUSES, (
            f"{emp['employee_id']} tiene employment_status invalido"
        )


def test_hire_date_is_a_valid_date(employees):
    for emp in employees:
        datetime.strptime(emp["hire_date"], "%Y-%m-%d")


# ---------------------------------------------------------------------
# terminations.csv <-> employees.csv coherence
# ---------------------------------------------------------------------

def test_every_terminated_employee_has_a_termination_record(employees, terminations):
    terminated_ids = {
        emp["employee_id"] for emp in employees if emp["employment_status"] == "Terminated"
    }
    termination_ids = {t["employee_id"] for t in terminations}
    assert terminated_ids == termination_ids, (
        "Desalineacion entre employees Terminated y terminations.csv: "
        f"solo en employees={terminated_ids - termination_ids}, "
        f"solo en terminations={termination_ids - terminated_ids}"
    )


def test_termination_records_reference_valid_employees(employees, terminations):
    employee_ids = {emp["employee_id"] for emp in employees}
    for t in terminations:
        assert t["employee_id"] in employee_ids


def test_termination_ids_are_not_duplicated(terminations):
    ids = [t["employee_id"] for t in terminations]
    assert len(ids) == len(set(ids)), "Un mismo empleado tiene mas de un registro de terminacion"


def test_termination_date_is_after_hire_date(employees, terminations):
    hire_date_by_id = {emp["employee_id"]: emp["hire_date"] for emp in employees}
    for t in terminations:
        hire = datetime.strptime(hire_date_by_id[t["employee_id"]], "%Y-%m-%d")
        term = datetime.strptime(t["termination_date"], "%Y-%m-%d")
        assert term > hire, (
            f"{t['employee_id']}: termination_date no es posterior a hire_date"
        )
