def replace_template(template_file, dag_file):
    # Confirmar con el usuario si desea proceder
    confirmation = input(f"¿Está seguro de reemplazar el contenido de '{dag_file}' con el de '{template_file}'? (sí/no): ").lower()
    if confirmation not in ["sí", "s", "yes", "y"]:
        print("Operación cancelada.")
        return

    # Reemplazar el contenido
    try:
        with open(template_file, "r") as template:
            content = template.read()
        with open(dag_file, "w") as dag:
            dag.write(content)
        print(f"Contenido de '{dag_file}' reemplazado con éxito.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{template_file}' o '{dag_file}'.")
    except Exception as e:
        print(f"Error al reemplazar contenido: {e}")