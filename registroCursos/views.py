from django.utils import timezone
from django.views.generic import View
from registroCursos.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *
#import fill_poll
from datetime import date, timedelta, datetime
from .choices import * 
from django.http import JsonResponse

day, month, year = timezone.now().strftime('%d/%m/%Y').split("/")
currentSemester = "ago_dic" if int(month) >= 7 else "ene_jun"

dict_results = {
    'grados': {
        'lic': {'Licenciatura':set() },
        'mtr': {'Maestria':set() },
        'doc': {'Doctorado':set() }
    },
    'puestos': {
        'docente': {'Docente':set() },
        'jefe': {'Jefe Depto':set() }
    },
    'sexos': {
        'H': {'Hombre':set() },
        'M': {'Mujer':set() }
    },
    'nombramientos': {
        'TC': {'Tiempo Completo':set() },
        '3/4': {'Tres Cuartos':set() },
        '1/2': {'1/2':set() },
        'PA': {'Por Asignatura':set() },
        'HN': {'Honorarios':set() },
        'HA': {'Horas Administrativas':set() },
        'DIR': {'Directivo':set() }
    },
    'areas': {
        'admin': {'Economico-Admvas':set() },
        'DVP': {'Division de Estudios Profesionales':set() },
        'RF': {'Recursos Financieros':set() },
        'EXT': {'Actividades Extraescolares':set() },
        'CBAS': {'Ciencias Basicas':set() },
        'CII': {'Campus II':set() },
        'CDC': {'Centro De Computo':set() },
        'CDI': {'Centro De Informacion':set() },
        'CYD': {'Comunicacion y Difusion':set() },
        'DA': {'Desarrollo Academico':set() },
        'DEP': {'Division de Estudios Profesionales':set() },
        'ED': {"Educacion a Distancia":set() },
        'ELEC': {"Electrica - Electronica":set() },
        'GTV': {'Gestion Tecnologica y Vinculacion':set() },
        'INDUS': {'ING. Industrial':set() },
        'MEM': {'Metal-Mecanica':set() },
        'PLA': {"Planeacion":set() },
        'POSG': {'Posgrado':set() },
        'RECMYS': {'Recursos Materiales y Servicios':set() },
        'RECF': {'Recursos Financieros':set() },
        'RECH': {'Recursos Humanos':set() },
        'SERV': {'Servicios Escolares':set() },
        'SYS': {'Sistemas Y Computacion':set() },
        'SUB': {'Subdireccion Academica':set() },
    } 
} 
 
class StatsUserView(View):
    template_name = "stats-user.html"
    def get(self, request, *args, **kwargs):
        id_user=self.kwargs["id_user"]

        historial = Historial.objects.filter(alumno_id = id_user)
        perfil = Perfil.objects.get(user_id = id_user)
        cursos = Curso.objects.filter(alumno__id=id_user)
        aprobados = historial.filter(aprobado = True).count()
        reprobados = historial.filter(aprobado = False).count()
 
        return render(request, self.template_name, locals())
    


class StatsIndividualView(View):
    template_name = 'stats-individual.html'
    def get(self, request, *args, **kwargs):
        option_semestres = dict(semestres)
        option_cursos = dict(cursos) 
        option_grados = dict(grados)
        option_puestos = dict(puestos)
        option_areas = dict(areas)
        option_nombramientos = dict(nombramientos)
        option_sexos = dict(sexos)
        results =  dict_results
        id_curso=self.kwargs["id_curso"]
        curso=Curso.objects.get(id=id_curso) 
        all_perfiles = Perfil.objects.all()
        alumnos = curso.alumno.all()
        historial = Historial.objects.filter(curso_id=id_curso)
        print(historial)
        list_alumnos = [] 
        for item in historial:
            list_alumnos.append(item.alumno.id)

        perfil_data = Perfil.objects.none() 
        for item in set(list_alumnos):
            perfil_data = perfil_data | all_perfiles.filter(id = item) 
        count_alumnos = curso.alumno.count()
        for alumno in set(list_alumnos): 
            user_to_stat = Perfil.objects.get(id=alumno)
            dict_results['grados'][user_to_stat.grado][option_grados[user_to_stat.grado]].add(user_to_stat) 
            dict_results['puestos'][user_to_stat.puesto][option_puestos[user_to_stat.puesto]].add(user_to_stat) 
            dict_results['sexos'][user_to_stat.sexo][option_sexos[user_to_stat.sexo]].add(user_to_stat) 
            dict_results['nombramientos'][user_to_stat.nombramiento][option_nombramientos[user_to_stat.nombramiento]].add(user_to_stat) 
            dict_results['areas'][user_to_stat.area][option_areas[user_to_stat.area]].add(user_to_stat) 
 
        count_hombres =  len(dict_results['sexos']['H']['Hombre'] )
        count_mujeres = len(dict_results['sexos']['M']['Mujer'] )
        grados_data = len(dict_results['grados'] )
        count_aprobados = historial.filter(aprobado=True).count()
        count_reprobados =historial.filter(aprobado=False).count()
        porcent_aprobados = 0 if count_alumnos == 0 else round((count_aprobados / count_alumnos) * 100,2)
        porcent_reprobados =  0 if count_alumnos == 0 else round((count_reprobados / count_alumnos) * 100,2)
        porcent_hombres = 0 if count_alumnos == 0 else round(count_hombres/count_alumnos * 100,2)
        porcent_mujeres = 0 if count_alumnos == 0 else round(count_mujeres/count_alumnos * 100,2) 
        
        
         
        return render(request, self.template_name, locals())

 

 
class ReportsView(View):
    template_name='reports.html'
    def get(self, request, *args, **kwargs):
        id_curso=self.kwargs["id_curso"]
        curso=Curso.objects.get(id=id_curso)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        id_curso=self.kwargs["id_curso"]
        curso=Curso.objects.get(id=id_curso)
        post_data=request.POST.copy()
        type_pdf=post_data['type_pdf']
        id_alumno=post_data['id_alumno']

        user_profile=Perfil.objects.get(id=id_alumno)

        user=User.objects.get(id=id_alumno)
        #fill_poll(user, user_profile, curso) 
        return render(request, self.template_name, locals()) 

class StatsGeneralView(View):
    template_name = 'stats.html'

    def get(self, request, *args, **kwargs): 

        option_semestres = dict(semestres)
        option_cursos = dict(cursos) 

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs): 
        
        results = dict_results

        option_semestres = dict(semestres)
        option_cursos = dict(cursos) 
        option_grados = dict(grados)
        option_puestos = dict(puestos)
        option_areas = dict(areas)
        option_nombramientos = dict(nombramientos)
        option_sexos = dict(sexos)

          
        post_data=request.POST.copy()  
        all_cursos = Curso.objects.all()
        all_historial = Historial.objects.all() 
        all_perfiles = Perfil.objects.all()

        cursos_data = all_cursos.filter(tipo__icontains=post_data['tipo'],
                                            nombre__icontains=post_data['nombre'],
                                            semestre__icontains=post_data['semestre'],
                                            anno = post_data['anno'])
    
        historial_data = Historial.objects.none() 
        for item in cursos_data:
            historial_data = historial_data | all_historial.filter(curso_id= item.id)
  
        
        # numero de alumnos en el query
        count_alumnos, count_hombres, count_mujeres,count_aprobados, count_reprobados = 0,0,0,0,0 

        for item in cursos_data:
            count_alumnos = count_alumnos + item.alumno.count() 
  
        list_alumnos = []
        perfil_data = Perfil.objects.none() 
        for item in historial_data:
            list_alumnos.append(item.alumno.id)
            if item.aprobado == True:
                count_aprobados += 1
            else:
                count_reprobados +=1 

        for item in set(list_alumnos):
            perfil_data = perfil_data | all_perfiles.filter(id = item)

        user_to_stat = Perfil.objects.none()  

        for alumno in set(list_alumnos): 
            user_to_stat = Perfil.objects.get(id=alumno)
            dict_results['grados'][user_to_stat.grado][option_grados[user_to_stat.grado]].add(user_to_stat) 
            dict_results['puestos'][user_to_stat.puesto][option_puestos[user_to_stat.puesto]].add(user_to_stat) 
            dict_results['sexos'][user_to_stat.sexo][option_sexos[user_to_stat.sexo]].add(user_to_stat) 
            dict_results['nombramientos'][user_to_stat.nombramiento][option_nombramientos[user_to_stat.nombramiento]].add(user_to_stat) 
            dict_results['areas'][user_to_stat.area][option_areas[user_to_stat.area]].add(user_to_stat) 
 
        count_hombres =  len(dict_results['sexos']['H']['Hombre'] )
        count_mujeres = len(dict_results['sexos']['M']['Mujer'] )
        grados_data = len(dict_results['grados'] )
        porcent_aprobados = 0 if count_alumnos == 0 else round((count_aprobados / count_alumnos) * 100,2)
        porcent_reprobados =  0 if count_alumnos == 0 else round((count_reprobados / count_alumnos) * 100,2)
        porcent_hombres = 0 if count_alumnos == 0 else round(count_hombres/count_alumnos * 100,2)
        porcent_mujeres = 0 if count_alumnos == 0 else round(count_mujeres/count_alumnos * 100,2) 
        return render(request, self.template_name, locals())

class PollView(View):
    template_name='user/poll.html'
    def get(self, request, *args, **kwargs):
        id_curso=self.kwargs["id_curso"]

        curso=Curso.objects.get(id=id_curso)

        is_instructor=True if curso.instructor_id == request.user.id else False

        is_alumno=True if Curso.objects.filter(
            id=id_curso, alumno=request.user.id) else False
        poll_done=True if Encuesta.objects.filter(
            curso_id=id_curso, alumno_id=request.user.id) else False

        return render(request, self.template_name, locals())
 
class PollDoneView(View):
    template_name='user/poll_done.html'
    def post(self, request, *args, **kwargs):
        post_data=request.POST.copy()

        encuesta=Encuesta(curso_id=post_data['curso_id'],
                                alumno_id=post_data['user_id'],
                                pregunta_1=post_data['question-1'],
                                pregunta_2=post_data['question-2'],
                                pregunta_3=post_data['question-3'],
                                pregunta_4=post_data['question-4'],
                                pregunta_5=post_data['question-5'],
                                pregunta_6=post_data['question-6'],
                                pregunta_7=post_data['question-7'],
                                pregunta_8=post_data['question-8'],
                                pregunta_9=post_data['question-9'],
                                pregunta_10=post_data['question-10'],
                                pregunta_11=post_data['question-11'],
                                            )
        encuesta.save()

        return render(request, self.template_name, locals())

class EvaluateDoneView(View):
    template_name='instructor/evaluate_done.html'
    def post(self, request, *args, **kwargs):
        post_data=request.POST.copy()
        id_curso=self.kwargs["id_curso"]
        id_user=self.kwargs['id_user']

        historial=Historial.objects.get(curso_id=id_curso, alumno_id=id_user)

        if "aprobado" in post_data:
            historial.aprobado=True
        if "calificacion" in post_data:
            historial.calificacion=post_data["calificacion"]
        historial.save()
        dias=[]
        for e in post_data:
            if e[0].isdigit():
                dias.append(e)

        for dia in dias:
            date=datetime.strptime(dia, '%d-%m-%Y')
            format_date=date.strftime('%Y-%m-%d')
            print(format_date)

            asistencia=Asistencia(
                curso_id=id_curso, alumno_id=id_user, dia=format_date, asistio=True)
            if not Asistencia.objects.filter(dia=format_date):
                asistencia.save()

        return render(request, self.template_name, locals())

class EvaluateView(View):
    template_name='instructor/evaluate.html'

    def get(self, request, *args, **kwargs):
        id_curso=self.kwargs["id_curso"]
        id_user=self.kwargs['id_user']

        curso=Curso.objects.get(id=id_curso)

        alumno=User.objects.get(id=id_user)

        delta=curso.dia_final - curso.dia_inicio
        dias=[]

        for i in range(delta.days + 1):
            dia=curso.dia_inicio + timedelta(i)
            if dia.weekday() != 6 and dia.weekday() != 5:
                dias.append(dia.strftime("%d-%m-%Y"))

        can_evaluate=True if curso.dia_final == timezone.now().date() else False

        has_alumno=True if curso.alumno.all().get(id=id_user) else False

        is_instructor=True if curso.instructor_id == request.user.id else False

        return render(request, self.template_name, locals())


class AdminCourseView(View):
    template_name='instructor/admin.html'

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):
        id_curso=self.kwargs["id_curso"]
        curso=Curso.objects.get(id=id_curso)
        alumnos=curso.alumno.all()

        is_instructor=True if curso.instructor_id == request.user.id else False

        return render(request, self.template_name, locals())


class UserProfileView(View):
    template_name='user/user_profile.html'

    def post(self, request, *args, **kwargs):
        post_data=request.POST.copy()


        user_profile=Perfil.objects.get(id=request.user.id)

        user=User.objects.get(id=request.user.id)

        dict_nombramiento=dict(nombramientos);


        for key, value in dict_nombramiento.items():
            print("Key: ", key, "Value: ", value)


        if User.objects.filter(username=post_data['username']) and not User.objects.filter(id=request.user.id, username=post_data['username']):
            error=['username']
        else:
            if User.objects.filter(email=post_data['email']) and not User.objects.filter(id=request.user.id, email=post_data['email']):
                error=error.append('email')
            else:
                user.first_name=post_data['first_name']
                user.last_name=post_data['last_name']
                user.username=post_data['username']
                user.email=post_data['email']
                user_profile.sexo=post_data['sexo']
                user_profile.nombramiento=post_data['nombramiento']
                user_profile.horas=post_data['horas']
                user_profile.grado=post_data['grado']
                user_profile.area=post_data['area']
                user_profile.puesto=post_data['puesto']
                user_profile.extension=post_data['extension']
                user_profile.jefe_inmediato=post_data['jefe_inmediato']
                user_profile.horario_inicio=post_data['horario_inicio']
                user_profile.horario_final=post_data['horario_final']
                user_profile.telefono_particular=post_data['telefono_particular']
                user_profile.RFC=post_data['RFC']
                user_profile.CURP=post_data['CURP']
                user.save()
                user_profile.save()

        return render(request, 'user/update_user_profile_done.html', locals())

    def get(self, request, *args, **kwargs):

        profile=Perfil.objects.get(id=request.user.id)

        form_profile=UpdateUserProfileForm()
        form_user=UpdateUserForm()

        return render(request, self.template_name, locals())

class UpdateUsernameView(View):
    template_name='user/update_username.html'

    def post(self, request, *args, **kwargs):
        post_data=request.POST.copy()
        user=User.objects.get(id=request.user.id)

        if User.objects.filter(username=post_data['username']):
            action=False
        else:
            user.username=post_data['username']
            user.save()
            action=True
        return render(request, 'user/update_username_done.html', locals())

    def get(self, request, *args, **kwargs):
        form=UpdateUserForm()
        return render(request, self.template_name, locals())


class UpdateEmailView(View):
    template_name='user/update_email.html'

    def post(self, request, *args, **kwargs):
        post_data=request.POST.copy()
        user=User.objects.get(id=request.user.id)

        if User.objects.filter(email=post_data['email']):
            action=False
        else:
            user.email=post_data['email']
            user.save()
            action=True
        return render(request, 'user/update_email_done.html', locals())

    def get(self, request, *args, **kwargs):
        form=UpdateUserForm()
        return render(request, self.template_name, locals())


class DetailView(View):
    template_name="detail.html"

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):

        id=self.kwargs.get('id_curso')
        curso=Curso.objects.get(id=id)

        onCourseAsInstructor=True if Curso.objects.filter(
            id=id, instructor=request.user.id) else False

        onCourseAsAlumno=True if Curso.objects.filter(
            id=id, alumno=request.user.id) else False

        onCourseAsColaborador=True if Curso.objects.filter(
            id=id, colaborador=request.user.id) else False

        time_to_poll=True if str(curso.dia_final) == timezone.now().strftime(
            '%Y-%m-%d') else False

        next_day=curso.dia_inicio + timedelta(days=1)

        first_day_pass=True if next_day < timezone.now().date() else False

        print(first_day_pass)

        return render(request, self.template_name, locals())


class ConfirmActionCourseView(View):
    template_name='user/course_confirm_action.html'

    def post(self, request, *args, **kwargs):

        post_data=request.POST.copy()
        action=post_data['action']
        curso=Curso.objects.get(id=post_data['curso'])
        usuario=User.objects.get(id=post_data['user'])

        # QuerySet que verifica que no tenga otro grupo inscrito a la misma hora
        verify_enroll=Curso.objects.filter(alumno=request.user.id,
                                             hora_inicio=curso.hora_inicio,
                                             dia_inicio=curso.dia_inicio).exclude(id=curso.id)

        # variable que confirma la accion
        done=False

        # Si el usuario desea inscribirse a un curso
        if action == 'enroll':
            # QuerySet que verifica que no este inscrito ya
            if not Historial.objects.filter(curso=curso,
                                            alumno=usuario):
                if not verify_enroll:
                    h1=Historial(curso=curso,
                                   alumno=usuario)
                    h1.save()
                    done=True

        if action == 'disenroll':
            if Historial.objects.filter(curso=curso, alumno=usuario):
                Historial.objects.get(
                    curso=curso.id, alumno=usuario.id).delete()
                done=True

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())


class CursosView(View):

    template_name='cursos.html'

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):
        get_data=request.GET.copy()
        cursos=Curso.objects.filter(anno=year,
                                      semestre=currentSemester)
        if get_data:
            cursos=cursos.filter(nombre__icontains=get_data['search'])

        current_semester=currentSemester
        current_year=year
        return render(request, self.template_name, locals())

# vista de la pagina de inicio


class HomeView(View):

    template_name="home.html"

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):

        cursos_alumno=Curso.objects.filter(alumno=request.user.id,
                                             anno=year,
                                             semestre=currentSemester)
        cursos_instructor=Curso.objects.filter(instructor_id=request.user.id,
                                                 anno=year,
                                                 semestre=currentSemester)

        cursos_colaborador=Curso.objects.filter(colaborador_id=request.user.id,
                                                  anno=year,
                                                  semestre=currentSemester)
        return render(request, self.template_name, locals())
