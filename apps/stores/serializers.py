from stores.models import Contract, Store
from rest_framework import serializers


class StoreSchema(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"  # field를 일일히 다 나열하는 것보다 이렇게 대체 가능


class ContractSchema(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"  # field를 일일히 다 나열하는 것보다 이렇게 대체 가능
