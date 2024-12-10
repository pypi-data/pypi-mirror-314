import os
from sqlalchemy import create_engine

# Conexão DW
DW_DATABASE_TYPE = os.environ.get("DW_DATABASE_TYPE", "postgresql")
DW_DATABASE_DRIVER = os.environ.get("DW_DATABASE_DRIVER", "psycopg2")
DW_DATABASE_USER = os.environ.get("DW_DATABASE_USER", "projjetta")
DW_DATABASE_PASSWORD = os.environ.get("DW_DATABASE_PASSWORD", "projjetta")
DW_DATABASE_ADDRESS = os.environ.get("DW_DATABASE_ADDRESS", "localhost")
DW_DATABASE_PORT = int(os.environ.get("DW_DATABASE_PORT", 5432))
DW_DATABASE_NAME = os.environ.get("DW_DATABASE_NAME", "nexus")

class DatabaseConnection:

    def __init__(self, 
                 database_name : str,
                 database_type : str, 
                 database_driver : str, 
                 database_user : str, 
                 database_password : str,
                 database_address : str,
                 database_port : int):
        """ Construtor padrão da classe """
        self._database_name = database_name
        self._database_type = database_type
        self._database_driver = database_driver
        self._database_user = database_user
        self._database_password = database_password
        self._database_address = database_address
        self._database_port = database_port
        self._engine = create_engine(self.get_connection_string(), echo=True)

    @property
    def engine(self):
        return self._engine

    def get_connection_string(self) -> str:
        """ Retornar a string de conexão """
        return f"{self._database_type}+{self._database_driver}://{self._database_user}:{self._database_password}@{self._database_address}:{self._database_port}/{self._database_name}"

DW_ENGINE = DatabaseConnection(
    DW_DATABASE_NAME,
    DW_DATABASE_TYPE,
    DW_DATABASE_DRIVER,
    DW_DATABASE_USER,
    DW_DATABASE_PASSWORD,
    DW_DATABASE_ADDRESS,
    DW_DATABASE_PORT
)