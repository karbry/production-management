from django.contrib import admin
from .models import Employee, ProductionSite, Specialization

admin.site.register(Employee)
admin.site.register(ProductionSite)
admin.site.register(Specialization)
