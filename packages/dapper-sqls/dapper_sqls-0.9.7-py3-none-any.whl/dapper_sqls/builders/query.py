# -*- coding: latin -*-
from typing import Type, Union
from pydantic import BaseModel
from datetime import datetime, date
import json

class Value:
    def __init__(self, value : Union[str, int, bytes, float, datetime, date], prefix : str, suffix : str):
        self.value = value
        self.prefix = prefix
        self.suffix = suffix

class QueryBuilder(object):

    def value(value : Union[str, int, bytes, float, datetime, date], prefix = "=", suffix = ""):
        json_value = json.dumps({'prefix': prefix, 'value': value, 'suffix': suffix})
        return f"#QueryBuilderValue#{json_value}#QueryBuilderValue#"

    @classmethod
    def _build_where_clause(cls, **kwargs):
        conditions = []
        for field, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    if '#QueryBuilderValue#' in value:
                        value = value.replace('#QueryBuilderValue#', '')
                        value = Value(**json.loads(value.strip()))
                        if isinstance(value.value, str):
                            conditions.append(f"{field} {value.prefix} '{value.value}' {value.suffix}")
                        else:
                            conditions.append(f"{field} {value.prefix} {value.value} {value.suffix}")
                    else:
                        conditions.append(f"{field} = '{value}'")
                else:
                    conditions.append(f"{field} = {value}")
        return " AND ".join(conditions)

    @classmethod
    def update(cls, model: Type[BaseModel], where : Union[str , Type[BaseModel]]):
        update_data = model.model_dump(exclude_none=True)
        if not isinstance(where, str):
            where_data = where.model_dump(exclude_none=True)
            where = cls._build_where_clause(**where_data)

        set_clause = ", ".join([f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in update_data.items()])
        sql_query = f"UPDATE {model.TABLE_NAME} SET {set_clause} WHERE {where}"
        return sql_query

    def insert(model: Type[BaseModel], name_column_id = 'Id'):
        insert_data = model.model_dump(exclude_none=True)
        columns = ", ".join(insert_data.keys())
        values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in insert_data.values()])
        sql_query = f"""
            INSERT INTO {model.TABLE_NAME} ({columns})
            OUTPUT INSERTED.{name_column_id} AS Id
            VALUES ({values})
            """
        return sql_query

    @classmethod
    def select(cls, model: Type[BaseModel], additional_sql : str = "" ,select_top : int= None):
        top_clause = f"TOP ({select_top}) * " if select_top else "*"
        select_data = model.model_dump(exclude_none=True)
        where_clause = cls._build_where_clause(**select_data)

        sql_query = f"SELECT {top_clause} FROM {model.TABLE_NAME}"
        if where_clause:
            sql_query += f" WHERE {where_clause}"
        sql_query = f'{sql_query} {additional_sql}'
        return sql_query

    @classmethod
    def delete(cls, model: Type[BaseModel]):
        delete_data = model.model_dump(exclude_none=True)
        where_clause = cls._build_where_clause(**delete_data)
        if not where_clause:
            raise ValueError("DELETE operation requires at least one condition.")
        sql_query = f"DELETE FROM {model.TABLE_NAME} WHERE {where_clause}"
        return sql_query

