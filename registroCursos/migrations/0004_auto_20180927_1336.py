# Generated by Django 2.1.1 on 2018-09-27 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registroCursos', '0003_auto_20180927_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='apellidoMaterno',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='alumno',
            name='apellidoPaterno',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='alumno',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='alumno',
            name='nombre',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='instructor',
            name='apellidoMaterno',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='instructor',
            name='apellidoPaterno',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='instructor',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='instructor',
            name='nombre',
            field=models.CharField(default='', max_length=20),
        ),
    ]
