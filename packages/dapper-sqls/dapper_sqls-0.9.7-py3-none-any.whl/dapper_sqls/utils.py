# -*- coding: latin -*-

def get_dict_args(local : dict , ignore_args = [], ignore_values_none = True):
    if ignore_values_none:
        return {k: v for k, v in local.items() if k != 'self' and k != 'cls' and v != None and k not in ignore_args}
    return {k: v for k, v in local.items() if k != 'self' and k != 'cls' and k not in ignore_args}

class ArgsStored:
    def __init__(self, model : object | None, query : str | None, params : list | tuple | None, additional_sql : str, select_top : int | None):
        self.model = model
        self.query = query
        self.params = params
        self.additional_sql = additional_sql if isinstance(additional_sql, str) else ""
        self.select_top = select_top if isinstance(select_top, int) else None

class ArgsQuery:
    def __init__(self, model : object | None, query : str | None, additional_sql : str, select_top : int | None):
        self.model = model
        self.query = query
        self.additional_sql = additional_sql
        self.select_top = select_top

class ArgsSTP:
    def __init__(self, model : object | None, attempts : str | None, wait_timeout : str | None):
        self.model = model
        self.attempts = attempts
        self.wait_timeout = wait_timeout
        

class Utils(object):

    @staticmethod
    def args_stored(*args, **kwargs):
        query = kwargs.get('query')
        model = kwargs.get('model')
        params = kwargs.get('params')
        additional_sql = kwargs.get('additional_sql', '')
        select_top = kwargs.get('select_top')

        if not query and not model:
            if isinstance(args[0], str):
                query = args[0] 
                params = args[1:]
                if len(params) == 1 and isinstance(params[0], (list, tuple)):
                    params = params[0]
                params = tuple(params)

            else:
                model = args[0]
                if not additional_sql.strip():
                    if len(args) > 1:
                        additional_sql = args[1] if len(args) > 1 else ""
                if not select_top:
                    select_top = args[2] if len(args) > 2  else None

        return ArgsStored(model, query, params, additional_sql, select_top)


    @staticmethod
    def args_query(*args, **kwargs):
        query = kwargs.get('query')
        model = kwargs.get('model')
        additional_sql = kwargs.get('additional_sql', '')
        select_top = kwargs.get('select_top')

        if not query and not model:
            if  isinstance(args[0], str):
                query = args[0]
            else:
                model = args[0]
                if not additional_sql.strip():
                    additional_sql = args[1] if len(args) > 1 else ""
                if not select_top:
                    select_top = args[2] if len(args) > 2 and not select_top else None

        return ArgsQuery(model, query, additional_sql, select_top)

    @staticmethod
    def args_stp(*args, **kwargs):
        model = kwargs.get('model')
        attempts = kwargs.get('attempts')
        wait_timeout = kwargs.get('wait_timeout')
        if not model:
            model = args[0] if len(args) > 0 else None
            attempts = args[1] if len(args) > 1 else None
            wait_timeout = args[2] if len(args) > 2 else None

        return ArgsSTP(model, attempts, wait_timeout)

