import json
from pathlib import Path
from typing import List, Dict, Any

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "products.json"
)


def read_products() -> List[Dict[str, Any]]:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Products JSON must contain a list")

    return data


def write_products(products: List[Dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    temp_file = DATA_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)

    # Replaces the original file after writing the new data.
    temp_file.replace(DATA_FILE)