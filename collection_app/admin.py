from django.contrib import admin
from .models import Dashs, Transportacion, Contact, VehicleType, Vehicle

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
    
    
# Register your models here.
admin.site.register(Dashs, DashAdmin)
admin.site.register(Transportacion)
admin.site.register(Contact)
