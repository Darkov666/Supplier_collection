from django.contrib import admin
from .models import Dashs, Transportacion, Contact, VehicleType, Vehicle, Tour, ServiceRequest
class DashAdmin(admin.ModelAdmin):
    readonly_fields = ("creation", )

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price')
    search_fields = ('name',)

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

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('holder_name', 'service_type', 'tour_name', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('holder_name', 'custom_tour_name', 'tour__name')
    date_hierarchy = 'created_at'

# Register your models here.
admin.site.register(Dashs, DashAdmin)
admin.site.register(Transportacion)
admin.site.register(Contact)
