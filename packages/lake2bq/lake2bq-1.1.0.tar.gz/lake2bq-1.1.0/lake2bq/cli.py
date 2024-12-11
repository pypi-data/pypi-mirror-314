import argparse
import os
from .utils.generator import process_multiple_sql_files
from .utils.templates import replace_template

def main():
    parser = argparse.ArgumentParser(description="Herramienta para generar esquemas Avro, JSON y SQL desde archivos SQL")
    parser.add_argument("command", choices=["make"], help="Comando a ejecutar ('make')")
    parser.add_argument("schemas", nargs="?", default=None, help="Subcomando 'schemas'")
    parser.add_argument("template", nargs="?", default=None, help="Subcomando template'")
    parser.add_argument("--type", default="oracle", choices=["oracle", "api"], help="tipo de template")
    parser.add_argument("--input-folder", default="schemas/oracle", help="Carpeta de entrada con .sql")
    parser.add_argument("--avro-output-folder", default="schemas/avsc", help="Carpeta de salida Avro")
    parser.add_argument("--json-output-folder", default="schemas/json", help="Carpeta de salida JSON")
    parser.add_argument("--sql-output-folder", default="sql/oracle", help="Carpeta de salida SQL")
    parser.add_argument("--date-format", default="datetime", choices=["date", "datetime"], help="Formato de fechas")

    args = parser.parse_args()

    if args.command == "make":
        if args.schemas == "schemas":
            print("Generando esquemas...")
            process_multiple_sql_files(
                input_folder=args.input_folder,
                avro_output_folder=args.avro_output_folder,
                json_output_folder=args.json_output_folder,
                sql_output_folder=args.sql_output_folder,
                date_format=args.date_format,
            )
        elif args.template == "template":
            print("Generando template...")
            template_file = ""
            dag_file = ""
            # Determinar si es `template oracle` o `template api`
            if "oracle" == args.type:
                template_file = "./templates/oracle.py"
            elif "api" == args.type:
                template_file = "./templates/api.py"
            else:
                print("Error: Debe especificar 'oracle' o 'api' en el subcomando.")
                return

            # Buscar el archivo `dag_` en la raíz
            for file in os.listdir("."):
                if file.startswith("dag_"):
                    dag_file = file
                    break

            if not dag_file:
                print("Error: No se encontró un archivo que comience con 'dag_' en la raíz.")
                return

            # Reemplazar el contenido
            replace_template(template_file, dag_file)
        else:
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
