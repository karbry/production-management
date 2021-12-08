from django.db import models
from django.urls import reverse

from staff.models import Employee, ProductionSite


class Product(models.Model):
    SIZES = [
        ("150x105", "150cm x 105cm"),
        ("250x175", "250cm x 175cm"),
        ("350x256", "350cm x 256cm"),
        ("450x315", "450cm x 315cm"),
        ("50x1050", "50cm x 1050cm"),
    ]
    TYPES = [("T", "Tapeta"), ("F", "Fototapeta")]
    PRODUCTION_STEPS = [
        ("nowe", "Nowe"),
        ("w trakcie druku", "W trakcie druku"),
        ("wydrukowane", "Wydrukowane"),
        ("w trakcie pakowania", "W trakcie pakowania"),
        ("zapakowane", "Zapakowane"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nazwa")
    size = models.CharField(choices=SIZES, max_length=7, verbose_name="Rozmiar")
    type = models.CharField(choices=TYPES, max_length=1, verbose_name="Typ")
    pattern_index = models.IntegerField(verbose_name="Numer wzoru")
    production_step = models.CharField(
        choices=PRODUCTION_STEPS, default=PRODUCTION_STEPS[0][0], max_length=20, verbose_name="Etap produkcji"
    )
    def __str__(self):
        return f"{self.name} {self.pattern_index} {self.size}"


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    def __str__(self):
        return f"{self.name}, {self.address} {self.zip_code[0:2]}-{self.zip_code[2:5]} {self.city}"


class Order(models.Model):
    ORDER_STATUSES = [
        ("nowe", "Nowe"),
        ("w trakcie realizacji", "W trakcie realizacji"),
        ("zrealizowane", "Zrealizowane"),
        ("wydane do wysyłki", "Wydane do wysyłki"),
    ]

    store_order_id = models.IntegerField(unique=True)
    products = models.ManyToManyField(Product)
    shipping_info = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Dane do wysyłki")
    order_time = models.DateTimeField(verbose_name="Data złożenia")
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name="Data realizacji")
    status = models.CharField(
        choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0], max_length=20, verbose_name="Status"
    )
    packer = models.ForeignKey(Employee, related_name = "packer", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Osoba pakująca")
    printer_operator = models.ForeignKey(Employee, related_name = "printer_operator", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Osoba drukująca")
    production_site = models.ForeignKey(ProductionSite, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Lokalizacja")

    def __str__(self):
        return (' '.join(map(str, self.products.all())))


    def get_number_of_products(self):
        return self.products.all().count


    def get_products(self):
        products = ''
        for item in self.products.all():
            products += f"{item.name} "
        return products
