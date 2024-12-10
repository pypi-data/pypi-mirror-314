import argparse
from .utils.generator import process_multiple_sql_files

def main():
    parser = argparse.ArgumentParser(description="Herramienta para generar esquemas Avro, JSON y SQL desde definiciones Oracle.")
    parser.add_argument("command", choices=["make"], help="Comando a ejecutar ('make')")
    parser.add_argument("schemas", nargs='?', default=None, help="subcomando 'schemas'")
    parser.add_argument("--input-folder", default="schemas/oracle", help="Carpeta de entrada con .sql")
    parser.add_argument("--avro-output-folder", default="schemas/avsc", help="Carpeta de salida Avro")
    parser.add_argument("--json-output-folder", default="schemas/json", help="Carpeta de salida JSON")
    parser.add_argument("--sql-output-folder", default="schemas/sql", help="Carpeta de salida SQL")
    parser.add_argument("--date-format", default="datetime", choices=["date","datetime"], help="Formato de fecha para campos DATE")

    args = parser.parse_args()

    if args.command == "make" and args.schemas == "schemas":
        process_multiple_sql_files(
            input_folder=args.input_folder,
            avro_output_folder=args.avro_output_folder,
            json_output_folder=args.json_output_folder,
            sql_output_folder=args.sql_output_folder,
            date_format=args.date_format
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
