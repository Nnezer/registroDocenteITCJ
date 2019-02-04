from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 
import io
from reportlab.pdfbase import pdfmetrics
 
def fill_poll(User, User_Profile, Course):
  packet = io.BytesIO()
  can = canvas.Canvas(packet, pagesize=letter) 
  
  can.setFont('Helvetica', 11)#Fuente default con menor tamaño

  day, month, year = Course.dia_inicio.strftime('%d/%m/%Y').split("/")

#Fecha
  can.drawString(493, 649, day)#Día
  can.drawString(534, 649, month)#Mes
  can.drawString(565, 649, year)#Año
#1. Datos Personales
  apellidos = User.last_name.split()

  can.drawString(127, 605, apellidos[0])#Apellido Paterno
  can.drawCentredString(283, 605, apellidos[1])#Apellido Materno
  can.drawCentredString(445, 605, User.first_name)#Nombre(s)
  can.drawString(103, 565,User_Profile.RFC)#RFC
  can.drawString(298, 565,User_Profile.CURP)#Telefono
  can.drawString(454, 565, User.email)#email 

#2. Estudios

#  if grade == "Primaria":
#    can.drawString(120, 510, "X")#Primaria
#  elif grade == "Carrera Tecnica":
#    can.drawString(294, 510, "X")#Carrera Tecnica
  if User_Profile.grado == 'lic':
    can.drawString(410, 510, "X")#Licenciatura
  elif User_Profile.grado == "doc":
    can.drawString(526, 510, "X")#Doctorado
#  elif grade == "Secundaria":
#    can.drawString(120, 499, "X")#Secundaria
#  elif grade == "Bachillerato":
#    can.drawString(294, 499, "X")#Bachillerato
  elif User_Profile.grado == 'mtr':
    can.drawString(410, 499, "X")#Maestria 

  can.drawString(200, 475, User_Profile.carrera)#Nombre de la carrera cursada


#3. Datos Laborales
  if User_Profile.puesto == 'jefe':
    can.drawString(121, 373, "X")#Directivos
  elif User_Profile.puesto == 'docente':
    can.drawString(121, 329, "X")#Apoyo a la Educación

  can.drawString(241, 417, "ITCJ")#Unidad Responsable

  can.drawString(190, 401, User_Profile.get_area_display())#Area
  
  can.drawString(220, 385, User_Profile.get_puesto_display())#Puesto Actual

#Nombramientos
  if User_Profile.nombramiento == 'TC':
    can.drawString(263, 362, "X")#TC
  if User_Profile.nombramiento == '3/4':
    can.drawString(341, 362, "X")#Tres Cuartos
  if User_Profile.nombramiento == '1/2':
    can.drawString(422, 362, "X")#Medio Tiempo
  if User_Profile.nombramiento == 'PA':
    can.drawString(493, 362, "X")#Asignatura
  if User_Profile.nombramiento == 'HN':
    can.drawString(574, 362, "X")#Por Honorarios

  can.drawString(265, 346, User_Profile.jefe_inmediato)#Nombre del jefe inmediato
  can.drawString(225, 330, "Av. Tecnológico No. 1340 C.P. 32500 Ciudad Juárez, Chih. México")#Domicilio Oficial
  can.drawString(225, 314, "01 656 688 2500")#Telefono Oficial
  can.drawString(465, 314, User_Profile.extension)#Ext.
  can.drawString(185, 298, "De {0} a {1}".format(User_Profile.horario_inicio, User_Profile.horario_final))#Horario

#4. Datos del Evento
  can.drawString(138, 244, Course.nombre)#Nombre del Evento
  can.drawString(142, 229, str(Course.instructor.get_full_name()))#Nombre del Instructor
# can.drawString(118, 212, Course.colaborador)#Nombre del Colaborador
  can.drawCentredString(189, 197, str(Course.dia_inicio))#Dia de Inicio
  can.drawCentredString(255, 197, str(Course.dia_final))#Dia de terminación
  
  #Fecha de Realización
  can.drawCentredString(413, 197, str(Course.hora_inicio))#Hora inicial
  can.drawCentredString(486, 197, str(Course.hora_final))#Hora final

 
  can.save()
#move to the beginning of the StringIO buffer
  packet.seek(0)
  new_pdf = PdfFileReader(packet)
# read your existing PDF
  existing_pdf = PdfFileReader(open("template_inscription.pdf", "rb"))
  output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
  page = existing_pdf.getPage(0)
  page.mergePage(new_pdf.getPage(0))
  output.addPage(page)
# finally, write "output" to a real file
  outputStream = open("Cedula de Inscripcion - "+User.first_name+ " "+ User.last_name +".pdf", "wb")
  output.write(outputStream)
  outputStream.close()
 
