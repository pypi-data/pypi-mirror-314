# -*- coding: latin -*-

from itertools import groupby
import os
from .utils import create_content_orm, InformationSchemaTables, InformationSchemaRoutines, create_field, create_content_async_orm, create_params_routine, get_parameters_with_defaults

class TableBuilderData:
    def __init__(self, table_schema : str, table_name : str, class_name : str, model : str, orm : str | None, async_orm : str | None):
        self.table_schema = table_schema
        self.table_name = table_name
        self.class_name = class_name
        self.model = model
        self.orm = orm
        self.async_orm = async_orm

class RoutineBuilderData:
    def __init__(self, table_schema : str, stp_name : str, content_stp : str, content_async_stp : str):
        self.table_schema = table_schema
        self.stp_name = stp_name
        self.content_stp = content_stp
        self.content_async_stp = content_async_stp

class BuilderData(object):
    def __init__(self, table_catalog : str):
        self.table_catalog = table_catalog
        self.talbes : list[TableBuilderData] = []
        self.routines : list[RoutineBuilderData] = []

class ModelBuilder(object):

    class TableOptions(object):
        def __init__(self, table_name : str, *, create_orm=True, ignore_table=False):
            self.table_name = table_name
            self.create_orm = create_orm
            self.ignore_table = ignore_table

    class RoutineOptions(object):
        def __init__(self, routine_name : str, ignore_routine=False):
            self.routine_name = routine_name
            self.ignore_routine = ignore_routine

    def __init__(self, dapper):
        self._dapper = dapper
        self.query_tables = f"""
            SELECT c.TABLE_CATALOG, c.TABLE_SCHEMA, c.TABLE_NAME, c.DATA_TYPE, c.COLUMN_NAME, c.IS_NULLABLE
            FROM (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE') t
            JOIN (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            ) c ON t.TABLE_NAME = c.TABLE_NAME
        """

        self.query_routines = f"""
            SELECT 
                p.SPECIFIC_NAME,
                p.PARAMETER_NAME,
                p.DATA_TYPE,
                p.SPECIFIC_CATALOG,
                p.SPECIFIC_SCHEMA,
                p.ORDINAL_POSITION,
                sm.definition AS PROCEDURE_DEFINITION
            FROM 
                INFORMATION_SCHEMA.PARAMETERS p
            JOIN 
                INFORMATION_SCHEMA.ROUTINES r ON p.SPECIFIC_NAME = r.SPECIFIC_NAME
            JOIN 
                sys.sql_modules sm ON OBJECT_NAME(sm.object_id) = r.SPECIFIC_NAME
            WHERE 
                r.ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY 
                p.SPECIFIC_NAME, p.ORDINAL_POSITION;
        """

    @property
    def dapper(self):
        return self._dapper

    def get_info_model_db(self):
        with self.dapper.query() as db:
            information_schema_tables = db.fetchall(self.query_tables)
            if not information_schema_tables.success:
                return False
            information_schema_tables = self.dapper.load(InformationSchemaTables, information_schema_tables)
            information_schema_tables = [table for table in information_schema_tables if not table.TABLE_NAME.startswith('__')]

        information_schema_tables.sort(key=lambda x: x.TABLE_NAME)
        grouped_data = groupby(information_schema_tables, lambda  x: x.TABLE_NAME)
        grouped_list : list[list[InformationSchemaTables]] = [[obj for obj in group] for _, group in grouped_data]
        if not grouped_list:
            return False
        return grouped_list

    def get_info_routines_db(self):
        with self.dapper.query() as db:
            information_schema_routines = db.fetchall(self.query_routines)
            if not information_schema_routines:
                return []
            information_schema_routines = self.dapper.load(InformationSchemaRoutines, information_schema_routines)

        information_schema_routines.sort(key=lambda x: x.SPECIFIC_NAME)
        grouped_data = groupby(information_schema_routines, lambda  x: x.SPECIFIC_NAME)
        grouped_list : list[list[InformationSchemaRoutines]] = [[obj for obj in group] for _, group in grouped_data]
        if not grouped_list:
            return []
        return grouped_list

    def create_model_db(self, dir_path : str, create_orm = True, create_stp = True, *, table_catalog : str | list[str] | tuple[str] = "all",
                          table_schema : str | list[str] | tuple[str] = "all",
                          tables_options : list[TableOptions] = [], routines_oprions : list[RoutineOptions] = []):

        dict_tables_options = {}
        if tables_options:
            dict_tables_options = {options.table_name : options for options in tables_options}
            create_orm = False
            for options in tables_options:
                if options.create_orm:
                    create_orm = True
                    break

        dict_routines_options = {options.routine_name : options for options in routines_oprions}
        if routines_oprions:
            create_stp = False
            for options in routines_oprions:
                if not options.ignore_routine:
                    create_stp = True
                    break

        information_db = self.get_info_model_db()
        information_routines = []
        if create_stp:
            information_routines = self.get_info_routines_db()
        if not information_db:
            return False

        table_catalog = [table_catalog] if isinstance(table_catalog, str) and table_catalog != "all" else table_catalog
        table_schema = [table_schema] if isinstance(table_schema, str) and table_schema != "all" else table_schema
       
        builder_data : dict[str, BuilderData] = {}
        import_init_db = ""
        for data in information_db:

            if table_catalog != "all":
                if data[0].TABLE_CATALOG not in table_catalog :
                    continue

            if table_schema != "all":
                if data[0].TABLE_SCHEMA not in table_schema :
                    continue

            table_options = dict_tables_options.get(data[0].TABLE_NAME)
            if table_options:
                if table_options.ignore_table:
                    continue

            content_model = '''# -*- coding: latin -*-

from dapper_sqls import TableBaseModel
from datetime import datetime
from pydantic import Field
from typing import Union
        
        '''

            table_name = data[0].TABLE_NAME
            class_name = table_name.replace("TBL_", "")
            schema = data[0].TABLE_SCHEMA

            fields = [create_field(row) for row in data]
            fields_str = "\n    ".join(fields)

            content_model += f'''
class {class_name}(TableBaseModel):
    _TABLE_NAME: str = '[{schema}].[{table_name}]'

    {fields_str}
\n
            '''

            fields_args = [create_field(row, "None") for row in data]
            fields_args_str = ", ".join(fields_args)

            table_create_orm = create_orm
            if table_options:
                    table_create_orm = table_options.create_orm

            content_orm = create_content_orm(class_name, fields_args_str) if table_create_orm else None
            content_async_orm = create_content_async_orm(class_name, fields_args_str) if table_create_orm else None

            catalog = data[0].TABLE_CATALOG
            if catalog not in builder_data:
                builder_data[catalog] = BuilderData(catalog)

            table_builder_data = TableBuilderData(schema, table_name, class_name, content_model, content_orm, content_async_orm)
            builder_data[catalog].talbes.append(table_builder_data)
      
        for data in information_routines:

            if table_catalog != "all":
                if data[0].SPECIFIC_CATALOG not in table_catalog :
                    continue

            if table_schema != "all":
                if data[0].SPECIFIC_SCHEMA not in table_schema :
                    continue

            routine_oprions = dict_routines_options.get(data[0].SPECIFIC_NAME)
            if routine_oprions:
                if routine_oprions.ignore_routine:
                    continue
            
            defaults_values = get_parameters_with_defaults(data[0].PROCEDURE_DEFINITION)
            params_routine = [create_params_routine(row, defaults_values) for row in data]
            params_routine_str = ", ".join(params_routine)

            stp_name = data[0].SPECIFIC_NAME.replace('STP_', '')
            content_routine = f'''
    def {stp_name}(self, *, {params_routine_str}):
        return StpBuilder(self.dapper, '[{data[0].SPECIFIC_SCHEMA}].[{data[0].SPECIFIC_NAME}]',locals())'''

            content_async_routine = f'''
    def {stp_name}(self, *, {params_routine_str}):
        return AsyncStpBuilder(self.async_dapper, '[{data[0].SPECIFIC_SCHEMA}].[{data[0].SPECIFIC_NAME}]', locals())'''
            
            catalog = data[0].SPECIFIC_CATALOG
            if catalog not in builder_data:
                builder_data[catalog] = BuilderData(catalog)

            builder_data[catalog].routines.append(RoutineBuilderData(data[0].SPECIFIC_SCHEMA, data[0].SPECIFIC_NAME, content_routine, content_async_routine))

        for catalog, data in builder_data.items():
            import_init_db += f"from .{catalog} import {catalog}\n"
  
            dir_catalog = os.path.join(dir_path, catalog)
            schema_data_tables : dict[str, list[TableBuilderData]] = {}
            for table in data.talbes:
                if table.table_schema not in schema_data_tables:
                    schema_data_tables[table.table_schema] = []

                dir_schema = os.path.join(dir_catalog, table.table_schema)
                dir_table = os.path.join(dir_schema, table.table_name)

                if not os.path.exists(dir_table):
                    os.makedirs(dir_table)

                table_options = dict_tables_options.get(table.table_name)

                table_create_orm = create_orm
                if table_options:
                    table_create_orm = table_options.create_orm

                if table_create_orm:
                    with open(os.path.join(dir_table ,'orm.py'), 'w', encoding='utf-8') as file:
                        file.write(''.join(table.orm))

                    with open(os.path.join(dir_table ,'async_orm.py'), 'w', encoding='utf-8') as file:
                        file.write(''.join(table.async_orm))

                with open(os.path.join(dir_table ,f'__init__.py'), 'w', encoding='utf-8') as file:
                    if table_create_orm:
                        file.write(f'from .orm import {table.class_name}ORM\nfrom .async_orm import Async{table.class_name}ORM\nfrom .model import {table.class_name}')
                    else:
                        file.write(f'from .model import {table.class_name}')

                with open(os.path.join(dir_table ,'model.py'), 'w', encoding='utf-8') as file:
                    file.write(''.join(table.model))

                
                schema_data_tables[table.table_schema].append(table)

            schema_data_routine : dict[str, list[RoutineBuilderData]] = {}
            content_file_routine = '''# -*- coding: latin -*-
from dapper_sqls import StpBuilder
from dapper_sqls import Dapper
from datetime import datetime
from typing import Union

class stp(object):

    def __init__(self, dapper : Dapper):
        self._dapper = dapper

    @property
    def dapper(self):
        return self._dapper
            '''

            content_file_async_rounine = '''# -*- coding: latin -*-
from dapper_sqls import AsyncStpBuilder
from dapper_sqls import AsyncDapper
from datetime import datetime
from typing import Union

class async_stp(object):

    def __init__(self, async_dapper : AsyncDapper):
        self._async_dapper = async_dapper

    @property
    def async_dapper(self):
        return self._async_dapper
            '''

            for routine in data.routines:
                if routine.table_schema not in schema_data_routine:
                    schema_data_routine[routine.table_schema] = []

                dir_schema = os.path.join(dir_catalog, routine.table_schema)
                if not os.path.exists(dir_schema):
                    os.makedirs(dir_schema)

                content_file_routine += f'{routine.content_stp}\n' 
                content_file_async_rounine += f'{routine.content_async_stp}\n' 

            if data.routines:
                dir_schema = os.path.join(dir_catalog, data.routines[0].table_schema)
                with open(os.path.join(dir_schema ,'routines.py'), 'w', encoding='utf-8') as file:
                     file.write(''.join(content_file_routine))
                with open(os.path.join(dir_schema ,'async_routines.py'), 'w', encoding='utf-8') as file:
                     file.write(''.join(content_file_async_rounine))

            import_init_catalog = ""
            class_init_catalog = f"class {catalog}(object):\n"
         
            for schema, data in schema_data_tables.items():
                import_init_catalog += f"from .{schema} import schema_{schema}\n"
                class_init_catalog += f"\n    class {schema}(schema_{schema}):\n        ...\n"
                import_init_schema = ""
                class_init_schema = ""
                class_models_schema = "    class models(object):\n"
                class_orm_schema = "    class orm(object):\n        def __init__(self, dapper : Dapper):\n"
                class_async_orm_schema = "    class async_orm(object):\n        def __init__(self, async_dapper : AsyncDapper):\n"
                for table in data:

                    table_options = dict_tables_options.get(table.table_name)
                    table_create_orm = create_orm
                    if table_options:
                        table_create_orm = table_options.create_orm

                    dir_schema = os.path.join(dir_catalog, schema)
                    class_models_schema += f"\n        class {table.class_name}({table.class_name}):\n            ...\n"
                    if table_create_orm:
                        class_orm_schema += f"            self.{table.class_name} = {table.class_name}ORM(dapper)\n"
                        class_async_orm_schema += f"            self.{table.class_name} = Async{table.class_name}ORM(async_dapper)\n"
                        import_init_schema += f"from .{table.table_name} import {table.class_name}, {table.class_name}ORM, Async{table.class_name}ORM\n"
                        class_init_schema += f"\n    class {table.class_name}ORM({table.class_name}ORM):\n        ...\n"
                        class_init_schema += f"\n    class Async{table.class_name}ORM(Async{table.class_name}ORM):\n        ...\n"
                    else:
                        import_init_schema += f"from .{table.table_name} import {table.class_name}\n"

                if information_routines :
                    import_init_schema += "from .routines import stp\nfrom .async_routines import async_stp\n"

                class_stp = "\n    class stp(stp):\n        ...\n" if information_routines else ""
                class_async_stp = "\n    class async_stp(async_stp):\n        ...\n" if information_routines else ""
                
                class_schema = f"class schema_{schema}(object):\n"
                if create_orm:
                    class_init_schema = f"{class_schema}{class_stp}{class_async_stp}\n{class_models_schema}\n{class_orm_schema}\n{class_async_orm_schema}\n{class_init_schema}"
                    content_init_schema = f"{import_init_schema}\nfrom dapper_sqls import Dapper, AsyncDapper\n\n{class_init_schema}"
                else:
                    class_init_schema = f"{class_schema}{class_stp}{class_async_stp}\n{class_models_schema}"
                    content_init_schema = f"{import_init_schema}\n\n{class_init_schema}"

                with open(os.path.join(dir_schema ,f'__init__.py'), 'w', encoding='utf-8') as file:
                    file.write(''.join(content_init_schema))

            content_init_catalog = f"{import_init_catalog}\n\n{class_init_catalog}"
            with open(os.path.join(dir_catalog ,f'__init__.py'), 'w', encoding='utf-8') as file:
                    file.write(''.join(content_init_catalog))

        if builder_data:
            #with open(os.path.join(dir_path ,f'__init__.py'), 'w', encoding='utf-8') as file:
            #        file.write(''.join(import_init_db))

            return True