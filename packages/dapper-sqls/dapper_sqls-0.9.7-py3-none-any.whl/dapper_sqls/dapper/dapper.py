# -*- coding: latin -*-
from .._types import  T
from ..config import Config
from ..models import Result
from typing import Type, overload
from .executors import Query, Stored

class Dapper(object):

        def __init__(self, server: str , database : str , username : str, password : str, sql_version : int = None, api_environment = False, default_attempts = 1, default_wait_timeout = 2):
            self._config = Config(server, database, username, password, sql_version, api_environment, default_attempts, default_wait_timeout)
            
        def query(self, attempts : int = None, wait_timeout : int = None):
            attempts = attempts if attempts else self.config.default_attempts
            wait_timeout = wait_timeout if wait_timeout else self.config.default_wait_timeout
            return Query(self.config.connectionStringDataQuery.get(), attempts, wait_timeout, self._config.sql_version, self._config.api_environment)

        def stored(self, attempts : int = None, wait_timeout : int = None):
            attempts = attempts if attempts else self.config.default_attempts
            wait_timeout = wait_timeout if wait_timeout else self.config.default_wait_timeout
            return Stored(self.config.connectionStringDataStored.get() , attempts, wait_timeout, self._config.sql_version, self._config.api_environment)

        @property
        def config(self):
            return self._config
        
        @overload
        @staticmethod
        def load(model : Type[T], dict_data : dict) -> T:
            pass

        @overload
        @staticmethod
        def load(model : Type[T], list_dict_data : list[dict]) -> list[T]:
            pass

        @overload
        @staticmethod
        def load(model : Type[T], fetchone : Result.Fetchone) -> T:
            pass

        @overload
        @staticmethod
        def load(model : Type[T], fetchall : Result.Fetchall) -> list[T]:
            pass

        @staticmethod
        def load(*args) -> object | list[object]:
            model = args[0] 
            data = args[1]
            if isinstance(args[1], dict) or isinstance(args[1], Result.Fetchone):
                if isinstance(args[1], Result.Fetchone):
                    data = data.dict
                if all(value is None for value in data.values()):
                    return model()

                return model(**data)

            if isinstance(args[1], Result.Fetchall):
                    data = data.list_dict

            return [model(**d) for d in data]




