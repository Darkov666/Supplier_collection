from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TransportacionForm, ContactForm, HomeForm
from .models import Dashs, Transportacion, Tours, Contact,Vehicle, VehicleType
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
import requests
import os
from django.urls import reverse
from django.conf import settings
from django import forms
#from django.core.mail import send_mail
#from django.contrib.auth.models import User, Group
#from django.contrib.auth import login, logout, authenticate
#from django.utils import timezone
#from django.contrib.auth.decorators import login_required 
#from .forms import SignUpForm

# Create your views here.


# Vista para la página de inicio
def home(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            # Guardar los datos en la sesión
            request.session['holder_name'] = form.cleaned_data['holder_name']
            request.session['num_adults'] = form.cleaned_data['num_adults']
            request.session['num_children'] = form.cleaned_data['num_children']
            request.session['start_date'] = str(form.cleaned_data['start_date'])
            request.session['email'] = form.cleaned_data['email']
            request.session['contact_phone'] = form.cleaned_data['contact_phone']
            return redirect('transportacion')  # Redirige a la página de transportación o donde necesites
    else:
        form = HomeForm()

    return render(request, 'home.html', {'form': form})

def transportacion(request):
    if request.method == 'POST':
        form = TransportacionForm(request.POST)
        if form.is_valid():
            try:          
                
                transportacion = form.save(commit=True)
                messages.success(request, 'Reservación creada exitosamente.')
                return redirect('detalle_transportacion', id=transportacion.id)
            except Exception as e:
                # Si ocurre un error inesperado al guardar
                messages.error(request, 'Ocurrió un error al crear la reservación.')
                # Aquí puedes registrar el error (opcional)
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = TransportacionForm()
    
    return render(request, 'transportacion.html', {'form': form})


def formulario_rev(request, id):
    transportacion = Transportacion.objects.get(id=id)
    return render(request, 'formulario_rev.html', {'transportacion': transportacion})

def calculate_vehicle_options(num_passengers):
    options = []
    
    if 1 <= num_passengers <= 6:
        # Buscar vehículos de lujo y estándar con capacidad suficiente
        luxury_vehicles = Vehicle.objects.filter(
            vehicle_type__name='Lujo',
            capacity__gte=num_passengers
        ).first()
        
        standard_vehicles = Vehicle.objects.filter(
            vehicle_type__name='Estándar',
            capacity__gte=num_passengers
        ).first()
        
        if luxury_vehicles:
            options.append({
                'type': 'luxury',
                'vehicles': [luxury_vehicles],
                'total_capacity': luxury_vehicles.capacity
            })
            
        if standard_vehicles:
            options.append({
                'type': 'standard',
                'vehicles': [standard_vehicles],
                'total_capacity': standard_vehicles.capacity
            })
            
    elif 7 <= num_passengers <= 9:
        # Calcular cuántos vehículos se necesitan
        luxury_vehicles = Vehicle.objects.filter(
            vehicle_type__name='Lujo',
            capacity__gte=5  # Asumiendo que cada vehículo de lujo tiene capacidad de 5
        )[:2]
        
        standard_vehicles = Vehicle.objects.filter(
            vehicle_type__name='Estándar',
            capacity__gte=5  # Asumiendo que cada vehículo estándar tiene capacidad de 5
        )[:2]
        
        if len(luxury_vehicles) == 2:
            options.append({
                'type': 'luxury',
                'vehicles': list(luxury_vehicles),
                'total_capacity': sum(v.capacity for v in luxury_vehicles)
            })
            
        if len(standard_vehicles) == 2:
            options.append({
                'type': 'standard',
                'vehicles': list(standard_vehicles),
                'total_capacity': sum(v.capacity for v in standard_vehicles)
            })
    
    return options

def transportacion_review(request, transportacion_id):
    transportacion = Transportacion.objects.get(id=transportacion_id)
    total_passengers = transportacion.num_adults + transportacion.num_children
    vehicle_options = calculate_vehicle_options(total_passengers)
    
    context = {
        'transportacion': transportacion,
        'vehicle_options': vehicle_options,
    }
    return render(request, 'formulario_rev.html', context)


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