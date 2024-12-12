from pydantic import BaseModel, BaseConfig
from abc import ABC
from abc import ABC, abstractmethod
from .result import Result

class TableBaseModel(BaseModel, ABC): 
    class Config(BaseConfig):
        from_attributes = True

    _TABLE_NAME: str = ''

    @property
    def TABLE_NAME(cls) -> str:
        return cls._TABLE_NAME

class BaseUpdate(ABC):

        def __init__(self, executor , model):
            self._set_data = model
            self._executor = executor

        @property
        def set_data(self):
            return self._set_data

        @property
        def executor(self):
            return self._executor

        @abstractmethod
        def where(self, *args)  -> Result.Send:
            pass



