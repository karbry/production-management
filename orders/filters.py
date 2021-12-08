import django_filters
from django import forms
from staff.models import Employee, ProductionSite
from .models import Order


class OrderForLocalizationFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(label="Numer zamówienia", widget=forms.TextInput(attrs={"class": "form-control mx-2 mb-2"}))
    order_time = django_filters.DateTimeFromToRangeFilter(
        label = "Data złożenia od - do",
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control mx-2 mb-2", "placeholder": "YYYY-MM-DD"}
        )
    )
    status = django_filters.ChoiceFilter(
        choices=Order.ORDER_STATUSES,
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )
    packer = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.filter(specialization__name="P"),
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )
    printer_operator = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.filter(specialization__name="D"),
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )

    class Meta:
        model = Order
        fields = ["id", "order_time", "status", "packer", "printer_operator"]


class OrderAllFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(label="Numer zamówienia", widget=forms.TextInput(attrs={"class": "form-control mx-2 mb-2"}))
    order_time = django_filters.DateTimeFromToRangeFilter(
        label="Data złożenia od - do",
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control mx-2 mb-2", "placeholder": "YYYY-MM-DD"}
        )
    )
    complete_time = django_filters.DateTimeFromToRangeFilter(
        label="Data realizacji od - do",
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control mx-2 mb-2", "placeholder": "YYYY-MM-DD"}
        )
    )
    status = django_filters.ChoiceFilter(
        choices=Order.ORDER_STATUSES,
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )
    packer = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.filter(specialization__name="P"),
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )
    printer_operator = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.filter(specialization__name="D"),
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )
    production_site = django_filters.ModelChoiceFilter(
        queryset=ProductionSite.objects.all(),
        widget=forms.Select(attrs={"class": "form-control mx-2 mb-2"}),
    )

    class Meta:
        model = Order
        fields = ["id", "order_time", "complete_time", "status", "packer", "printer_operator", "production_site"]
