# from django.shortcuts import render
from typing import Final  # 변수나 속성이 재할당되지 않도록 지정 (상수 지정, 상속 제어 등)

from drf_spectacular.utils import extend_schema, extend_schema_view
from stores.models import Contract, Store
from stores.serializers import ContractSchema, StoreSchema
from rest_framework import viewsets

STORE_TAG: Final[str] = '상점'


# Create your views here.

# Store에서 처리할 수 있는 view을 만듬
@extend_schema_view(
    list=extend_schema(tags=[STORE_TAG], summary="상점 목록 조회"),
    retrieve=extend_schema(tags=[STORE_TAG]),
    create=extend_schema(tags=[STORE_TAG]),
    update=extend_schema(tags=[STORE_TAG]),
    destroy=extend_schema(tags=[STORE_TAG]),
)
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSchema


CONTRACT_TAG: Final[str] = '상점 계약'


# Create your views here.

# Store에서 처리할 수 있는 view을 만듬
@extend_schema_view(
    list=extend_schema(tags=[CONTRACT_TAG], summary="계약 목록 조회"),
    retrieve=extend_schema(tags=[CONTRACT_TAG]),
    create=extend_schema(tags=[CONTRACT_TAG]),
    update=extend_schema(tags=[CONTRACT_TAG]),
    destroy=extend_schema(tags=[CONTRACT_TAG]),
)
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSchema

