from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField()
    cost = serializers.ReadOnlyField(source='get_price')
    
    class Meta:
        model = Order
        fields = ['customer',
                  'book',
                  'quantity', 
                  'order_no',
                  'cost']