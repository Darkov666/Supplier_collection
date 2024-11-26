from django import forms 
from .models import Dashs, Transportacion, Contact
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.timezone import now, timedelta
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class HomeForm(forms.Form):
    holder_name = forms.CharField(max_length=100, label='Nombre del titular')
    num_adults = forms.IntegerField(label='Número de adultos', min_value=1)
    num_children = forms.IntegerField(label='Número de niños', min_value=0)
    start_date = forms.DateField(widget=forms.SelectDateWidget(), label='Fecha de inicio')
    email = forms.EmailField(label='Correo electrónico')
    contact_phone = forms.CharField(max_length=12, label='Teléfono de contacto')

class DashForm(forms.ModelForm):
    class Meta:
        model = Dashs
        fields = ['title', 'description', 'important']
        widgets= {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coloca un titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Coloca una descripcion'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-imput m-auto'}),
        }

class TransportacionForm(forms.ModelForm):
    class Meta:
        model = Transportacion
        fields = ['holder_name', 'num_adults', 'num_children', 'start_date', 'pickup_start', 'airline_arrival','flight_number_arrival', 
                  'terminal_arrival', 'round_trip',  
                  'end_date', 'airline_departure', 'flight_number_departure', 'terminal_departure', 'destination_start', 
                   'email', 'contact_phone']    
    
        widgets = {
            'holder_name': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Coloca tu nombre'
            }),
            'num_adults': forms.NumberInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': '1'
            }),
            'num_children': forms.NumberInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': '0'
            }),
            'start_date': forms.TextInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
            }),
            'flight_number_arrival': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Vuelo de llegada',
                'id': 'flight_number_arrival',  
            }),
            'airline_arrival' : forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Aerolinea de llegada',
                'id': 'airline_arrival',  
            }), 
            'terminal_arrival' : forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Terminal de llegada',
                'id': 'terminal_arrival',  
            }), 
            'flight_number_departure': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Vuelo de llegada',
                'id': 'flight_number_departure',  # ID para autocompletar
            }),
            'airline_departure' : forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Aerolinea de salida',
                'id': 'airline_departure',  
            }),
            'terminal_departure' : forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Terminal de salida',
                'id': 'terminal_departure',  
            }), 
            'round_trip': forms.CheckboxInput(attrs={
                'class': 'form-checkbox rounded-lg mt-4 mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
            }),
            'end_date': forms.TextInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
            }),
            'pickup_start': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Aeroúerto Internacional de Cancún',
                'value': 'Aeroúerto Internacional de Cancún',
                'id': 'pickup_start',
                'readonly': True,
            }),
            'destination_start': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                'placeholder': 'Destino',
                'id': 'destination_start',  # ID para autocompletar
            }),
            'email': forms.TextInput(attrs={
                    'class': 'form-control flex rounded-lg mb-6 mt-2 input input-bordered shadow-lg bg-newlimel',
                    'placeholder': 'example@domain.com'
            }),
            'contact_phone': forms.TextInput(attrs={
                    'class': 'form-control flex rounded-lg mb-6 mt-2 text-1xl input input-bordered shadow-lg bg-newlimel',
                    'placeholder': ' + Lada + Phone',
                    
            }),                     
}        

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establece el valor por defecto para pickup_start
        self.fields['pickup_start'].initial = "Aeropuerto Internacional de Cancún, Carretera a Aeropuerto Cancún, Cancún, Q.R., México"
        self.fields['pickup_start'].widget.attrs['placeholder'] = "Aeropuerto Internacional de Cancún"

   
def clean_pickup_start(self):
    pickup_start = self.cleaned_data.get('pickup_start')
    if pickup_start != "Aeropuerto Internacional de Cancún, Carretera a Aeropuerto Cancún, Cancún, Q.R., México":
        raise forms.ValidationError("El punto de recogida debe ser el Aeropuerto Internacional de Cancún.")
    return pickup_start
 
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name', 'email', 'message']
        widgets = {
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Contact Name'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'E-mail'
            }),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Coloca tus comentarios'}),
            'newss_later': forms.CheckboxInput(attrs={
                'class': 'form-checkbox rounded-lg text-black shadow-lg bg-newlimel',
             }),
            'lada': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Lada'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Phone number'
            }),
        }
        
"""class TourForm(forms.ModelForm):
    class Meta:
        model = Tours
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
        
class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full'}))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}))
    #phone = forms.IntegerField(label='Numero de telefonico', Widjet=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))


class HospedajeForm(forms.ModelForm):
    class Meta:
        model = Hospedaje
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
        

class NocturnaForm(forms.ModelForm):
    class Meta:
        model = Nocturna
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
               
class ParquesForm(forms.ModelForm):
    class Meta:
        model = Parques
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
        

class CatamaranForm(forms.ModelForm):
    class Meta:
        model = Catamaran
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }"""