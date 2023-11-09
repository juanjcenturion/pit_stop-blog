# generate_sql.py
import os

# Ruta absoluta al archivo .env
env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

# Lee las variables de entorno desde el archivo .env
with open(env_file_path, 'r') as env_file:
    env_vars = dict(
        line.strip().split('=') for line in env_file if '=' in line
    )

# Nombre de la base de datos que deseas crear
database_name = env_vars.get('MYSQL_DATABASE')

# Genera el contenido SQL
sql_content = f"""CREATE DATABASE {database_name};

USE {database_name};
"""

# Ruta absoluta al archivo create_schema.sql
sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_schema.sql')

# Guarda el contenido SQL en un archivo
with open(sql_file_path, 'w') as sql_file:
    sql_file.write(sql_content)
