from orders.models import Order
from rest_framework import serializers


class OrderSchema(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"  # field를 일일히 다 나열하는 것보다 이렇게 대체 가능
