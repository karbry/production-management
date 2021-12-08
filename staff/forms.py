from django import forms
from django.contrib.auth.models import User

from staff.models import Employee, ProductionSite, Specialization

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['specialization'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.get_name_display()

    user = forms.ModelChoiceField(queryset=User.objects.filter(employee=None), label="Użytkownik")
    specialization = forms.ModelMultipleChoiceField(queryset=Specialization.objects.all(), label="Specjalizacja", widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Employee
        fields = ['user', 'specialization', 'production_site']

