from orders.models import Customer, Order, Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'size', 'type', 'pattern_index']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'city', 'zip_code']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    shipping_info = CustomerSerializer(many=False)

    class Meta:
        model = Order
        fields = ['products', 'shipping_info', 'order_time', 'store_order_id']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        shipping_info_data = validated_data.pop('shipping_info')
        shipping_info = Customer.objects.filter(id=shipping_info_data.get('id')).first()
        products = []
        if not shipping_info:
            shipping_info = CustomerSerializer.create(CustomerSerializer(), shipping_info_data)
        for product_data in products_data:
            products.append(Product.objects.create(**product_data))
        order = Order.objects.create(shipping_info=shipping_info, **validated_data)
        order.products.set(products)
        return order



