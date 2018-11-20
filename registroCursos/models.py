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

evaluacion = ((5,"Totalmente de Acuerdo"),(4,"Parcialmente de Acuerdo"),
                (3,"Indiferente"),(2,"Parcialmente"),
                (1,"Totalmente en Desacuerdo"))

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    sexo = models.CharField(max_length = 1, choices=sexos, default='',blank=True)

    nombramiento = models.CharField(max_length=3,choices=nombramientos , default='')

    Horas = models.IntegerField(blank=True, default='')

    grado = models.CharField(max_length=4, choices=grados, default='')

    departamento = models.CharField(max_length=20,blank=True,default='')

    puesto = models.CharField(max_length=7, choices=puestos, default='')

    telefono_particular = models.BigIntegerField(blank=True, default='')

    RFC = models.CharField(max_length=14, blank=True, default='')

    CURP = models.CharField(max_length=18, blank=True, default='')

    def __str__(self):
        return self.user.get_full_name()
    class Meta:
        verbose_name_plural = "UserProfile"
        db_table = 'UserProfile'

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor", blank=True,null=True)

    tipo = models.CharField(max_length=3, choices=cursos,default='')

    alumno = models.ManyToManyField(User, related_name="alumno",through='Historial', blank=True,default="")

    colaborador = models.ForeignKey(User,on_delete = models.CASCADE, related_name='colaborador',blank=True, default='',null=True)

    semestre = models.CharField(max_length=20, choices=semestres, default='')

    anno = models.IntegerField(blank=True)

    dia_inicio = models.DateField(blank=True)

    dia_final = models.DateField(blank=True)

    hora_inicio = models.TimeField(blank=True)

    hora_final = models.TimeField(blank=True)

    salon = models.IntegerField(blank=True)


    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Curso'


class Historial(models.Model):

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    alumno = models.ForeignKey(User, on_delete=models.CASCADE)

    aprobado = models.BooleanField(default=False)

    calificacion = models.IntegerField(default=0)

    def __str__(self):
        return self.curso.nombre

    class Meta:
        verbose_name_plural = "Historial"
        db_table = 'Historial'
        
class Asistencia(models.Model):

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    alumno = models.ForeignKey(User, on_delete=models.CASCADE)

    dia = models.DateField()

    asistio = models.BooleanField(default=False)

    def __str__(self):
        return self.curso.nombre + " "+ self.alumno.get_full_name() + " " +str(self.dia)

    class Meta:
        verbose_name_plural = "Asistencia"
        db_table = "Asistencia"

class Encuesta(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    alumno = models.ForeignKey(User, on_delete=models.CASCADE)

    pregunta_1 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_2 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_3 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_4 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_5 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_6 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_7 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_8 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_9 = models.CharField(max_length=2,choices=evaluacion,default='')

    pregunta_10 = models.CharField(max_length=2,choices=evaluacion,default='')

    def __str__(self):
        return self.curso.nombre

    class Meta:
        verbose_name_plural = "Encuesta"
        db_table = "Encuesta"