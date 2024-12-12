# -*- coding: latin -*-
import re
from pydantic import Field, BaseModel

class InformationSchemaTables(BaseModel):
    TABLE_CATALOG : str = Field(None, description="")
    TABLE_SCHEMA : str = Field(None, description="")
    TABLE_NAME : str = Field(None, description="")
    COLUMN_NAME : str = Field(None, description="")
    DATA_TYPE : str = Field(None, description="")
    IS_NULLABLE : str = Field(None, description="")

class InformationSchemaRoutines(BaseModel):
    SPECIFIC_CATALOG : str = Field(None, description="")
    SPECIFIC_SCHEMA : str = Field(None, description="")
    SPECIFIC_NAME : str = Field(None, description="")
    ORDINAL_POSITION : int = Field(None, description="")
    PARAMETER_NAME : str = Field(None, description="")
    DATA_TYPE : str = Field(None, description="")
    PROCEDURE_DEFINITION : str = Field(None, description="")
    
type_mapping = {
        'int': 'int',
        'bigint': 'int',
        'smallint': 'int',
        'tinyint': 'int',
        'bit': 'bool',
        'decimal': 'float',
        'numeric': 'float',
        'money': 'float',
        'smallmoney': 'float',
        'float': 'float',
        'real': 'float',
        'date': 'datetime',
        'datetime': 'datetime',
        'datetime2': 'datetime',
        'datetimeoffset': 'datetime',
        'smalldatetime': 'datetime',
        'time': 'datetime.time',
        'binary': 'bytes',
        'varbinary': 'bytes',
        'image': 'bytes',
        'timestamp': 'bytes', 
        'rowversion': 'bytes',  
    }

def create_field(data : InformationSchemaTables, field = 'Field(None, description="")'):
    
    sql_data_type = data.DATA_TYPE.lower()  
    python_type = type_mapping.get(sql_data_type)
    if python_type is None:
        python_type = 'str'

    if field == 'Field(None, description="")':
        if data.IS_NULLABLE:
            if python_type != 'str' and python_type != 'bool':
                return f'{data.COLUMN_NAME} : Union[{python_type}, str, None] = {field}'
            return f'{data.COLUMN_NAME} : Union[{python_type}, None] = {field}'
        
    if python_type != 'str' and python_type != 'bool':
        return f'{data.COLUMN_NAME} :  Union[{python_type}, str] = {field}'
    return f'{data.COLUMN_NAME} : {python_type} = {field}'

def get_parameters_with_defaults(stored_procedure):
    # Regular expression to capture parameters and their default values
    pattern = r"@(\w+)\s+\w+(?:\(\d+\))?\s*(?:=\s*(NULL|'[^']*'|\"[^\"]*\"|\d+))?"
    
    # Dictionary to hold parameters and their default values
    params_with_defaults = {}

    # Extract the parameter section of the stored procedure
    param_section_match = re.search(r'\(\s*(.*?)\s*\)\s*AS', stored_procedure, re.S | re.I)
    if not param_section_match:
        return params_with_defaults  # Return an empty dictionary if no parameters found

    param_section = param_section_match.group(1)

    # Find all parameter definitions in the extracted section
    matches = re.findall(pattern, param_section, re.IGNORECASE)

    for match in matches:
        param_name = match[0]  # Parameter name
        default_value = match[1] if match[1] else False  # Default value or None if not present

        # Validate the default value to be a string or an integer
        if default_value != False:
            # Check if it's a string (enclosed in quotes)
            if default_value.startswith(("'", '"')) and default_value.endswith(("'", '"')):
                # Remove quotes for the final value
                default_value = default_value
            # Check if it's an integer
            elif default_value.isdigit():
                default_value = int(default_value)
            else:
                # If it's not a valid string or integer, set to None
                default_value = None

        # Add to dictionary
        params_with_defaults[param_name] = default_value

    return params_with_defaults

def create_params_routine(data : InformationSchemaRoutines, defaults_values : dict[str, str | int | None]):
    sql_data_type = data.DATA_TYPE.lower()  
    python_type = type_mapping.get(sql_data_type)
    if python_type is None:
        python_type = 'str'
    name = data.PARAMETER_NAME.replace('@', '')
    default_value = defaults_values.get(name)
    if default_value == False:
        if python_type != 'str' and python_type != 'bool':
            return f'{name} : Union[{python_type}, str]'
        return f'{name} : {python_type}'
    else:
        if python_type != 'str' and python_type != 'bool':
            return f'{name} : Union[{python_type}, str] = {default_value}'
        return f'{name} : {python_type} = {default_value}'

def create_content_orm(class_name : str, fields_args_str : str):

    return f'''# -*- coding: latin -*-

from datetime import datetime
from typing import overload, Union
from dapper_sqls import Dapper
from dapper_sqls.dapper.dapper import Stored, Query
from dapper_sqls.dapper.executors import BaseExecutor, StoredUpdate, QueryUpdate
from dapper_sqls.utils import get_dict_args
from dapper_sqls.models import ConnectionStringData, Result
from .model import {class_name}

      
class BaseExecutorORM(BaseExecutor):
    def __init__(self, executor : Query | Stored , connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        BaseExecutor.__init__(self, connectionStringData, attempts, wait_timeout, sql_version, api_environment)
        self._executor = executor

    @property
    def executor(self):
        return self._executor

    def fetchone(self, additional_sql : str = "", *, {fields_args_str}) -> {class_name}:
        return self.executor.fetchone(self, {class_name}(**get_dict_args(locals(), ['additional_sql'])), additional_sql)

    def fetchall(self, additional_sql : str = "", select_top : int = None, *, {fields_args_str}) -> list[{class_name}]:
        return self.executor.fetchall(self, {class_name}(**get_dict_args(locals(), ['additional_sql', 'select_top'])), additional_sql, select_top)

    def delete(self, *, {fields_args_str}) -> Result.Send:
        return self.executor.delete(self, {class_name}(**get_dict_args(locals())))
    
    def insert(self, *, {fields_args_str}) -> Result.Insert:
        return self.executor.insert(self, {class_name}(**get_dict_args(locals())))

    def _exec_(self, *args):
        return self.executor._exec_(self, *args)

class QueryUpdate{class_name}ORM(object):
        def __init__(self, executor, model : {class_name}):
            self._set_data = model
            self._executor = executor

        @property
        def set_data(self):
            return self._set_data

        @property
        def executor(self):
            return self._executor

        @overload
        def where(self, query : str = None, *, {fields_args_str}) -> Result.Send:
            pass

        def where(self, *args, **kwargs) -> Result.Send:
            query = kwargs.get('query')
            if query:
                return QueryUpdate(self._executor, self.set_data).where(query)
            return QueryUpdate(self._executor, self.set_data).where({class_name}(**kwargs))

class Query{class_name}ORM(BaseExecutorORM):
    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        BaseExecutorORM.__init__(self, Query, connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    def update(self, *, {fields_args_str}):
            return QueryUpdate{class_name}ORM(self, {class_name}(**get_dict_args(locals())))

class StoredUpdate{class_name}ORM(object):
    def __init__(self, executor, model : {class_name}):
        self._set_data = model
        self._executor = executor

    @property
    def set_data(self):
        return self._set_data

    @property
    def executor(self):
        return self._executor

    def where(self, *, {fields_args_str}) -> Result.Send:
        return StoredUpdate(self._executor, self.set_data).where({class_name}(**get_dict_args(locals())))

class Stored{class_name}ORM(BaseExecutorORM):
    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        BaseExecutorORM.__init__(self, Stored, connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    def update(self, {fields_args_str}):
        return StoredUpdate{class_name}ORM(self, {class_name}(**get_dict_args(locals())))

class {class_name}ORM(object):

    def __init__(self, dapper : Dapper):
          self._dapper = dapper

    class {class_name}({class_name}):
        ...

    @property
    def dapper(self):
        return self._dapper

    def query(self, attempts : int = None, wait_timeout : int = None):
            attempts = attempts if attempts else self.dapper.config.default_attempts
            wait_timeout = wait_timeout if wait_timeout else self.dapper.config.default_wait_timeout
            return Query{class_name}ORM(self.dapper.config.connectionStringDataQuery.get(), attempts, wait_timeout, self.dapper.config.sql_version, self.dapper.config.api_environment)

    def stored(self, attempts : int = None, wait_timeout : int = None):
        attempts = attempts if attempts else self.dapper.config.default_attempts
        wait_timeout = wait_timeout if wait_timeout else self.dapper.config.default_wait_timeout
        return Stored{class_name}ORM(self.dapper.config.connectionStringDataStored.get() , attempts, wait_timeout, self.dapper.config.sql_version, self.dapper.config.api_environment)
            
    @overload
    @staticmethod
    def load(dict_data : dict) -> {class_name}:
        pass

    @overload
    @staticmethod
    def load(list_dict_data : list[dict]) -> list[{class_name}]:
        pass

    @overload
    @staticmethod
    def load(fetchone : Result.Fetchone) -> {class_name}:
        pass

    @overload
    @staticmethod
    def load(fetchall : Result.Fetchall) -> list[{class_name}]:
        pass

    @staticmethod
    def load(*args):
        data = args[0]
        if isinstance(data, dict) or isinstance(data, Result.Fetchone):
            if isinstance(data, Result.Fetchone):
                data = data.dict
            if all(value is None for value in data.values()):
                return {class_name}()

            return {class_name}(**data)

        if isinstance(data, Result.Fetchall):
                data = data.list_dict

        return [{class_name}(**d) for d in data]
            '''

def create_content_async_orm(class_name : str, fields_args_str : str):

    return f'''# -*- coding: latin -*-

from datetime import datetime
from typing import overload, Union
from dapper_sqls import AsyncDapper
from dapper_sqls.async_dapper.async_dapper import AsyncStored, AsyncQuery
from dapper_sqls.async_dapper.async_executors import AsyncBaseExecutor, AsyncQueryUpdate, AsyncStoredUpdate
from dapper_sqls.utils import get_dict_args
from dapper_sqls.models import ConnectionStringData, Result
from .model import {class_name}


class AsyncBaseExecutorORM(AsyncBaseExecutor):
    def __init__(self, executor : AsyncQuery | AsyncStored , connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        AsyncBaseExecutor.__init__(self, connectionStringData, attempts, wait_timeout, sql_version, api_environment)
        self._executor = executor

    @property
    def executor(self):
        return self._executor

    async def fetchone(self, additional_sql : str = "", *, {fields_args_str}) -> {class_name}:
        return await self.executor.fetchone(self, {class_name}(**get_dict_args(locals(), ['additional_sql'])), additional_sql)

    async def fetchall(self, additional_sql : str = "", select_top : int = None, *, {fields_args_str}) -> list[{class_name}]:
        return await self.executor.fetchall(self, {class_name}(**get_dict_args(locals(), ['additional_sql', 'select_top'])), additional_sql, select_top)

    async def delete(self, *, {fields_args_str}) -> Result.Send:
        return await self.executor.delete(self, {class_name}(**get_dict_args(locals())))
    
    async def insert(self, *, {fields_args_str}) -> Result.Insert:
        return await self.executor.insert(self, {class_name}(**get_dict_args(locals())))

    async def _exec_(self, *args):
        return await self.executor._exec_(self, *args)

class AsyncQueryUpdate{class_name}ORM(object):
    def __init__(self, executor, model : {class_name}):
        self._set_data = model
        self._executor = executor

    @property
    def set_data(self):
        return self._set_data

    @property
    def executor(self):
        return self._executor

    @overload
    async def where(self, query : str = None, *, {fields_args_str}) -> Result.Send:
        pass
        
    async def where(self, *args, **kwargs) -> Result.Send:
        query = kwargs.get('query')
        if query:
            return await AsyncQueryUpdate(self._executor, self.set_data).where(query)
        return await AsyncQueryUpdate(self._executor, self.set_data).where({class_name}(**kwargs))

class AsyncQuery{class_name}ORM(AsyncBaseExecutorORM):
    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        AsyncBaseExecutorORM.__init__(self, AsyncQuery, connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    def update(self, *, {fields_args_str}):
        return AsyncQueryUpdate{class_name}ORM(self, {class_name}(**get_dict_args(locals())))

class AsyncStoredUpdate{class_name}ORM(object):
    def __init__(self, executor, model : {class_name}):
        self._set_data = model
        self._executor = executor

    @property
    def set_data(self):
        return self._set_data

    @property
    def executor(self):
        return self._executor

    async def where(self, *, {fields_args_str}) -> Result.Send:
        return await AsyncStoredUpdate(self._executor, self.set_data).where({class_name}(**get_dict_args(locals())))

class AsyncStored{class_name}ORM(AsyncBaseExecutorORM):
    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        AsyncBaseExecutorORM.__init__(self, AsyncStored, connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    def update(self, {fields_args_str}):
        return AsyncStoredUpdate{class_name}ORM(self, {class_name}(**get_dict_args(locals())))

class Async{class_name}ORM(object):

    def __init__(self, async_dapper : AsyncDapper):
          self._async_dapper = async_dapper

    class {class_name}({class_name}):
        ...

    @property
    def async_dapper(self):
        return self._async_dapper

    async def query(self, attempts : int = None, wait_timeout : int = None):
            attempts = attempts if attempts else self.async_dapper.config.default_attempts
            wait_timeout = wait_timeout if wait_timeout else self.async_dapper.config.default_wait_timeout
            return AsyncQuery{class_name}ORM(self.async_dapper.config.connectionStringDataQuery.get(), attempts, wait_timeout, self.async_dapper.config.sql_version, self.async_dapper.config.api_environment)

    async def stored(self, attempts : int = None, wait_timeout : int = None):
        attempts = attempts if attempts else self.async_dapper.config.default_attempts
        wait_timeout = wait_timeout if wait_timeout else self.async_dapper.config.default_wait_timeout
        return AsyncStored{class_name}ORM(self.async_dapper.config.connectionStringDataStored.get() , attempts, wait_timeout, self.async_dapper.config.sql_version, self.async_dapper.config.api_environment)
    
    @overload
    @staticmethod
    def load(dict_data : dict) -> {class_name}:
        pass

    @overload
    @staticmethod
    def load(list_dict_data : list[dict]) -> list[{class_name}]:
        pass

    @overload
    @staticmethod
    def load(fetchone : Result.Fetchone) -> {class_name}:
        pass

    @overload
    @staticmethod
    def load(fetchall : Result.Fetchall) -> list[{class_name}]:
        pass

    @staticmethod
    def load(*args):
        data = args[0]
        if isinstance(data, dict) or isinstance(data, Result.Fetchone):
            if isinstance(data, Result.Fetchone):
                data = data.dict
            if all(value is None for value in data.values()):
                return {class_name}()

            return {class_name}(**data)

        if isinstance(data, Result.Fetchall):
                data = data.list_dict

        return [{class_name}(**d) for d in data]
    '''



