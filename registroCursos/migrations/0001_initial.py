# Generated by Django 2.1.1 on 2018-09-25 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('apellidoPaterno', models.CharField(max_length=15)),
                ('apellidoMaterno', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('grado', models.CharField(choices=[('Lic.', 'Licenciatura'), ('Mtr.', 'Maestria'), ('Doc.', 'Doctorado')], default='', max_length=4)),
                ('departamento', models.CharField(max_length=20)),
                ('puesto', models.CharField(choices=[('docente', 'Docente'), ('jefe', 'Jefe Depto')], default='', max_length=7)),
                ('RFC', models.CharField(blank=True, max_length=14)),
                ('CURP', models.CharField(blank=True, max_length=18)),
            ],
            options={
                'db_table': 'Alumno',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('semestre', models.CharField(choices=[('ago_dic', 'Ago - Dic'), ('ene_jun', 'Ene - Jun')], default='', max_length=20)),
                ('anno', models.IntegerField()),
                ('diaInicio', models.DateField()),
                ('diaFinal', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFinal', models.TimeField()),
                ('salon', models.IntegerField()),
                ('alumnos', models.ManyToManyField(blank=True, to='registroCursos.Alumno')),
            ],
            options={
                'db_table': 'Curso',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('apellidoPaterno', models.CharField(max_length=15)),
                ('apellidoMaterno', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('grado', models.CharField(choices=[('Lic.', 'Licenciatura'), ('Mtr.', 'Maestria'), ('Doc.', 'Doctorado')], max_length=4)),
                ('departamento', models.CharField(max_length=20)),
                ('puesto', models.CharField(choices=[('docente', 'Docente'), ('jefe', 'Jefe Depto')], default='', max_length=7)),
                ('RFC', models.CharField(blank=True, max_length=14)),
                ('CURP', models.CharField(blank=True, max_length=18)),
            ],
            options={
                'verbose_name_plural': 'Instructores',
                'db_table': 'Instructor',
            },
        ),
        migrations.AddField(
            model_name='curso',
            name='instructor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='registroCursos.Instructor', verbose_name='Instructor'),
        ),
    ]