import django_tables2 as tables
from .models import Employee

class EmployeeTable(tables.Table):
    full_name = tables.Column(accessor='get_user_full_name', verbose_name='Imię i nazwisko', order_by=("user"))
    spec_type = tables.Column(accessor='get_specialization', verbose_name='Specjalizacja', order_by=("specialization"))
    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "full_name", "spec_type", "production_site")