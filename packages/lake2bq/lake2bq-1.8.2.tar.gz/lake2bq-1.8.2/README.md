### README.md

```markdown
# Lake2BQ - Generador de Esquemas Avro, JSON y SQL

Lake2BQ es una herramienta diseñada para generar esquemas en formato Avro, JSON y SQL a partir de definiciones de tablas de Oracle en formato `.sql`. Este proyecto permite automatizar la creación de esquemas y la configuración de plantillas para tareas personalizadas.

## Comandos disponibles

El flujo recomendado es ejecutar primero `make template` para configurar la plantilla y luego `make schemas` para generar los esquemas.

---

### 1. `make template`

El comando `make template` configura las plantillas necesarias para trabajar con DAGs. Este comando sobrescribe el contenido de un archivo que comience con `dag_` en la raíz del proyecto con el contenido de una plantilla predefinida.

#### Uso

```bash
lake2bq make template --type {oracle|api}
```

#### Argumentos

- `--type`: Especifica el tipo de plantilla a utilizar. Las opciones disponibles son:
  - `oracle`: Configura la plantilla para trabajar con esquemas de Oracle.
  - `api`: Configura la plantilla para trabajar con APIs.

#### Ejemplo

```bash
lake2bq make template --type oracle
```

#### Notas

- El archivo `dag_` debe estar presente en la raíz del proyecto. Si no se encuentra, se mostrará un mensaje de error.
- Este comando debe ejecutarse antes de generar los esquemas.

---

### 2. `make schemas`

El comando `make schemas` genera los esquemas en formato Avro, JSON y SQL a partir de definiciones de tablas en archivos `.sql`.

#### Uso

```bash
lake2bq make schemas 
```

#### Argumentos

- `--input-folder`: Carpeta donde se encuentran los archivos `.sql`. Valor por defecto: `schemas/oracle`.
- `--avro-output-folder`: Carpeta donde se guardarán los archivos en formato Avro. Valor por defecto: `schemas/avsc`.
- `--json-output-folder`: Carpeta donde se guardarán los archivos en formato JSON. Valor por defecto: `schemas/json`.
- `--sql-output-folder`: Carpeta donde se guardarán los archivos en formato SQL. Valor por defecto: `sql/oracle`.
- `--date-format`: Especifica el formato de las fechas. Opciones:
  - `date`
  - `datetime` (valor por defecto)

#### Ejemplo

```bash
lake2bq make schemas --input-folder schemas/oracle --avro-output-folder schemas/avsc
```

#### Notas

- Es obligatorio que haya al menos un esquema de tabla de Oracle disponible en la carpeta especificada por `--input-folder`.
- Los esquemas generados se guardarán en las carpetas de salida especificadas.

---

## Flujo recomendado de ejecución

1. **Configurar la plantilla**:

   Ejecuta el comando `make template` para configurar la plantilla correspondiente:

   ```bash
   lake2bq make template --type oracle
   ```

2. **Generar los esquemas**:

   Una vez configurada la plantilla, genera los esquemas necesarios ejecutando:

   ```bash
   lake2bq make schemas 
   ```

---

## Requisitos

- Python 3.6 o superior.
- Archivos `.sql` con la definición de las tablas en formato Oracle.

---

## Mensajes de error comunes

1. **Error: No se encontró un archivo que comience con `dag_` en la raíz**:
   - Asegúrate de que un archivo con prefijo `dag_` esté presente en la raíz del proyecto antes de ejecutar `make template`.

2. **Error: No se encontró el archivo de plantilla**:
   - Asegúrate de que el paquete se instaló correctamente y que incluye la carpeta `templates`.

3. **Error: No hay esquemas disponibles**:
   - Verifica que haya al menos un archivo `.sql` en la carpeta especificada por `--input-folder`.

---

## Instalación y ejecución

1. Clona este repositorio.
2. Instala el paquete:
   ```bash
   pip install .
   ```
3. Usa los comandos descritos anteriormente para trabajar con las plantillas y generar los esquemas.

---

## Contribuciones

¡Se aceptan contribuciones! Si encuentras un problema o tienes sugerencias, por favor abre un issue o envía un pull request.

---

## Licencia

Este proyecto está bajo la licencia MIT.
```

### Explicación del contenido

1. **Estructura clara**: El flujo de ejecución (`make template` seguido de `make schemas`) está explicado paso a paso.
2. **Ejemplos prácticos**: Cada comando incluye ejemplos concretos para facilitar su uso