from django.contrib import admin
from .models import Dashs, Transportacion, Contact, VehicleType, Vehicle, Tour, ServiceRequest
class DashAdmin(admin.ModelAdmin):
    readonly_fields = ("creation", )

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price')
    search_fields = ('name',)

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['holder_name', 'service_type', 'created_at']  # Incluye 'created_at'
    list_filter = ['service_type', 'created_at']  # Agrega 'created_at' si es un campo válido
    date_hierarchy = 'created_at'  # Configura jerarquía de fechas con 'created_at'
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'capacity', 'is_available')
    list_filter = ('vehicle_type', 'is_available')
    search_fields = ('name',)    
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'default_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

# Register your models here.
admin.site.register(Dashs, DashAdmin)
admin.site.register(Transportacion)
admin.site.register(Contact)
admin.site.register(ServiceRequest, ServiceRequestAdmin)




