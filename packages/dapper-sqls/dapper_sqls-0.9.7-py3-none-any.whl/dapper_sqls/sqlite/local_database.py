# -*- coding: latin -*-

from sqlalchemy import create_engine, inspect, text, insert,MetaData, Table, Integer, Column, String, delete, update
from sqlalchemy.engine import Engine
from tempfile import gettempdir
from os import path, makedirs
from .models import Path, System ,EnvVar
import re

#C:\Users\Samuel\AppData\Local\Temp


def is_valid_name(name, max_length=255):
    # Verifica se o nome não é vazio
    if not name:
        return False

    # Verifica se o nome não excede o comprimento máximo permitido
    if len(name) > max_length:
        return False

    # Verifica se o nome não contém caracteres inválidos
    # Neste exemplo, permitimos apenas letras, números, espaços e underscore (_)
    if not re.match(r'^[\w\s]+$', name):
        return False

    return True

class LocalDatabase(object):

    class Tables(object):

        meta_data = MetaData()

        system = Table(
            'system',  # Nome da tabela
            meta_data,
            Column('id', Integer, primary_key=True),  
            Column('App', String),  
            Column('Tema', String) 
        )

        env_var = Table(
            'env_var',
            meta_data,
            Column('id', Integer, primary_key=True),
            Column('App', String), 
            Column('Name', String),
            Column('Value', String)
            )

        path = Table(
            'path',
            meta_data,
            Column('id', Integer, primary_key=True),
            Column('App', String), 
            Column('Name', String),
            Column('Path', String)
            )


    def __init__(self, app_name : str, *, path_local_database = gettempdir(), database_name="saftOnlineLocalDatabase", database_folder_name = "SaftOnline"):
        app_name = self.get_value(app_name)
        if not database_name.endswith('.db'):
            database_name = f'{database_name}.db'
        if not is_valid_name(app_name):
            raise Exception("Nome de identificação do programa é inválido")
        self._app_name = app_name
        self._path_database = path.join(path_local_database,database_folder_name, database_name)
        self._engine : Engine = None

        if not path.isfile(self._path_database):
            if not path.exists(path.join(path_local_database,database_folder_name)):
                makedirs(path.join(path_local_database,database_folder_name))

            # Se o banco de dados não existe, crie-o e crie a tabela
            conn = self.engine.connect()
      
            self.Tables.meta_data.create_all(self.engine)

            ins = insert(self.Tables.system).values(App=app_name, Tema='light')
            conn.execute(ins)
            conn.commit()
            conn.close()

        else:
            if not self.are_tables_existing(self.engine):
                try:
                    self.Tables.meta_data.create_all(self.engine)
                    ...
                except:
                   ...
            else:
                try:
                    self.synchronize_columns(self.engine)
                except:
                    ...
       

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(f'sqlite:///{self.path_database}')
        return self._engine

    @property
    def app_name(self):
        return self._app_name

    @property
    def path_database(self):
        return self._path_database

    def are_columns_existing(self, engine):
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        required_tables = self.Tables.meta_data.tables.keys()

        for table_name in required_tables:
            if table_name in existing_tables:
                # Get the columns in the existing table
                existing_columns = inspector.get_columns(table_name)
                existing_column_names = [column['name'] for column in existing_columns]
            
                # Get the columns defined in the Table class
                required_columns = self.Tables.meta_data.tables[table_name].c.keys()
            
                if not all(column in existing_column_names for column in required_columns):
                    return False
            else:
                return False
        return True

    def are_tables_existing(self, engine):
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        required_tables = self.Tables.meta_data.tables.keys()
    
        return all(table in existing_tables for table in required_tables)

    def synchronize_columns(self, engine):
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        for table_name in self.Tables.meta_data.tables.keys():
            if table_name in existing_tables:
                # Get the columns in the existing table
                existing_columns = inspector.get_columns(table_name)
                existing_column_names = [column['name'] for column in existing_columns]

                # Get the columns defined in the Table class
                required_columns = self.Tables.meta_data.tables[table_name].c.keys()
                required_column_defs = {col.name: col for col in self.Tables.meta_data.tables[table_name].columns}

                # Add columns in lack
                for column in required_columns:
                    if column not in existing_column_names:
                        column_type = required_column_defs[column].type
                        add_column_sql = f'ALTER TABLE {table_name} ADD COLUMN {column} {column_type}'
                        with engine.connect() as conn:
                            conn.execute(text(add_column_sql))
                     
    def get_value(self, value):
        try :
            return value.value
        except:
            return value

    def select(self, table : str, where : str = None):
        with self.engine.connect() as conn:
            if where:
                query = conn.execute(text(f"select * from {table} where App = '{self.app_name}' and {where}"))
            else:
                query = conn.execute(text(f"select * from {table} where App = '{self.app_name}'"))
            data = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return data


    def get_path(self, name):
        name = self.get_value(name)
        data = self.select('path', f"Name = '{name}'")
        for d in data:
            return Path(d).Path

    def update_path(self, name : str, path_name : str):
        name = self.get_value(name)
        path_name = self.get_value(path_name)
        existsPath = self.get_path(name)

        with self.engine.connect() as conn:
            if existsPath != None:
                stmt = update(self.Tables.path).where(
                    (self.Tables.path.c.Name == name) &
                    (self.Tables.path.c.App == self.app_name)
                ).values(Path=path_name)
                conn.execute(stmt)
            else:
                ins = insert(self.Tables.path).values(App=self.app_name, Name=name, Path=path_name)
                conn.execute(ins)
            conn.commit()

    def delete_path(self, name : str):
        name = self.get_value(name)
        with self.engine.connect() as conn:
            stmt = delete(self.Tables.path).where((self.Tables.path.c.Name == name) & (self.Tables.env_var.c.App == self.app_name))
            conn.execute(stmt)
            conn.commit()

    def get_var(self, name):
        name = self.get_value(name)
        data = self.select('env_var', f"name = '{name}'")
        for d in data:
            return EnvVar(d).Value

    def update_var(self, name : str, value : str):
        name = self.get_value(name)
        value = self.get_value(value)
        existsVar = self.get_var(name)
        with self.engine.connect() as conn:
            if existsVar != None:
               stmt = update(self.Tables.env_var).where(
                    (self.Tables.env_var.c.Name == name) &
                    (self.Tables.env_var.c.App == self.app_name)
               ).values(Value=value)
               conn.execute(stmt)
            else:
               ins = insert(self.Tables.env_var).values(App=self.app_name, Name=name, Value=value)
               conn.execute(ins)
            conn.commit()

    def delete_var(self, name : str):
        name = self.get_value(name)
        with self.engine.connect() as conn:
            stmt = delete(self.Tables.env_var).where((self.Tables.env_var.c.Name == name) & (self.Tables.env_var.c.App == self.app_name))
            conn.execute(stmt)
            conn.commit()

    def get_theme(self):
        # Consulta o tema no banco de dados
        data = self.select('system')
        if data:
            # Se houver dados, retorna o tema
            return System(data[0]).Theme
        else:
            # Se não houver dados, insere um tema padrão e retorna 'light'
            with self.engine.connect() as conn:
                ins = insert(self.Tables.system).values(App=self.app_name, Tema='light')
                conn.execute(ins)
                conn.commit()
            return 'light'

    def update_theme(self, theme : str):
        theme = self.get_value(theme)
        _theme = self.get_theme()
        if _theme:
            with self.engine.connect() as conn:
                stmt = update(self.Tables.system).where(
                    self.Tables.system.c.App == self.app_name
                ).values(Tema=theme)
                conn.execute(stmt)
                conn.commit()
           

    




