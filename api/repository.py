"""
Capa de acceso a datos (Data Access / Repository).

Responsabilidad UNICA: leer los CSV y exponerlos como estructuras
en memoria, indexadas por su ID. No contiene reglas de negocio
(eso vive en services.py) ni nada relacionado con HTTP (eso vive
en main.py).

En una fase posterior, esta clase sera la unica pieza que cambie
cuando pasemos de CSV a otra fuente de datos.
"""

import csv
from pathlib import Path


class DataRepository:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

        self.employees = self._load("employees.csv")
        self.organizations = self._load("organizations.csv")
        self.positions = self._load("positions.csv")
        self.terminations = self._load("terminations.csv")

        # El CSV representa "sin valor" como cadena vacia; lo normalizamos
        # a None aqui, una sola vez, para que el resto de la app (y los
        # schemas Pydantic con tipo `str | None`) no tengan que lidiar
        # con cadenas vacias dispersas por todo el codigo.
        for employee in self.employees:
            if employee["manager_id"] == "":
                employee["manager_id"] = None
        for org in self.organizations:
            if org["parent_organization_id"] == "":
                org["parent_organization_id"] = None

        # Indices por ID para acceso O(1) en lugar de recorrer listas.
        self._employees_by_id = {e["employee_id"]: e for e in self.employees}
        self._organizations_by_id = {o["organization_id"]: o for o in self.organizations}
        self._positions_by_id = {p["position_id"]: p for p in self.positions}
        self._terminations_by_employee_id = {t["employee_id"]: t for t in self.terminations}

    def _load(self, filename: str) -> list[dict]:
        path = self.data_dir / filename
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    # --- Lecturas puntuales por ID -------------------------------------

    def get_employee(self, employee_id: str) -> dict | None:
        return self._employees_by_id.get(employee_id)

    def get_organization(self, organization_id: str) -> dict | None:
        return self._organizations_by_id.get(organization_id)

    def get_position(self, position_id: str) -> dict | None:
        return self._positions_by_id.get(position_id)

    def get_termination(self, employee_id: str) -> dict | None:
        return self._terminations_by_employee_id.get(employee_id)


# Instancia unica compartida por toda la app (los datos son de solo
# lectura, asi que cargarlos una vez al iniciar el proceso es suficiente).
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
repository = DataRepository(DATA_DIR)
