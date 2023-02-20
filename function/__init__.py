import sys
from django.db import connections
from django.http import JsonResponse
from datetime import datetime
from django.utils.html import strip_tags

def formatear_error(error):
    return f'Error en la linea {format(sys.exc_info()[-1].tb_lineno)} {type(error).__name__} {error}'

class ConsultaBD(object):
    def __init__(self,procedimiento,parametros=()):
        self.procedimiento = procedimiento
        self.parametros = parametros

    def rows_to_dict_list(self,cursor):
        columns = [i[0] for i in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def execute_proc(self):
        cursor = connections['default'].cursor()
        try:
            cursor.callproc(self.procedimiento,self.parametros)
            data = self.rows_to_dict_list(cursor)
            cursor.close()
            return data
        except Exception as exc:
            return formatear_error(exc)

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
            if hasattr(self.object, 'fecha_desde'):
                self.object.fecha_desde = self.object.fecha_desde.strftime("%Y-%m-%d")
            if hasattr(self.object, 'fecha_hasta'):
                self.object.fecha_hasta = self.object.fecha_hasta.strftime("%Y-%m-%d")
            self.object.save()
            
            context = {
                'estado': '0',
                'mensaje': 'Operación exitosa',
                'id': self.object.pk,
            }
            return JsonResponse(context, status=200)
        except Exception as exc:
            return JsonResponse({'estado': '1','error':formatear_error(exc)}, status=500,safe=False)