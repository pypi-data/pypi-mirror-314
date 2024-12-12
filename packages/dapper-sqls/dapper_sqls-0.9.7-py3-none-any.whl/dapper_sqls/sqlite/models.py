# -*- coding: latin -*-

class BaseTableModel(object):
    def __init__(self, dados : dict):
        self.id : int = dados['id']
        self.App : str = dados['App'] 

class Path(BaseTableModel):
    def __init__(self, dados : dict):
       super().__init__(dados)
       self.Name : str = dados['Name']
       self.Path : str = dados['Path']

class EnvVar(BaseTableModel):
    
    def __init__(self, dados : dict):
       super().__init__(dados)
       self.Name : str = dados['Name']
       self.Value : str = dados['Value']

class System(BaseTableModel):
    def __init__(self, dados : dict):
       super().__init__(dados)
       self.Theme : str = dados['Tema']


   
    


