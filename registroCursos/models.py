from django.db import models
from django.contrib.auth.models import User

grados = (('lic', "Licenciatura"), ("mtr", 'Maestria'), ('doc', 'Doctorado'))
puestos = (('docente', "Docente"), ('jefe', "Jefe Depto"))

ene_jun = 'ene_jun'
ago_dic = 'ago_dic'

semestres = ((ago_dic, 'Ago - Dic'), (ene_jun, 'Ene - Jun'))


class Alumno(models.Model):

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default='')
    apellidoPaterno = models.CharField(max_length=15, default='')
    apellidoMaterno = models.CharField(max_length=15, default='')
    nombre = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    grado = models.CharField(max_length=4, choices=grados, default='')
    departamento = models.CharField(max_length=20)
    puesto = models.CharField(max_length=7, choices=puestos, default='')
    RFC = models.CharField(max_length=14, blank=True)
    CURP = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return '{} {} , {}'.format(self.apellidoPaterno, self.apellidoMaterno, self.nombre)

    class Meta:
        db_table = 'Alumno'


class Instructor(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, default='')
    apellidoPaterno = models.CharField(max_length=15, default='')
    apellidoMaterno = models.CharField(max_length=15, default='')
    nombre = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    grado = models.CharField(max_length=4, choices=grados)
    departamento = models.CharField(max_length=20)
    puesto = models.CharField(max_length=7, choices=puestos, default='')
    RFC = models.CharField(max_length=14, blank=True)
    CURP = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return '{} {} , {}'.format(self.apellidoPaterno, self.apellidoMaterno, self.nombre)

    class Meta:
        verbose_name_plural = "Instructores"
        db_table = 'Instructor'


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    alumnos = models.ManyToManyField(Alumno)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, verbose_name="Instructor", blank=True)
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
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return self.curso.nombre

    class Meta:
        db_table = 'Historial'

