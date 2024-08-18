from django.shortcuts import render, redirect, get_object_or_404
#from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import DashForm, TransportacionForm, TourForm, ContactForm
from .models import Dashs, Transportacion, Tours, Contact
from django.http import HttpResponseRedirect
from django.db import IntegrityError
#from django.core.mail import send_mail
#from django.conf import settings
#from django.contrib.auth.models import User, Group
#from django.contrib.auth import login, logout, authenticate
#from django.utils import timezone
#from django.contrib.auth.decorators import login_required 
#from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def tours(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos
            return redirect('exito_transportacion.html')  # Redirige a una página de éxito (define la URL en urls.py)
    else:
        form = TourForm()
    return render(request, 'tours_grupos.html')

def Transportacion(request):
    if request.method == 'POST':
        form = TransportacionForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos
            return redirect('exito_transportacion.html')  # Redirige a una página de éxito (define la URL en urls.py)
    else:
        form = TransportacionForm()
    return render(request, 'transportacion.html', {'form': form})

def contacto(request):
    if request.method == 'GET':
        return render(request, 'contacto.html', {
            'contact_form': ContactForm()
        })
    else:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                # Procesa los datos del formulario
                name = form.cleaned_data['contact_name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                newss = form.cleaned_data['newss_later']
                phone = form.cleaned_data['phone_number']
     # Se requiere validacion de numero telefonico al menos el estandar basico de 10 digitos y colocar api de lada por pais.
     # Requiere validacion del dominio de correo electronico           
                # Guardar la información en la base de datos
                form.save()
                
                # Redirige o muestra un mensaje de éxito
                return redirect('home')
        else:
            form = ContactForm()

        return render(request, 'contacto.html', {'form': form})
        
"""    
def catamaran(request):
    return render(request, 'catamaran.html')

def hospedaje(request):
    return render(request, 'hospedaje.html')

def nocturna(request):
    return render(request, 'nocturna.html')

def parques(request):
    return render(request, 'parques.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def privacidad(request):
    return render(request, 'aviso_privacidad.html')

def contacto(request):
    return render(request, 'contacto.html')

def legal(request):
    return render(request, 'legal.html')

def politicas_cookies(request):
    return render(request, 'politicas_cookies.html')

"""