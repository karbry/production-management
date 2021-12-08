
from datetime import datetime
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.http import HttpResponseRedirect
from orders.filters import OrderAllFilter, OrderForLocalizationFilter
from orders.serializers import CustomerSerializer, OrderSerializer, ProductSerializer
from orders.tables import OrderTable, OrderTableAll, ProductsTable
from staff.models import Employee
from .models import Customer, Order, Product
from rest_framework import viewsets


def get_logged_employee(self):
    user_id = self.request.user.id
    employee = Employee.objects.get(user=user_id)

    return employee


class OrdersForLocalizationListView(SingleTableMixin, FilterView):
    template_name = "orders.html"
    model = Order
    table_class = OrderTable
    filterset_class = OrderForLocalizationFilter

    def get_table_data(self):
        prod_site = get_logged_employee(self).production_site
        data = Order.objects.filter(production_site=prod_site)
        if self.request.GET:
            options = {}
            for key in ('id', 'status', 'packer', 'printer_operator'):
                value = self.request.GET.get(key)
                if value:
                    options[key] = value
            if self.request.GET.get('order_time_min') or self.request.GET.get('order_time_max'):
                options['order_time__range'] = ['', '']
                options['order_time__range'][0] = '2021-01-01' if not self.request.GET.get('order_time_min') else self.request.GET.get('order_time_min')
                options['order_time__range'][1] = datetime.now() if not self.request.GET.get('order_time_max') else self.request.GET.get('order_time_max')

            data = Order.objects.filter(**options, production_site=prod_site)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site"] = get_logged_employee(
            self
        ).production_site.get_localization_display()
        context["supervisor"] = get_logged_employee(self).is_supervisor

        return context


class AllOrdersListView(SingleTableMixin, FilterView):
    template_name = "orders.html"
    model = Order
    table_class = OrderTableAll
    filterset_class = OrderAllFilter

    def dispatch(self, request, *args, **kwargs):
        if not get_logged_employee(self).is_supervisor:
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_table_data(self):
        data = Order.objects.all()
        if self.request.GET:
            options = {}
            for key in ('id', 'status', 'production_site', 'packer', 'printer_operator'):
                value = self.request.GET.get(key)
                if value:
                    options[key] = value
            if self.request.GET.get('order_time_min') or self.request.GET.get('order_time_max'):
                options['order_time__range'] = ['', '']
                options['order_time__range'][0] = '2021-01-01' if not self.request.GET.get('order_time_min') else self.request.GET.get('order_time_min')
                options['order_time__range'][1] = datetime.now() if not self.request.GET.get('order_time_max') else self.request.GET.get('order_time_max')
            if self.request.GET.get('complete_time_min') or self.request.GET.get('complete_time_max'):
                options['complete_time__range'] = ['', '']
                options['complete_time__range'][0] = '2021-01-01' if not self.request.GET.get('complete_time_min') else self.request.GET.get('complete_time_min')
                options['complete_time__range'][1] = datetime.now() if not self.request.GET.get('complete_time_max') else self.request.GET.get('complete_time_max')

            data = Order.objects.filter(**options)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_orders_view"] = True
        context["supervisor"] = get_logged_employee(self).is_supervisor
        context["supervisor_site"] = get_logged_employee(self).production_site.get_localization_display()

        return context

    def post(self, request, *args, **kwargs):
        supervisor_prod_site = get_logged_employee(self).production_site
        if request.POST.get("change_prod_site"):
            for order_id in request.POST.getlist("checkbox_column"):
                order = Order.objects.get(pk=order_id)
                if not order.production_site:
                    order.production_site = supervisor_prod_site
                    order.save()
            return HttpResponseRedirect(f"all")
        if request.POST.get("delete_prod_site"):
            for order_id in request.POST.getlist("checkbox_column"):
                order = Order.objects.get(pk=order_id)
                if order.production_site == supervisor_prod_site:
                    order.production_site = None
                    order.save()
            return HttpResponseRedirect(f"all")
        return render(request, self.template_name)


class OrderDetailView(SingleTableView):
    template_name = "order_detail.html"
    model = Product
    table_class = ProductsTable

    def get_table_data(self):
        data = Order.objects.get(pk=self.kwargs["pk"]).products.all()

        return data

    def get_context_data(self, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"])
        products = order.products.all()
        employee = get_logged_employee(self)
        context = super().get_context_data(**kwargs)
        context["is_employee_packer"] = True if "Pakowacz" in employee.get_specialization() else False
        context["is_employee_printer_op"] = True if "Operator drukarki" in employee.get_specialization() else False
        context["supervisor"] = employee.is_supervisor
        context["order_id"] = order.id
        context["order_time"] = order.order_time.strftime("%d-%m-%Y %H:%M")
        context["complete_time"] = order.complete_time if order.complete_time == None else order.complete_time.strftime("%d-%m-%Y %H:%M")
        context["order_status"] = order.status
        context["shipping_address"] = order.shipping_info
        context["printer_operator"] = order.printer_operator
        context["packer"] = order.packer
        context["are_all_products_printed"] = all(
            obj.production_step
            == ("wydrukowane" or "w trakcie pakowania" or "zapakowane")
            for obj in products
        )
        context["are_all_products_packed"] = all(
            obj.production_step == "zapakowane" for obj in products
        )
        context["is_at_least_one_product_being_packed"] = any(
            obj.production_step == "w trakcie pakowania" for obj in products
        )
        context["is_at_least_one_product_printed"] = any(
            obj.production_step
            == ("wydrukowane" or "w trakcie pakowania" or "zapakowane")
            for obj in products
        )
        context["is_at_least_one_product_packed"] = any(
            obj.production_step == "zapakowane" for obj in products
        )

        return context

    def post(self, request, *args, **kwargs):
        employee = get_logged_employee(self)
        order = Order.objects.get(pk=self.kwargs["pk"])
        products = order.products.all()
        if request.POST.get("assign_printer_operator"):
            order.printer_operator = employee
            order.status = "w trakcie realizacji"
            for product in products:
                product.production_step = "w trakcie druku"
                product.save()
            order.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        if request.POST.get("assign_packer"):
            order.packer = employee
            for product in products:
                product.production_step = "w trakcie pakowania"
                product.save()
            order.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        if request.POST.get("cancel_printer_operator"):
            order.printer_operator = None
            order.status = "nowe"
            for product in products:
                product.production_step = "nowe"
                product.save()
            order.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        if request.POST.get("cancel_packer"):
            order.packer = None
            for product in products:
                product.production_step = "wydrukowane"
                product.save()
            order.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        if request.POST.get("product_printed"):
            printed_products_ids = request.POST.getlist("checkbox_column")
            for id in printed_products_ids:
                printed_product = order.products.get(pk=id)
                printed_product.production_step = "wydrukowane"
                printed_product.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        if request.POST.get("product_packed"):
            packed_products_ids = request.POST.getlist("checkbox_column")
            for id in packed_products_ids:
                packed_product = order.products.get(pk=id)
                packed_product.production_step = "zapakowane"
                packed_product.save()
            if all(obj.production_step == "zapakowane" for obj in products):
                order.status = "zrealizowane"
                order.complete_time = datetime.now()
                order.save()
            return HttpResponseRedirect(f"{self.kwargs['pk']}")
        return render(request, self.template_name)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
