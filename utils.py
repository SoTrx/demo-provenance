import json

from generated.ap_explanation.models.pg_json import PgJson
from generated.ap_explanation.models.pg_json_edge import PgJsonEdge
from generated.ap_explanation.models.pg_json_node import PgJsonNode


def load_pg_json_from_file(file_path: str) -> PgJson:
    """Load and deserialize a PgJson object from a JSON file."""
    with open(file_path) as f:
        raw = json.load(f)

    body = PgJson()
    body.nodes = [
        PgJsonNode(
            id=n["id"],
            labels=n["labels"],
            additional_data={"properties": n["properties"]} if n.get(
                "properties") else {},
        )
        for n in raw.get("nodes", [])
    ]
    body.edges = [
        PgJsonEdge(
            from_=e["from"],
            labels=e["labels"],
            to=e["to"],
            additional_data={"properties": e["properties"]} if e.get(
                "properties") else {},
        )
        for e in raw.get("edges", [])
    ]
    return body


def extract_sql_query(pg_json: PgJson) -> str | None:
    """Return the SQL query string from the Provenance_SQL_Operator node, or None if not found."""
    for node in pg_json.nodes or []:
        if node.labels and "Provenance_SQL_Operator" in node.labels:
            props = (node.additional_data or {}).get("properties", {})
            return props.get("query")
    return None


def extract_formula_expressions(provenance) -> list[str]:
    """Extract the formula semiring expression string from each result item."""
    results = (provenance.additional_data or {}).get("result", [])
    expressions = []
    for item in results:
        try:
            expr = item["provenance"]["formula"]["expression"]
            expressions.append(expr)
        except (KeyError, TypeError):
            pass
    return expressions
