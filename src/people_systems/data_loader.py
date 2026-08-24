from pathlib import Path
import csv


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_csv(filename: str) -> list[dict]:
    """Carga un CSV desde la carpeta data."""
    path = DATA_DIR / filename
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
