from django.utils import timezone
from django.views.generic import View
from registroCursos.models import Curso, Historial, UserProfile
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *


date_filter = timezone.now().strftime('%d/%m/%Y')
currentSemester = "ago_dic" if int(date_filter[-7:-5]) > 7 else "ene_jun"


class UserProfileView(View):
    template_name = 'user/user_profile.html'

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()

        user_profile = UserProfile.objects.get(id=request.user.id)

        user = User.objects.get(id=request.user.id)
        print(request.user.id)
        if User.objects.filter(username=post_data['username']) and not User.objects.filter(id=request.user.id, username=post_data['username']):
            error = ['username']
        else:
            if User.objects.filter(email=post_data['email']) and not User.objects.filter(id=request.user.id, email=post_data['email']):
                error = error.append('email')
            else:
                user.first_name = post_data['first_name']
                user.last_name = post_data['last_name']
                user.username = post_data['username']
                user.email = post_data['email']
                user_profile.telefono_particular = post_data['telefono_particular']
                user_profile.departamento = post_data['departamento']
                user_profile.RFC = post_data['RFC']
                user_profile.CURP = post_data['CURP']
                user.save()
                user_profile.save()
        return render(request, 'user/update_user_profile_done.html', locals())

    def get(self, request, *args, **kwargs):

        profile = UserProfile.objects.get(id=request.user.id)

        form_profile = UpdateUserProfileForm()
        form_user = UpdateUserForm()

        return render(request, self.template_name, locals())


class UpdateUsernameView(View):
    template_name = 'user/update_username.html'

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        user = User.objects.get(id=request.user.id)

        if User.objects.filter(username=post_data['username']):
            action = False
        else:
            user.username = post_data['username']
            user.save()
            action = True
        return render(request, 'user/update_username_done.html', locals())

    def get(self, request, *args, **kwargs):
        form = UpdateUserForm()
        return render(request, self.template_name, locals())


class UpdateEmailView(View):
    template_name = 'user/update_email.html'

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        user = User.objects.get(id=request.user.id)

        if User.objects.filter(email=post_data['email']):
            action = False
        else:
            user.email = post_data['email']
            user.save()
            action = True
        return render(request, 'user/update_email_done.html', locals())

    def get(self, request, *args, **kwargs):
        form = UpdateUserForm()
        return render(request, self.template_name, locals())


class DetailView(View):
    template_name = "detail.html"

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):

        id = self.kwargs.get('id_curso')
        curso = Curso.objects.get(id=id)
        date = date_filter

        onCourseAsInstructor = True if Curso.objects.filter(
            id=id, instructor=request.user.id) else False

        onCourseAsAlumno = True if Curso.objects.filter(
            id=id, alumno=request.user.id) else False

        onCourseAsColaborador = True if Curso.objects.filter(
            id=id, colaborador=request.user.id) else False

        return render(request, self.template_name, locals())


class ConfirmActionCourseView(View):
    template_name = 'user/course_confirm_action.html'

    def post(self, request, *args, **kwargs):

        post_data = request.POST.copy()
        action = post_data['action']
        curso = Curso.objects.get(id=post_data['curso'])
        usuario = User.objects.get(id=post_data['user'])

         # QuerySet que verifica que no tenga otro grupo inscrito a la misma hora
        verify_enroll = Curso.objects.filter(alumno=request.user.id,
                                            hora_inicio=curso.hora_inicio,
                                            dia_inicio=curso.dia_inicio).exclude(id=curso.id)
                                            
        # variable que confirma la accion
        done = False

            # Si el usuario desea inscribirse a un curso
        if action == 'enroll':
            # QuerySet que verifica que no este inscrito ya 
            if not Historial.objects.filter(curso=curso,
             alumno=usuario):
                if not verify_enroll: 
                    h1 = Historial(curso=curso,
                               alumno=usuario)
                    h1.save()
                    done = True

        if action == 'disenroll':
            if Historial.objects.filter(curso=curso, alumno=usuario):
                Historial.objects.get(curso=curso.id, alumno=usuario.id).delete()
                done = True

        return render(request, self.template_name, locals())


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())



class CursosView(View):

    template_name = 'cursos.html'

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):
        get_data = request.GET.copy()
        cursos = Curso.objects.filter(anno=int(date_filter[-4:]),
                                      semestre=currentSemester)
        if get_data:
            cursos = cursos.filter(nombre__icontains=get_data['search'])     

        current_semester = currentSemester
        current_year = date_filter[-4:]
        return render(request, self.template_name, locals())

# vista de la pagina de inicio
class HomeView(View):
    
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def get(self, request, *args, **kwargs):

        cursos_alumno = Curso.objects.filter(alumno=request.user.id,
                                             anno=int(date_filter[-4:]),
                                             semestre=currentSemester)
        cursos_instructor = Curso.objects.filter(instructor_id=request.user.id,
                                                 anno=int(date_filter[-4:]),
                                                 semestre=currentSemester)

        cursos_colaborador = Curso.objects.filter(colaborador_id=request.user.id,
                                                  anno=int(date_filter[-4:]),
                                                  semestre=currentSemester)
        return render(request, self.template_name, locals())
