"""sistemaDocenteITCJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from registroCursos.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'), # pagina principal 
    path('course/', CursosView.as_view(), name='course'), # pagina donde se muestran los cursos
    path('course/detail/<int:id_curso>', DetailView.as_view(), name='detail'), # donde se confirma la inscripcion o se desinscribe del curso
    path('course/detail/<int:id_curso>/course_confirm_action', ConfirmActionCourseView.as_view(),name='course_confirm_action'), # pagina de confirmacion de inscripcion y desinscripcion del curso
    path('course/detail/<int:id_curso>/admin', AdminCourseView.as_view(), name='admin_course'), # Pagina donde el instructor subira la asistencia
    path('course/detail/<int:id_curso>/admin/<int:id_user>', EvaluateView.as_view(), name='evaluate'),
    path('course/detail/<int:id_curso>/admin/<int:id_user>/done', EvaluateDoneView.as_view(), name='evaluate_done'),
    path('course/detail/<int:id_curso>/poll/<int:id_user>', PollView.as_view(), name='poll'),
    path('course/detail/<int:id_curso>/poll/<int:id_user>/done', PollDoneView.as_view(), name='poll_done'),
    path('course/detail/<int:id_curso>/reports', ReportsView.as_view(),name='reports'),
     path('admin/', admin.site.urls), # link a sitio de administracion (solo administradores o superuser)
    path('accounts/', include('django.contrib.auth.urls')), # link para el inicio de sesion
    path('accounts/update_email/', UpdateEmailView.as_view(),name='update_email'), # link para el cambio de email
    path('accounts/update_username/', UpdateUsernameView.as_view(),name='update_username'), # link para el cambio de nombre de usuario
    path('accounts/user_profile/', UserProfileView.as_view(),name='user_profile') # link para ver los datos personales   
]

