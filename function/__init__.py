import sys
from django.db import connections

def formatear_error(error):
    return f'Error en la linea {format(sys.exc_info()[-1].tb_lineno)} {type(error).__name__} {error}'

class ConsultaBD(object):
    def __init__(self,procedimiento,parametros=()):
        self.procedimiento = procedimiento
        self.parametros = parametros

    def rows_to_dict_list(self,cursor):
        columns = [i[0] for i in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def execute(self):
        cursor = connections['default'].cursor()
        try:
            cursor.callproc(self.procedimiento,self.parametros)
            data = self.rows_to_dict_list(cursor)
            cursor.close()
            return data
        except Exception as exc:
            return formatear_error(exc)