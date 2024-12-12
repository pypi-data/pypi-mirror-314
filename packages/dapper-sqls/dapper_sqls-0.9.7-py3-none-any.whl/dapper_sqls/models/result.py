# -*- coding: latin -*-

def result_dict(cursor, result):
        return dict(
                zip(
                    [column[0] for column in cursor.description],
                    result
                )
                )

class Result(object):
    
    class Fetchone(object):
        def __init__(self, cursor, result, status_code = 200, message : str = ""):
            self._status_code = status_code
            self._message = message
            if result:
                self._success = True
                self._list = result
                self._dict = dict(zip([column[0] for column in cursor.description], result))
            else:
                self._success = False
                self._list = []
                self._dict = {}

        @property
        def status_code(self):
            return self._status_code

        @property
        def list(self):
            return self._list

        @property
        def dict(self):
            return self._dict

        @property
        def success(self):
            return self._success
        
        @property
        def message(self):
            return self._message


    class Fetchall:

        def __init__(self, cursor, result, status_code = 200, message : str = ""):
            self._status_code = status_code
            self._message = message
            if result:
                self._success = True
                self._list_dict = []
                for r in result:
                    self._list_dict.append(dict(zip([column[0] for column in cursor.description], r)))
            else:
                self._success = False
                self._list_dict = []

        @property
        def status_code(self):
            return self._status_code

        @property
        def list_dict(self):
            return self._list_dict

        @property
        def dict(self):
            return self._dict

        @property
        def success(self):
            return self._success
        
        @property
        def message(self):
            return self._message

    class Insert:
        def __init__(self, result : int | str, status_code = 200, message : str = ""):
            self._id = result
            self._status_code = status_code
            self._success = bool(result)
            self._message = message

        @property
        def id(self):
            return self._id

        @property
        def status_code(self):
            return self._status_code

        @property
        def success(self):
            return self._success
        
        @property
        def message(self):
            return self._message

    class Send:
        def __init__(self, result : bool, status_code = 200, message : str = ""):
            self._status_code = status_code
            self._success = result
            self._message = message

        @property
        def status_code(self):
            return self._status_code

        @property
        def success(self):
            return self._success
        
        @property
        def message(self):
            return self._message



