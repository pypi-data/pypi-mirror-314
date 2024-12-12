import hashlib
from pathlib import Path
from typing import Any, Dict, List, Union

from tinybird.tb.modules.common import format_data_to_ndjson
from tinybird.tb.modules.datafile.parse_datasource import parse_datasource


def build_fixture_name(filename: str, datasource_name: str, datasource_content: str) -> str:
    """Generate a unique fixture name based on datasource properties.

    Args:
        datasource_name: Name of the datasource
        datasource_content: Content of the datasource file
        row_count: Number of rows requested

    Returns:
        str: A unique fixture name combining a hash of the inputs with the datasource name
    """

    doc = parse_datasource(filename, datasource_content)
    schema = doc.nodes[0].get("schema", "").strip()
    # Combine all inputs into a single string
    combined = f"{datasource_name}{schema}"

    # Generate hash
    hash_obj = hashlib.sha256(combined.encode())
    hash_str = hash_obj.hexdigest()[:8]

    # Return fixture name with hash
    return f"{datasource_name}_{hash_str}"


def get_fixture_dir() -> Path:
    fixture_dir = Path("fixtures")
    if not fixture_dir.exists():
        fixture_dir.mkdir()
    return fixture_dir


def persist_fixture(fixture_name: str, data: Union[List[Dict[str, Any]], str], format="ndjson") -> Path:
    fixture_dir = get_fixture_dir()
    fixture_file = fixture_dir / f"{fixture_name}.{format}"
    fixture_file.write_text(data if isinstance(data, str) else format_data_to_ndjson(data))
    return fixture_file


def load_fixture(fixture_name: str, format="ndjson") -> Union[Path, None]:
    fixture_dir = get_fixture_dir()
    fixture_file = fixture_dir / f"{fixture_name}.{format}"
    if not fixture_file.exists():
        return None
    return fixture_file
