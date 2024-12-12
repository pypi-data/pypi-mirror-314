from ..utils import get_dict_args, Utils
from .._types import T
from ..models import Result
from typing import overload, Union
from abc import ABC

class StpBaseBuilder(ABC):

    @staticmethod
    def build_data(stp_name : str, **kwargs : dict[str, Union[int, str, any]]):
        query = f"EXEC {stp_name} "
        i = 0
        for chave, valor in kwargs.items():
            i += 1
            query += f"@{chave} = ?"
            if i < len(kwargs):
                query += ", "

        return query, tuple(kwargs.values())


    def __init__(self, stp_name : str, _locals : Union[object ,dict[str, Union[int, str, any]]]):
        _locals = _locals if isinstance(_locals, dict) else _locals()
        query , params = self.build_data(stp_name, **get_dict_args(_locals, ignore_values_none=False))
        self._query = query
        self._params = params

    @property
    def query(self):
        return self._query

    @property
    def params(self):
        return self._params

class StpBuilder(StpBaseBuilder):

    def __init__(self, dapper, stp_name : str, _locals : Union[object ,dict[str, Union[int, str, any]]]):
        self._dapper = dapper
        super().__init__(stp_name, _locals)

    @property
    def dapper(self):
        return self._dapper

    def execute(self, attempts : int = None, wait_timeout : int = None) -> Result.Send:
        with self.dapper.stored(attempts, wait_timeout) as db:
            return db.execute(self.query, self.params)

    @overload
    def fetchone(self, attempts : int = None, wait_timeout : int = None) -> Result.Fetchone:
            pass

    @overload
    def fetchone(self, model : T , attempts : int = None, wait_timeout : int = None) -> T:
            pass

    def fetchone(self, *args, **kwargs) -> T | Result.Fetchone:
        args = Utils.args_stp(*args, **kwargs)

        with self.dapper.stored(args.attempts, args.wait_timeout) as db:
            result = db.fetchone(self.query, self.params)
            if args.model:
                return self.dapper.load(args.model, result)
            return result

    @overload
    def fetchall(self, attempts : int = None, wait_timeout : int = None) -> Result.Fetchall:
            pass

    @overload
    def fetchall(self, model : T, attempts : int = None, wait_timeout : int = None) -> list[T]:
            pass

    def fetchall(self, *args, **kwargs) -> list[T] | Result.Fetchall:
        args = Utils.args_stp(*args, **kwargs)
            
        with self.dapper.stored(args.attempts, args.wait_timeout) as db:
            result = db.fetchall(self.query, self.params)
            if args.model:
                    return self.dapper.load(args.model, result)
            return result


class AsyncStpBuilder(StpBaseBuilder):

    def __init__(self, async_dapper, stp_name : str, _locals : Union[object ,dict[str, Union[int, str, any]]]):
        self._async_dapper = async_dapper
        super().__init__(stp_name, _locals)

    @property
    def async_dapper(self):
        return self._async_dapper

    async def execute(self, attempts : int = None, wait_timeout : int = None) -> Result.Send:
        async with await self.async_dapper.stored(attempts, wait_timeout) as db:
            return await db.execute(self.query, self.params)

    @overload
    async def fetchone(self, attempts : int = None, wait_timeout : int = None) -> Result.Fetchone:
            pass

    @overload
    async def fetchone(self, model : T , attempts : int = None, wait_timeout : int = None) -> T:
            pass

    async def fetchone(self, *args, **kwargs) -> T | Result.Fetchone:
        args = Utils.args_stp(*args, **kwargs)

        async with await self.async_dapper.stored(args.attempts, args.wait_timeout) as db:
            result = await db.fetchone(self.query, self.params)
            if args.model:
                return self.async_dapper.load(args.model, result)
            return result

    @overload
    async def fetchall(self, attempts : int = None, wait_timeout : int = None) -> Result.Fetchall:
            pass

    @overload
    async def fetchall(self, model : T , attempts : int = None, wait_timeout : int = None) -> list[T]:
            pass

    async def fetchall(self, *args, **kwargs) -> list[T] | Result.Fetchall:
        args = Utils.args_stp(*args, **kwargs)
            
        async with await self.async_dapper.stored(args.attempts, args.wait_timeout) as db:
            result = await db.fetchall(self.query, self.params)
            if args.model:
                    return self.async_dapper.load(args.model, result)
            return result


