from rest_framework import fields, serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['name', 'description']