import django_tables2 as tables
from .models import Order, Product


class OrderTable(tables.Table):
    number_of_products = tables.Column(
        accessor="get_number_of_products",
        verbose_name="Produkty",
        order_by=("products"),
    )

    class Meta:
        model = Order
        order_by = "-id"
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}
        row_attrs = {
            "onClick": lambda record: f"document.location.href='{record.id}';",
            "style": "cursor: pointer;",
        }
        fields = (
            "id",
            "number_of_products",
            "shipping_info",
            "order_time",
            "complete_time",
            "status",
            "packer",
            "printer_operator",
        )


class OrderTableAll(tables.Table):
    checkbox_column = tables.CheckBoxColumn(
        accessor="pk",
        attrs={
            "td": {
                "onclick": "(function(e) { e.stopPropagation(); })(event)",
            },
            "th__input": {"onclick": "toggle(this)"},
        },
        orderable=False,
    )

    number_of_products = tables.Column(
        accessor="get_number_of_products",
        verbose_name="Produkty",
    )

    class Meta:
        model = Order
        order_by = "-id"
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}
        row_attrs = {
            "onClick": lambda record: f"document.location.href='{record.id}';",
            "style": "cursor: pointer;",
        }
        fields = (
            "checkbox_column",
            "id",
            "number_of_products",
            "shipping_info",
            "order_time",
            "complete_time",
            "status",
            "packer",
            "printer_operator",
            "production_site",
        )


class ProductsTable(tables.Table):

    checkbox_column = tables.CheckBoxColumn(
        accessor="pk", attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False
    )

    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "checkbox_column",
            "id",
            "name",
            "size",
            "type",
            "pattern_index",
            "production_step",
        )
