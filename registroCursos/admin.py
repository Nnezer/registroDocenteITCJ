from django.contrib import admin
from .models import Perfil,Curso,Historial, Asistencia,Encuesta

                                       
# Register your models here.
admin.site.register(Perfil)
admin.site.register(Curso)
admin.site.register(Historial)
admin.site.register(Asistencia)
admin.site.register(Encuesta)
