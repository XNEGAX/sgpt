from __future__ import print_function
import sys
from django.db import connections
from django.http import JsonResponse
from datetime import datetime
from django.utils.html import strip_tags
from dateutil.parser import parse

mes_nombre_completo = {
    'january': 'Enero',
    'february': 'Febrero',
    'march': 'Marzo',
    'april': 'Abril',
    'may': 'Mayo',
    'june': 'Junio',
    'july': 'Julio',
    'august': 'Agosto',
    'september': 'Septiembre',
    'october': 'Octubre',
    'november': 'Noviembre',
    'december': 'Diciembre',
}

def getDatetime():
    import pytz
    return datetime.now(tz=pytz.timezone('Chile/Continental'))

def formatear_error(error):
    return f'Error en la linea {format(sys.exc_info()[-1].tb_lineno)} {type(error).__name__} {error}'

class ConsultaBD(object):
    def __init__(self,procedimiento,parametros=()):
        self.procedimiento = procedimiento
        self.parametros = parametros

    def rows_to_dict_list(self,cursor):
        columns = [i[0] for i in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]
    
    def execute_proc(self,onefetch=False):
        cursor = connections['default'].cursor()
        try:
            cursor.callproc(self.procedimiento,self.parametros)
            data = self.rows_to_dict_list(cursor)
            if onefetch:
                data = data[0] if len(data)>0 else data
            cursor.close()
            return data
        except Exception as exc:
            print(formatear_error(exc)) 
        return [] if not onefetch else {}

    def execute_lines(self):
        cursor = connections['default'].cursor()
        try:
            cursor.execute(self.procedimiento)
            data = self.rows_to_dict_list(cursor)
            cursor.close()
            return data
        except Exception as exc:
            return formatear_error(exc)


class JsonGenericView(object):
    """ Se extiende de esta clase cuando se requiere obtener la respuesta de una vista generica en formato json """
    def form_invalid(self, form):
        try:
            for elem in form:
                for k, v in form.errors.items():
                    if k == elem.name:
                        return JsonResponse({
                            'estado': '1',
                            'error': strip_tags(v)
                        }, status=200,safe=False)
        except Exception as exc:
            return JsonResponse({'estado': '1','error':formatear_error(exc)}, status=500,safe=False)

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            if hasattr(self.object, 'responsable_id'):
                self.object.responsable_id = self.request.user.id
            self.object.save()
            
            context = {
                'estado': '0',
                'mensaje': 'Operación exitosa',
                'id': self.object.pk,
            }
            return JsonResponse(context, status=200)
        except Exception as exc:
            return JsonResponse({'estado': '1','error':formatear_error(exc)}, status=500,safe=False)
        

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False
    