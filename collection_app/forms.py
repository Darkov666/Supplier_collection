from django import forms 
from .models import Dashs, Transportacion, Tours, Contact
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
                  'pickup_end', 'destination_end']
        widgets = {
            'holder_name': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Coloca tu nombre'
            }),
            'num_people': forms.NumberInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Número de personas'
            }),
            'round_trip': forms.CheckboxInput(attrs={
                'class': 'form-checkbox rounded-lg text-black shadow-lg bg-newlimel',
            }),
            'start_date': forms.TextInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
            }),
            'end_date': forms.TextInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
            }),
            'pickup_start': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Lugar de inicio'
            }),
            'destination_start': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Destino inicial'
            }),
            'pickup_end': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Lugar de finalización'
            }),
            'destination_end': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Destino final'
            }),
        }

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
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control flex rounded-lg text-black shadow-lg bg-newlimel',
                'placeholder': 'Phone'
            }),
        }

        
class TourForm(forms.ModelForm):
    class Meta:
        model = Tours
        fields = ['holder_name', 'num_people', 'round_trip', 'start_date', 'end_date', 'pickup_start', 'destination_start', 
            'pickup_end', 'destination_end']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
        
"""class ContactForm(forms.Form):
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