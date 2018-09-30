from django.contrib import admin
from .models import Curso, Alumno, Instructor ,Clase


# Register your models here.

admin.site.register(Alumno)
admin.site.register(Instructor)
admin.site.register(Curso)
admin.site.register(Clase)
