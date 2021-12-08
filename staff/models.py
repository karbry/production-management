from django.db import models
from django.conf import settings


class Specialization(models.Model):
    SPECIALIZATIONS = [("D", "Operator drukarki"), ("P", "Pakowacz")]
    name = models.CharField(choices=SPECIALIZATIONS, max_length=1)
    def __str__(self):
        return self.name 


class ProductionSite(models.Model):
    LOCALIZATIONS = [("WRO", "Wrocław"), ("KRK", "Kraków")]
    localization = models.CharField(choices=LOCALIZATIONS, max_length=3)
    def __str__(self):
        return self.localization


class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
    specialization = models.ManyToManyField(Specialization, verbose_name="Specjalizacja")
    production_site = models.ForeignKey(ProductionSite, on_delete=models.CASCADE, verbose_name="Lokalizacja")
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def get_user_full_name(self):
        return self.user.get_full_name
    def get_user_active_state(self):
        return self.user.is_active
    def get_specialization(self):
        specializations = ''
        for item in self.specialization.all():
            specializations += f"- {item.get_name_display()} "
        return specializations
