from django.utils import timezone
from django.views.generic import TemplateView
from registroCursos.models import Alumno,Instructor,Curso

date_filter = timezone.now().strftime('%d/%m/%Y')
current_semester = "ago_dic" if int(date_filter[-7:-5]) > 7 else "ene_jun"


class CursosView(TemplateView):

    template_name = 'cursos.html'

    def get_context_data(self,*args, **kwargs):
        context = super(CursosView, self).get_context_data(**kwargs)
        context['cursos'] = Curso.objects.filter(anno=int(date_filter[-4:]),
                                                        semestre=current_semester)
        context['current_semester'] = current_semester
        context['current_year'] = date_filter[-4:]
        return context


class HomeView(TemplateView): 
      
    template_name = "home.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        current_user = self.request.user
        current_user_id = current_user.id

        context['now'] = timezone.now()
      
        context['cursos_alumno'] = Curso.objects.filter(alumnos=current_user_id, 
                                                        anno=int(date_filter[-4:]),
                                                        semestre=current_semester)
        context['cursos_instructor'] = Curso.objects.filter(instructor_id=current_user_id,
                                                         anno=int(date_filter[-4:]),
                                                            semestre=current_semester)

        return context
    
        
        






