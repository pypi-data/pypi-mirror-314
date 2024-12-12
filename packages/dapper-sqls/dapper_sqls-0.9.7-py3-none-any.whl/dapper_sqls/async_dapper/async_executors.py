# -*- coding: latin -*-
import aioodbc, asyncio
from typing import overload
from datetime import datetime
from abc import ABC, abstractmethod
from ..models import ConnectionStringData, Result, UnavailableServiceException, BaseUpdate
from .._types import T, ExecType
from ..config import Config
from ..builders import QueryBuilder, StoredBuilder
from ..utils import Utils

class AsyncBaseExecutor(ABC):
    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        self._connectionStringData = connectionStringData
        self._cursor = None
        self._connection = None
        self._wait_timeout = wait_timeout 
        self._attempts = attempts 
        self._sql_version = sql_version
        self._api_environment = api_environment

    async def __aenter__(self):
        cs_data = self._connectionStringData
        for n in range(self._attempts):
            odbc_version = f'ODBC Driver {self._sql_version} for SQL Server' 
            if not self._sql_version:
                all_driver_versions = Config.get_all_odbc_driver_versions()
                if all_driver_versions:
                    odbc_version = all_driver_versions[0]
                else:
                    raise RuntimeError("Nenhuma vers�o do driver ODBC for SQL Server foi encontrada.")
            try:
                connection_string = f'DRIVER={{{odbc_version}}};SERVER={cs_data.server};DATABASE={cs_data.database};UID={cs_data.username};PWD={cs_data.password}'
                self._connection = await aioodbc.connect(dsn=connection_string)
                self._cursor = await self._connection.cursor()

            except Exception as e:
                print(e)
                print(f'Erro na conex�o com a base de dados, nova tentativa em {self._wait_timeout}s')
                await asyncio.sleep(self._wait_timeout)

        return self

    async def __aexit__(self, *args):
        if self._cursor:
            await self._cursor.close()
        if self._connection:
            await self._connection.close()

    @property
    def connectionStringData(self):
        return self._connectionStringData

    @property
    def api_environment(self):
        return self._api_environment

    @property
    def sql_version(self):
        return self._sql_version

    @property
    async def cursor(self):
        if not self._cursor:
            if self._connection:
                self._cursor = await self._connection.cursor()
        return self._cursor

    @property
    def connection(self):
        if self._connection:
            return self._connection

    @property
    def attempts(self):
        return self._attempts

    @attempts.setter
    def attempts(self, value):
        if isinstance(value, int):
            self._attempts = value
        else:
            raise ValueError("O n�mero de tentativas deve ser um n�mero inteiro.")

    @property
    def wait_timeout(self):
        return self._wait_timeout

    @wait_timeout.setter
    def wait_timeout(self, value):
        if isinstance(value, int):
            self._wait_timeout = value
        else:
            raise ValueError("O tempo de espera deve ser um n�mero inteiro.")

    @abstractmethod
    async def _exec_(self, connection, operation_sql, exec_type):
        pass

class AsyncQueryUpdate(BaseUpdate):
    def __init__(self, executor : AsyncBaseExecutor, model : T):
        super().__init__(executor, model)

    @overload
    async def where(self, model : T)  -> Result.Send:
            pass

    @overload
    async def where(self, query : str)  -> Result.Send:
        pass

    async def where(self, *args) -> Result.Send:
        query = QueryBuilder.update(self._set_data, *args)
        return await self.executor._exec_(self.executor.connection , query, ExecType.send)


class AsyncQuery(AsyncBaseExecutor):

    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int, sql_version : int | None, api_environment : bool):
        super().__init__(connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    @overload
    async def fetchone(self, query : str) -> Result.Fetchone:
        pass

    @overload
    async def fetchone(self, model : T, additional_sql : str = "") -> T:
        pass
          
    async def fetchone(self, *args, **kwargs) -> T | Result.Fetchone:
        args = Utils.args_query(*args, **kwargs)
        if args.model:
            args.query = QueryBuilder.select(args.model, args.additional_sql, args.select_top)
        
        result = await self._exec_(self._connection, args.query, ExecType.fetchone)
        if args.model:
            return args.model.__class__(**result.dict) if result.success else args.model.__class__()
        return result

    @overload
    async def fetchall(self, query : str) -> Result.Fetchall:
        pass

    @overload
    async def fetchall(self, model : T, additional_sql : str = "", select_top : int = None) -> list[T]:
        pass

    async def fetchall(self, *args, **kwargs) -> list[T] | Result.Fetchall:
        args = Utils.args_query(*args, **kwargs)
        if args.model:
            args.query = QueryBuilder.select(args.model, args.additional_sql, args.select_top)

        result = await self._exec_(self._connection, args.query, ExecType.fetchall)
        if args.model:
            return [args.model.__class__(**r) for r in result.list_dict] if result.success else []
        return result

    async def execute(self, query : str) -> Result.Send:
            return await self._exec_(self._connection, query, ExecType.send)

    async def delete(self, model: T) -> Result.Send:
        query = QueryBuilder.delete(model)
        return await self._exec_(self._connection, query, ExecType.send)

    def update(self, model: T):
        return AsyncQueryUpdate(self, model)

    async def insert(self, model: T, name_column_id = 'Id') -> Result.Insert:
        insert_data = model.model_dump()
        if name_column_id not in insert_data:
            name_column_id = next(iter(insert_data.keys())) 

        query = QueryBuilder.insert(model, name_column_id)
        result : Result.Fetchone = await self._exec_(self._connection, query, ExecType.fetchone)
        if result.success:
            return Result.Insert(result.dict.get('Id', 0), result.status_code, result.message)
        return Result.Insert(0, result.status_code, result.message)
    
    async def _exec_(self, connection, query_sql : str, exec_type : ExecType):
 
        if not self._cursor:
            if self._api_environment:
                raise UnavailableServiceException()

            if exec_type == ExecType.fetchone:
                return Result.Fetchone(None, None, 503)
            elif exec_type == ExecType.fetchall:
                return Result.Fetchall(None, None, 503)
            elif exec_type == ExecType.send:
                return Result.Send(False, 503)

        # executar
        response = await self._cursor.execute(query_sql)

        # ober resultado se nessesario
        if exec_type == ExecType.fetchone:
            result = Result.Fetchone(self._cursor, await response.fetchone())

        elif exec_type == ExecType.fetchall:
            result = Result.Fetchall(self._cursor, await response.fetchall())
        elif exec_type == ExecType.send:
            result = Result.Send(True)

        # fazer o commit 
        await connection.commit()

        # retorna o resultado
        return result


class AsyncStoredUpdate(BaseUpdate):
    def __init__(self, executor : AsyncBaseExecutor, model : T):
        super().__init__(executor, model)

    async def where(self, data : T)  -> Result.Send:
        query, params = StoredBuilder.update(self._set_data, data)
        return await self.executor._exec_(self.executor.connection, (query,  *params), ExecType.send)


class AsyncStored(AsyncBaseExecutor):

    def __init__(self, connectionStringData : ConnectionStringData, attempts : int, wait_timeout : int,sql_version : int | None,  api_environment : bool):
        super().__init__(connectionStringData, attempts, wait_timeout, sql_version, api_environment)

    @overload
    async def fetchone(self, query : str, params : list | tuple) -> Result.Fetchone:
        pass

    @overload
    async def fetchone(self, query : str, *params : int | str | datetime) -> Result.Fetchone:
        pass

    @overload
    async def fetchone(self, model : T, additional_sql : str = "") -> T:
        pass

    async def fetchone(self, *args, **kwargs) -> T | Result.Fetchone:
        args = Utils.args_stored(*args, **kwargs)
        if args.model:
            args.query, args.params = StoredBuilder.select(args.model, args.additional_sql, args.select_top)

        result = await self._exec_(self._connection, (args.query, *args.params), ExecType.fetchone)
        if args.model:
            return args.model.__class__(**result.dict) if result.success else args.model.__class__()
        return result

    @overload
    async def fetchall(self, query : str, params : list | tuple) -> Result.Fetchall:
        pass

    @overload
    async def fetchall(self, query : str, *params : int | str | datetime) -> Result.Fetchall:
        pass

    @overload
    async def fetchall(self, model : T, additional_sql : str = "", select_top : int = None) -> list[T]:
        pass

    async def fetchall(self, *args, **kwargs) -> list[T] | Result.Fetchall:
        args = Utils.args_stored(*args, **kwargs)
        if args.model:
            args.query, args.params = StoredBuilder.select(args.model, args.additional_sql, args.select_top)

        result = await self._exec_(self._connection, (args.query, *args.params), ExecType.fetchall)
        if args.model:
            return [args.model.__class__(**r) for r in result.list_dict] if result.success else []
        return result

    @overload
    async def execute(self, query : str, *params : str | int) -> Result.Send:
        pass

    @overload
    async def execute(self, query : str, params : list | tuple) -> Result.Send:
        pass

    async def execute(self, *args) -> Result.Send:
        query = args[0]
        params = args[1:]
        if len(params) == 1 and isinstance(params[0], (list, tuple)):
            params = params[0]
        return await self._exec_(self._connection, (query, *params), ExecType.send)

    async def delete(self, model: T) -> Result.Send:
        query, params = StoredBuilder.delete(model)
        return await self._exec_(self._connection, (query,  *params), ExecType.send)

    def update(self, model: T):
        return AsyncStoredUpdate(self, model)

    async def insert(self, model: T, name_column_id = 'Id') -> Result.Insert:
        insert_data = model.model_dump()
        if name_column_id not in insert_data:
            name_column_id = next(iter(insert_data.keys()))

        query, params = StoredBuilder.insert(model, name_column_id)
        result : Result.Fetchone = await self._exec_(self._connection, (query,  *params), ExecType.fetchone)
        if result.success:
            return Result.Insert(result.dict.get('Id', 0), result.status_code, result.message)
        return Result.Insert(0, result.status_code, result.message)
    
    async def _exec_(self, connection , stored_procedure : tuple, exec_type : ExecType):
 
        if not self._cursor:
            if self._api_environment:
                raise UnavailableServiceException()

            if exec_type == ExecType.fetchone:
                return Result.Fetchone(None, None, 503)
            elif exec_type == ExecType.fetchall:
                return Result.Fetchall(None, None, 503)
            elif exec_type == ExecType.send:
                return Result.Send(False, 503)

        try:
            # executar
            response = await self._cursor.execute(*stored_procedure)

            # ober resultado se nessesario
            if exec_type == ExecType.fetchone:
                result = Result.Fetchone(self._cursor, await response.fetchone())
            elif exec_type == ExecType.fetchall:
                result = Result.Fetchall(self._cursor, await response.fetchall())
            elif exec_type == ExecType.send:
                result = Result.Send(True)

            # fazer o commit 
            await connection.commit()
            
        except Exception as ex:
            if exec_type == ExecType.fetchone:
                return Result.Fetchone(None, None, 503, str(ex))
            elif exec_type == ExecType.fetchall:
                return Result.Fetchall(None, None, 503, str(ex))
            elif exec_type == ExecType.send:
                return Result.Send(False, 503, str(ex))

        # retorna o resultado
        return result




