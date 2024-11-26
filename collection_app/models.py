from django.db import models
from django.contrib.auth.models import User, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.utils.timezone import now, is_naive, make_aware
import pytz

def default_check_out_date():
    return now() + timedelta(days=1)
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
    # Datos generales
    created_at = models.DateTimeField(auto_now_add=True)
    holder_name = models.CharField(max_length=200)
    email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    total_adults = models.PositiveIntegerField()
    total_children = models.PositiveIntegerField(default=0)
    child_ages = models.JSONField(default=list, blank=True)  # Lista de edades de menores
    service_type = models.CharField(max_length=20, choices=[
        ('TRANSPORT', 'Transporte'),
        ('TOUR', 'Tour'),
        ('LODGING', 'Hospedaje'),
    ])
    
    # Datos de transporte
    transport_type = models.CharField(max_length=10, null=True, blank=True, choices=[
        ('ROUND', 'Redondo'),
        ('SINGLE', 'Sencillo'),
    ])
    origin = models.CharField(max_length=200, null=True, blank=True)
    destination = models.CharField(max_length=200, null=True, blank=True)
    departure_datetime = models.DateTimeField(null=True, blank=True, default=now)
    return_datetime = models.DateTimeField(null=True, blank=True)

    # Datos de tour
    tour = models.ForeignKey('Tour', null=True, blank=True, on_delete=models.SET_NULL)
    tour_datetime = models.DateTimeField(null=True, blank=True, default=now)
    custom_tour_name = models.CharField(max_length=200, null=True, blank=True)
    tour_datetime = models.DateTimeField(null=True, blank=True, default=now)
    requires_pickup = models.BooleanField(default=False)

    # Datos de hospedaje
    hotel_name = models.CharField(max_length=200, null=True, blank=True)
    room_count = models.PositiveIntegerField(null=True, blank=True)
    lodging_destination = models.CharField(max_length=200, null=True, blank=True)
    check_in_date = models.DateTimeField(null=True, blank=True, default=now)
    check_out_date = models.DateTimeField(null=True, blank=True, default=default_check_out_date)    
    
    # Notas adicionales
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.holder_name} - {self.service_type}"
    
    def clean(self):
        """
        Validaciones personalizadas para fechas según el tipo de servicio.
        """
        if self.total_adults < 1:
            raise ValidationError('Debe haber al menos un adulto.')

        if self.service_type == 'TRANSPORT' and not self.origin:
            raise ValidationError('El campo "Origen" es obligatorio para transporte.')

        # Obtener la fecha actual
        today = now()

        # Validación de transporte
        if self.service_type == 'TRANSPORT':
            if not self.departure_datetime:
                raise ValidationError('Debe ingresar una fecha de ida para el transporte.')

            # Fecha de ida debe estar al menos un día en el futuro
            if self.departure_datetime < today + timedelta(days=1):
                raise ValidationError('La fecha de ida debe ser al menos un día despues de la fecha actual.')

            # Si es transporte redondo, validar la fecha de regreso
            if self.return_datetime:
                if self.return_datetime <= self.departure_datetime:
                    raise ValidationError('La fecha de regreso debe ser posterior a la fecha de ida.')
                if self.return_datetime < self.departure_datetime + timedelta(hours=1):
                    raise ValidationError('La fecha de regreso debe ser al menos una hora después de la ida.')

        # Validación de hospedaje
        if self.service_type == 'LODGING':
            if not self.check_in_date:
                raise ValidationError('Debe ingresar la fecha de check-in.')
            if self.check_in_date < today + timedelta(days=1):
                raise ValidationError('La fecha de check-in debe ser al menos un día despues de la fecha actual.')

            if not self.check_out_date:
                raise ValidationError('Debe ingresar la fecha de check-out.')
            if self.check_out_date <= self.check_in_date:
                raise ValidationError('La fecha de check-out debe ser posterior a la fecha de check-in.')
            if self.check_out_date < self.check_in_date + timedelta(days=1):
                raise ValidationError('La fecha de check-out debe ser al menos un día después del check-in.')

        # Validación de tour
        if self.service_type == 'TOUR':
            if not self.tour_datetime:
                raise ValidationError('Debe ingresar una fecha para el tour.')
            if self.tour_datetime < today + timedelta(days=1):
                raise ValidationError('La fecha del tour debe ser al con un día de anticipación.')
            
        # Asegurarse de que las fechas sean aware
        if is_naive(self.departure_datetime):
            self.departure_datetime = make_aware(self.departure_datetime, timezone=pytz.UTC)

        if self.return_datetime:
            if is_naive(self.return_datetime):
                self.return_datetime = make_aware(self.return_datetime, timezone=pytz.UTC)

            # Validación adicional: la fecha de regreso debe ser posterior a la de ida
            if self.return_datetime <= self.departure_datetime:
                raise ValidationError("La fecha de regreso debe ser posterior a la fecha de ida.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:  # Solo modifica created_at al crear el objeto
            self.created_at = localtime()
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