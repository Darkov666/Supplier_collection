from django.db import models
from django.contrib.auth.models import User, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import now, timedelta

# Create your models here.
class Transportacion(models.Model):
    holder_name = models.CharField(max_length=100)
    num_adults = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Numero de adultos", default=1)
    num_children = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Numero  de Menores", default=0, null=True)
    start_date = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    round_trip = models.BooleanField(null=True, blank=True, default=False)
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y hora de regreso")
    pickup_start = models.CharField(max_length=255)
    destination_start = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)  # Campo para el correo electrónico
    contact_phone = PhoneNumberField(blank=False, null=False, verbose_name="Teléfono de contacto")
    flight_number_arrival = models.CharField(max_length=20, null=True, blank=True)
    flight_number_departure = models.CharField(max_length=20, null=True, blank=True)
    airline_arrival = models.CharField(max_length=50, null=True, blank=True)
    airline_departure = models.CharField(max_length=50, null=True, blank=True)
    terminal_arrival = models.CharField(max_length=50, null=True, blank=True)
    terminal_departure = models.CharField(max_length=50, null=True, blank=True)
    
    def clean(self):
        # Validar que start_date no sea en el pasado
        date_start_valid = timezone.now() + timedelta(days=0, hours=8)
        if self.start_date and self.start_date <= date_start_valid:
            raise ValidationError({'start_date': 'La fecha de recervació debe ser al menos con un día de anticipacion a tu llegada'})
        
        # Validar que end_date sea después de start_date
        #date_end_valid = timezone.now() + timedelta(days=0, hours=16)
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError({'end_date': 'La fecha de regreso debe ser posterior a la fecha de inicio.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.holder_name} - {self.start_date} - {self.destination_start}'

   # def __str__(self):
    #    return f"Reservation by {self.holder_name} for {self.num_people} people"

class Tour(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True)  # ej: "4 horas", "2 días"
    default_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Meta:
        ordering = ['name']
    
class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('TRANSPORT', 'Transporte'),
        ('TOUR', 'Tour'),
        ('LODGING', 'Hospedaje'),
    ]
    TRANSPORT_TYPES = [
        ('ROUND', 'Redondo'),
        ('SINGLE', 'Sencillo'),
    ]

    # Campos base
    created_at = models.DateTimeField(auto_now_add=True)
    holder_name = models.CharField(max_length=200)
    total_adults = models.PositiveIntegerField()
    total_children = models.PositiveIntegerField()
    additional_notes = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    email = models.EmailField(max_length=254)  # Campo para el correo electrónico
    contact_phone = PhoneNumberField(blank=False, null=False, verbose_name="Teléfono de contacto")
    # Campos para edades
    adult_ages = models.JSONField(default=list)
    children_ages = models.JSONField(default=list)

    # Campos para transporte
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPES, null=True, blank=True)
    origin = models.CharField(max_length=200, null=True, blank=True)
    destination = models.CharField(max_length=200, null=True, blank=True)
    departure_datetime = models.DateTimeField(null=True, blank=True)
    return_datetime = models.DateTimeField(null=True, blank=True)

    # Campos para tour
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, blank=True)
    custom_tour_name = models.CharField(max_length=200, null=True, blank=True)
    tour_datetime = models.DateTimeField(null=True, blank=True)
    requires_pickup = models.BooleanField(null=True, blank=True)

    # Campos para hospedaje
    hotel_name = models.CharField(max_length=200, null=True, blank=True)
    room_count = models.PositiveIntegerField(null=True, blank=True)
    lodging_destination = models.CharField(max_length=200, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.holder_name} - {self.service_type} - {self.created_at}"
    
    def clean(self):
        # Validar que tour_datetim del tour no sea en el pasado
        date_start_valid = timezone.now() + timedelta(days=0, hours=8)
        if self.tour_datetime and self.tour_datetime <= date_start_valid:
            raise ValidationError({'tour_datetim': 'La fecha de recervació debe ser al menos con un día de anticipacion'})
        
        # Validar que check_in_date del tourhospedaje no sea en el pasado
        date_start_valid = timezone.now() + timedelta(days=0, hours=8)
        if self.check_in_date and self.check_in_date <= date_start_valid:
            raise ValidationError({'check_in_date': 'La fecha de recervació debe ser al menos con un día de anticipacion'})
        
        # Validar que check_out_date sea después de start_date
        #date_end_valid = timezone.now() + timedelta(days=0, hours=16)
        if self.check_out_date and self.check_in_date and self.check_out_date <= self.check_in_date:
            raise ValidationError({'check_out_date': 'La fecha de regreso debe ser posterior a la fecha de inicio.'})
        
         # Validar que departure_datetime del tourhospedaje no sea en el pasado
        date_start_valid = timezone.now() + timedelta(days=0, hours=8)
        if self.departure_datetime and self.departure_datetime <= date_start_valid:
            raise ValidationError({'departure_datetime': 'La fecha de recervació debe ser al menos con un día de anticipacion'})
        
        # Validar que check_out_date sea después de start_date
        #date_end_valid = timezone.now() + timedelta(days=0, hours=16)
        if self.return_datetime and self.departure_datetime and self.return_datetime <= self.departure_datetime:
            raise ValidationError({'return_datetime': 'La fecha de regreso debe ser posterior a la fecha de inicio.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.holder_name} - {self.start_date} - {self.destination_start}'

    @property
    def tour_name(self):
        """Retorna el nombre del tour, sea personalizado o predefinido"""
        return self.custom_tour_name if self.custom_tour_name else (self.tour.name if self.tour else None)

class VehicleType(models.Model):
    name = models.CharField(max_length=100)  # ej: "Estándar", "Lujo"
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/')
    
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # ej: "Suburban Lujo"
    capacity = models.IntegerField()  # capacidad máxima de pasajeros
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.vehicle_type.name})"    
    
class Dashs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + '- by ' + self.user.username
    
class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    phone_number = PhoneNumberField()
    newss_later = models.BooleanField(default=False)
       
    def __str__(self):
        return self.contact_name 