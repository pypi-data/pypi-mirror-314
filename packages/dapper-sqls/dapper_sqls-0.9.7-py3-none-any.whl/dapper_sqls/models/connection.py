# -*- coding: latin -*-

class ConnectionStringData(object):
    def __init__(self, server: str, database: str, username: str, password: str):
        self._server = server
        self._database = database
        self._username = username
        self._password = password

    @property
    def server(self) -> str:
        return self._server

    @server.setter
    def server(self, value: str):
        if not isinstance(value, str):
            raise ValueError("O valor do servidor deve ser uma string.")
        self._server = value

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value: str):
        if not isinstance(value, str):
            raise ValueError("O nome do banco de dados deve ser uma string.")
        self._database = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        if not isinstance(value, str):
            raise ValueError("O nome de usuário deve ser uma string.")
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        if not isinstance(value, str):
            raise ValueError("A senha deve ser uma string.")
        self._password = value

    def get(self, server : str , database : str, username : str, password : str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def get(self):
        return ConnectionStringData(self.server, self.database, self.username, self.password)



