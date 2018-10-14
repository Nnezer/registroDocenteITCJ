from django.utils import timezone
from django.views.generic import TemplateView,View
from registroCursos.models import Curso
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *
from django.views.generic.edit import FormView


date_filter = timezone.now().strftime('%d/%m/%Y')
currentSemester = "ago_dic" if int(date_filter[-7:-5]) > 7 else "ene_jun"


class DetailView(View):
    template_name = "detail.html"
    
    def post(self,request,*args,**kwargs):   
        return render(request,self.template_name,locals())

    def get(self,request,*args,**kwargs):
        
        current_user = request.user
        current_user_id = current_user.id
        id = self.kwargs.get('id_curso')
        curso= Curso.objects.get(id=id)
        date= date_filter
        onCourseAsInstructor= True if Curso.objects.filter(id=id,instructor=current_user_id) else False
        onCourseAsAlumno= True if Curso.objects.filter(id=id,alumno=current_user_id) else False
        return render(request,self.template_name,locals())

class DisEnrollCourseView(View):
    template_name = 'user/disenroll.html'

    def post(self,request,*args,**kwargs):   

        post_data = request.POST.copy()
        curso = Curso.objects.get(id=post_data['id_curso'])
        usuario = User.objects.get(id=post_data['id_user'])
        curso.alumno.remove(usuario)

        return render(request,self.template_name,locals())

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,locals())


class PersonalView(View):
    template_name="user/personal.html"
   
    def post(self,request,*args,**kwargs):   
        
        return render(request,self.template_name,locals())
    
    def get(self,request,*args,**kwargs):
        formUser= UpdateUserForm()
        formProfile = UpdateUserProfileForm()
        return render(request,self.template_name,locals())

class CursosView(View):

    template_name = 'cursos.html'

    def post(self,request,*args,**kwargs):   
        
        return render(request,self.template_name,locals())
        

    def get(self,request,*args,**kwargs):
        cursos = Curso.objects.filter(anno=int(date_filter[-4:]),
                                                        semestre=currentSemester)
        current_semester= currentSemester
        current_year= date_filter[-4:]
        return render(request,self.template_name,locals())

class EnrollCourseView(View):

    template_name = 'user/enroll.html'     
    
    def post(self,request,*args,**kwargs):   
        post_data = request.POST.copy()
        curso = Curso.objects.get(id=post_data['curso'])
        usuario = User.objects.get(id=post_data['user'])
        curso.alumno.add(usuario)
        return render(request,self.template_name,locals())
        

    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name,locals())


class HomeView(View): 
      
    template_name = "home.html"

    def post(self,request,*args,**kwargs):   
        return render(request,self.template_name,locals())


    def get(self, request, *args, **kwargs):

        current_user = request.user
        current_user_id = current_user.id

        now= timezone.now()
      
        cursos_alumno= Curso.objects.filter(alumno=current_user_id, 
                                                        anno=int(date_filter[-4:]),
                                                        semestre=currentSemester)
        cursos_instructor= Curso.objects.filter(instructor_id=current_user_id,
                                                         anno=int(date_filter[-4:]),
                                                            semestre=currentSemester)

        return render(request,self.template_name,locals())
    
        
        






