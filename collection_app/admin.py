from django.contrib import admin
from .models import Dashs, Transportacion, Contact

class DashAdmin(admin.ModelAdmin):
    readonly_fields = ("creation", )
    
# Register your models here.
admin.site.register(Dashs, DashAdmin)
admin.site.register(Transportacion)
admin.site.register(Contact)