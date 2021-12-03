from rest_framework import serializers
from . models import Book

class BookSerializer(serializers.ModelSerializer):
    
    tag = serializers.ReadOnlyField()
    
    image = serializers.ImageField(max_length=None, 
                                   allow_empty_file=False, 
                                   allow_null=True, 
                                   required=False)
    
    class Meta:
        model = Book
        fields = ['title', 'price', 'image', 'tag'] 
        
class BookDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=250)
    author = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=13)
    price = serializers.CharField(max_length=50)
