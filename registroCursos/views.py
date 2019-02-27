from django.utils import timezone
from django.views.generic import View
from registroCursos.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *
from datetime import date, timedelta, datetime
from .utils import *
from .choices import *

day, month, year = timezone.now().strftime('%d/%m/%Y').split("/")
currentSemester = "ago_dic" if int(month) >= 7 else "ene_jun"

 
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
        fill_poll(user, user_profile, curso)


        return render(request, self.template_name, locals())


class StatsView(View):
    template_name = 'stats.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
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
