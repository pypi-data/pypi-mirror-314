import re
def map_oracle_to_avro(column_type: str) -> str:
    """Mapea los tipos de Oracle a tipos Avro."""
    column_type = column_type.strip().upper()

    # Manejo de NUMBER(p, s)
    number_ps_match = re.match(r"NUMBER\((\d+)\s*,\s*(\d+)\)", column_type)
    if number_ps_match:
        precision, scale = map(int, number_ps_match.groups())
        if scale == 0:
            # Si la escala es 0, determinar si es int o long basado en la precisión
            if precision <= 10:
                return "int"
            else:
                return "long"
        else:
            # Si la escala es mayor que 0, mapear a decimal
            return "decimal"

    # Manejo de NUMBER(p) asumiendo escala 0
    number_p_match = re.match(r"NUMBER\((\d+)\)", column_type)
    if number_p_match:
        precision = int(number_p_match.group(1))
        if precision <= 10:
            return "int"
        else:
            return "long"

    # Mapeos básicos
    mapping = {
        "DATE": "string",
        "VARCHAR2": "string",
        "NUMBER": "bytes"  # Si no se especifica precisión ni escala, se usa bytes
    }

    for oracle_type, avro_type in mapping.items():
        if column_type.startswith(oracle_type):
            return avro_type

    # Por defecto string
    return "string"
