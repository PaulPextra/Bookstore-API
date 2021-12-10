from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField()
    book_title = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = ['id',
                  'user',
                  'customer',
                  'book',
                  'book_title',
                  'quantity', 
                  'unit_price',
                  'transaction_id', 
                  'status']