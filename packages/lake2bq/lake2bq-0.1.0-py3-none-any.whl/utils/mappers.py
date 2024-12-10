import re

def map_oracle_to_avro(column_type: str) -> str:
    """Mapea los tipos de Oracle a tipos Avro."""
    column_type = column_type.strip().upper()

    # Manejo de NUMBER(p,0) para distinguir int/long
    if re.match(r"NUMBER\((\d+),0\)", column_type):
        precision = int(re.search(r"NUMBER\((\d+),0\)", column_type).group(1))
        if precision <= 10:
            return "int"
        else:
            return "long"

    # Mapeos básicos
    mapping = {
        "DATE": "string",
        "VARCHAR2": "string",
        "NUMBER": "bytes"  # Si no se especifica precisión, se usa bytes
    }

    for oracle_type, avro_type in mapping.items():
        if column_type.startswith(oracle_type):
            return avro_type

    # Por defecto string
    return "string"
