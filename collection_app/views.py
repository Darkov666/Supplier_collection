from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TransportacionForm, ContactForm, HomeForm
from .models import Dashs, Transportacion, Tour, Contact,Vehicle, VehicleType, ServiceRequest
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
import requests
import json
import os
from django.urls import reverse
from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.utils.dateparse import parse_datetime, parse_date

 

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

            return redirect('home')  # Redirige a la página de transportación o donde necesites
    else:
        form = HomeForm()
        tours = Tour.objects.filter(is_active=True).order_by('name')

        return render(request, 'home.html', {'form': form, 'tours': tours})

def service_request_form(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        
        # Crea la solicitud de servicio
        service_request = ServiceRequest(**form_data)
        service_request.save()
        
        # Envía el correo electrónico
        subject = f'Nueva solicitud de servicio de {service_request.holder_name}'
        message = f'Se ha recibido una nueva solicitud de servicio:\n\n'
        message += f'Tipo de servicio: {service_request.get_service_type_display()}\n'
        message += f'Correo electrónico: {service_request.email}\n'
        message += f'Número de contacto: {service_request.contact_phone}\n'
        if service_request.service_type == 'TOUR':
            message += f'Tour: {service_request.tour_name}\n'
        message += f'Fecha y hora: {service_request.tour_datetime}\n'
        message += f'Notas adicionales: {service_request.additional_notes}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False
        )
        
        # Redirige al usuario a una página de éxito
        return redirect('home')
    else:
        tours = Tour.objects.filter(is_active=True).order_by('name')
    return render(request, 'contact.html', {'tours': tours})

def get_tours(request):
    tours = Tour.objects.filter(is_active=True).values('id', 'name', 'duration')
    return JsonResponse(list(tours), safe=False)

@require_http_methods(["POST"])
def create_service_request(request):
    try:
        print("Content Type:", request.content_type)
        print("Body:", request.body)

        # Determinar el tipo de contenido y obtener los datos
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        else:
            data = request.POST.dict()

        # Debug: imprimir los datos recibidos
        print("Datos recibidos:", data)

        try:
            # Obtener campos específicos del servicio
            service_specific_fields = get_service_specific_fields(data)  # Aquí pasamos data, no request
            
            # Debug: imprimir campos específicos
            print("Campos específicos:", service_specific_fields)

            # Conversiones básicas
            total_adults = int(data.get('total_adults', 0))
            total_children = int(data.get('total_children', 0))
            
            # Manejar las listas de edades
            adult_ages = data.get('adult_ages', [])
            children_ages = data.get('children_ages', [])
            
            # Si las edades vienen como strings, convertirlas a listas
            if isinstance(adult_ages, str):
                adult_ages = json.loads(adult_ages) if adult_ages else []
            if isinstance(children_ages, str):
                children_ages = json.loads(children_ages) if children_ages else []

            # Crear la solicitud de servicio
            service_request = ServiceRequest.objects.create(
                holder_name=data.get('holder_name'),
                email=data.get('email'),
                contact_phone=data.get('contact_phone'),
                total_adults=total_adults,
                total_children=total_children,
                adult_ages=adult_ages,
                children_ages=children_ages,
                service_type=data.get('service_type'),
                additional_notes=data.get('additional_notes', ''),
                **service_specific_fields
            )
            
            # Enviar email con SendGrid
            send_confirmation_email(service_request)
            
            return JsonResponse({'message': 'Solicitud creada exitosamente'}, status=201)
            
        except ValueError as e:
            print(f"Error de valor: {str(e)}")
            return JsonResponse({'message': f'Error en la conversión de datos: {str(e)}'}, status=400)
            
    except Exception as e:
        print(f"Error en create_service_request: {str(e)}")
        return JsonResponse({'message': str(e)}, status=400)

def get_service_specific_fields(data):
    """
    Procesa los campos específicos según el tipo de servicio.
    
    Args:
        data (dict): Diccionario con los datos del formulario
    """
    if not isinstance(data, dict):
        raise ValueError("Los datos deben ser un diccionario")

    service_type = data.get('service_type')
    fields = {}
    
    try:
        if service_type == 'TRANSPORT':
            fields = {
                'transport_type': data.get('transport_type'),
                'origin': data.get('origin'),
                'destination': data.get('destination'),
                'departure_datetime': parse_datetime(data.get('departure_datetime')),
                'return_datetime': parse_datetime(data.get('return_datetime'))
            }
        elif service_type == 'TOUR':
            fields = {
                'custom_tour_name': data.get('custom_tour_name'),
                'tour_datetime': parse_datetime(data.get('tour_datetime')),
                'requires_pickup': data.get('requires_pickup') == 'true'
            }
            
            # Manejar el tour_id solo si no es 'other'
            tour_id = data.get('tour')
            if tour_id and tour_id != 'other':
                try:
                    fields['tour_id'] = int(tour_id)
                except (ValueError, TypeError):
                    pass
                    
        elif service_type == 'LODGING':
            fields = {
                'hotel_name': data.get('hotel_name'),
                'room_count': int(data.get('room_count', 0)) if data.get('room_count') else None,
                'lodging_destination': data.get('lodging_destination'),
                'check_in_date': parse_date(data.get('check_in_date')),
                'check_out_date': parse_date(data.get('check_out_date'))
            }
        
        # Eliminar campos None
        return {k: v for k, v in fields.items() if v is not None}
        
    except Exception as e:
        print(f"Error en get_service_specific_fields: {str(e)}")
        raise ValueError(f"Error procesando campos específicos: {str(e)}")

def send_confirmation_email(service_request):
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=service_request.email,
            subject='Confirmación de solicitud de servicio',
            plain_text_content=generate_email_content(service_request)
        )
        sg.send(message)
    except Exception as e:
        print(f"Error enviando email: {e}")

def generate_email_content(service_request):
    content = f"""
    Estimado/a {service_request.holder_name},

    Hemos recibido su solicitud de servicio con los siguientes detalles:

    Tipo de servicio: {service_request.get_service_type_display()}
    Adultos: {service_request.total_adults}
    Menores: {service_request.total_children}
    """
    
    if service_request.service_type == 'TRANSPORT':
        content += f"""
        Tipo de transporte: {service_request.get_transport_type_display()}
        Origen: {service_request.origin}
        Destino: {service_request.destination}
        Fecha de salida: {service_request.departure_datetime}
        """
    # Agregar más detalles según el tipo de servicio
    
    content += "\nNos pondremos en contacto con usted pronto."
    
    return content

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