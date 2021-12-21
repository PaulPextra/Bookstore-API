from rest_framework import serializers
from . models import Book
from category.serializers import CategorySerializer

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ['title', 
                  'author', 
                  'category', 
                  'price', 
                  'image'] 
        
class AddBookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ['title',
                  'description', 
                  'author',
                  'publisher',
                  'isbn',
                  'price',
                  'category', 
                  'price', 
                  'image']
        
class BookDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=250)
    author = serializers.CharField(max_length=100)
    publisher = serializers.CharField(max_length=200)
    isbn = serializers.CharField(max_length=13)
    price = serializers.IntegerField()
    category = CategorySerializer(read_only=True, many=True)
    rating = serializers.IntegerField(max_value=5, min_value=1)
