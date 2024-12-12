import re
def map_oracle_to_avro(column_type: str) -> dict:
    """Mapea los tipos de Oracle a tipos Avro, incluyendo soporte para decimal."""
    column_type = column_type.strip().upper()

    # Manejo de NUMBER(p, s)
    number_ps_match = re.match(r"NUMBER\((\d+),\s*(\d+)\)", column_type)
    if number_ps_match:
        precision, scale = map(int, number_ps_match.groups())
        if scale == 0:
            return "int" if precision <= 10 else "long"
        return {
            "type": "bytes",
            "logicalType": "decimal",
            "precision": precision,
            "scale": scale
        }

    # Mapeos básicos
    mapping = {
        "DATE": "string",
        "VARCHAR2": "string",
        "NUMBER": "long",  # Si no se especifica precisión ni escala, se usa long
    }

    for oracle_type, avro_type in mapping.items():
        if column_type.startswith(oracle_type):
            return avro_type

    # Por defecto string
    return "string"
