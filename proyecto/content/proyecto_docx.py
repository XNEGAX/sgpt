from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

class ProyectoDocx(object):
    def __init__(self,proyecto) -> None:
        self.proyecto = proyecto

    def getDocumento(self):
        return self.generate_docx()
    
    def get_html(self):
        return render_to_string('documento/docx/index.html',{'proyecto':self.proyecto})

    def generar(self,nombre):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"inline; {nombre}"
        HTML(string=self.get_html()).write_pdf(response)
        return response