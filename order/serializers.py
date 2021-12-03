from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = ['user','customer','book','quantity', 'unit_price','transaction_id', 'status']