# lake2bq

Esta herramienta genera esquemas Avro, archivos JSON de mapeo y consultas SQL a partir de archivos `.sql` con definiciones de tablas en Oracle.

## Uso

Instalar el paquete:
```bash
pip install lake2bq
```
Luego ejecutar:
```bash
lake2bq make schemas --input-folder schemas/oracle --avro-output-folder schemas/avsc --json-output-folder schemas/json --sql-output-folder schemas/sql
```

