from django.db import models
from django.contrib.auth.models import User, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Transportacion(models.Model):
    holder_name = models.CharField(max_length=100)
    num_people = models.IntegerField()
    round_trip = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_start = models.CharField(max_length=100)
    destination_start = models.CharField(max_length=100)
    pickup_end = models.CharField(max_length=100)
    destination_end = models.CharField(max_length=100)

    def __str__(self):
        return f"Reservation by {self.holder_name} for {self.num_people} people"
    
class Tours(models.Model):
    holder_name = models.CharField(max_length=100)
    num_people = models.IntegerField()
    round_trip = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_start = models.CharField(max_length=100)
    destination_start = models.CharField(max_length=100)
    pickup_end = models.CharField(max_length=100)
    destination_end = models.CharField(max_length=100)

    def __str__(self):
        return f"Reservation by {self.holder_name} for {self.num_people} people"
    
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