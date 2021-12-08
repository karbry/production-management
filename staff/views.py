from django.contrib.auth.models import User
from django_tables2 import SingleTableView
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from staff.forms import EmployeeForm
from staff.models import Employee

from staff.tables import EmployeeTable

def get_logged_employee(self):
    user_id = self.request.user.id
    employee = Employee.objects.get(user=user_id)

    return employee

class EmployeesListView(SingleTableView):
    template_name = 'staff.html'
    model = Employee
    table_class = EmployeeTable

    def dispatch(self, request, *args, **kwargs):
        if not get_logged_employee(self).is_supervisor:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_table_data(self):
        prod_site = get_logged_employee(self).production_site
        data = Employee.objects.filter(production_site=prod_site).filter(user__is_active=True)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supervisor'] = get_logged_employee(self).is_supervisor
        context['site'] = get_logged_employee(self).production_site.get_localization_display()

        return context


class EmployeesCreatorView(FormView):
    template_name = 'staff_creator.html'
    form_class = EmployeeForm

    def form_valid(self, form):
        if self.request.method == "POST":
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect('/staff')
        return super(EmployeesCreatorView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not get_logged_employee(self).is_supervisor:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supervisor'] = get_logged_employee(self).is_supervisor
        context['site'] = get_logged_employee(self).production_site.get_localization_display()

        return context

