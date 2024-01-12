import os # Esta librería ayuda a acceder al sistema de archivos, manipular y obtener información.
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre de la base de datos
sqlite_file_name = "../database.sqlite"

# Es el directorio del archivo database.py
base_dir = os.path.dirname(os.path.realpath(__file__)) 

# Es la forma en la que se conecta a una base de datos.
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" 

# Representa el motor de la base de datos.
# Con el comando echo=True se muestra por consola lo que está realizando.
engine = create_engine(database_url, echo=True)

# Se crea una Session y se enlaza a la base de datos a través del comando bind.
Session = sessionmaker(bind=engine)

# Sirve para manipular las tablas de la base de datos.
Base = declarative_base()