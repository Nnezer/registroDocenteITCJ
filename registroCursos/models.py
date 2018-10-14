from django.db import models
from django.contrib.auth.models import User

grados = (('lic', "Licenciatura"), ("mtr", 'Maestria'), ('doc', 'Doctorado'))
puestos = (('docente', "Docente"), ('jefe', "Jefe Depto"))
sexos = (('H','Hombre'), ('M','Mujer'))
ene_jun = 'ene_jun'
ago_dic = 'ago_dic'
nombramientos = (('TC',"Tiempo Completo"),('3/4',"3/4"),('1/2',"1/2"),('PA',"Por Asignatura")
                    ,('HN',"Honorarios"),('HA',"Horas Administrativas"),('DIR',"Directivo"))

cursos = (("AP","Actualizacion Profesional"),("FD","Formacion Docente"),
        ("DT","Diplomado en Tutorias"),("DC","Diplomado en Competencias"),
        ("APD","Actualizacion Profesional y Formacion Docente"))

semestres = ((ago_dic, 'Ago - Dic'), (ene_jun, 'Ene - Jun'))


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sexo = models.CharField(max_length = 1, choices=sexos, default='')
    nombramiento = models.CharField(max_length=3,choices=nombramientos , default='')
    email = models.EmailField(default='')
    grado = models.CharField(max_length=4, choices=grados, default='')
    departamento = models.CharField(max_length=20,default='')
    puesto = models.CharField(max_length=7, choices=puestos, default='')
    RFC = models.CharField(max_length=14, blank=True)
    CURP = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=cursos,default='')
    alumno = models.ManyToManyField(User, related_name="alumno", blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor", blank=True)
    semestre = models.CharField(max_length=20, choices=semestres, default='')
    anno = models.IntegerField()
    diaInicio = models.DateField()
    diaFinal = models.DateField()
    horaInicio = models.TimeField()
    horaFinal = models.TimeField()
    salon = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Curso'


class Historial(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    enCurso= models.BooleanField(default=False)
    aprobado = models.BooleanField(default=False)
    calificacion = models.IntegerField(default=0)

    def __str__(self):
        return self.curso.nombre

    class Meta:
        verbose_name_plural = "Historial"
        db_table = 'Historial'
        

