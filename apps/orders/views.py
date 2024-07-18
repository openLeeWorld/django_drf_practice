# from django.shortcuts import render
from typing import Final  # 변수나 속성이 재할당되지 않도록 지정 (상수 지정, 상속 제어 등)

from drf_spectacular.utils import extend_schema, extend_schema_view
from orders.models import Order
from orders.serializers import OrderSchema
from rest_framework import viewsets

ORDER_TAG: Final[str] = '주문'


# Create your views here.

# order에서 처리할 수 있는 모델을 만듬
@extend_schema_view(
    list=extend_schema(tags=[ORDER_TAG]),
    retrieve=extend_schema(tags=[ORDER_TAG]),
    create=extend_schema(tags=[ORDER_TAG]),
    update=extend_schema(tags=[ORDER_TAG]),
    destroy=extend_schema(tags=[ORDER_TAG]),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSchema
