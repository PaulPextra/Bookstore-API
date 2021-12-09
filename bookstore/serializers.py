from rest_framework import serializers
from . models import Book

class BookSerializer(serializers.ModelSerializer):
    
    tag = serializers.ReadOnlyField()
    author_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'author_name', 'tag', 'price', 'image'] 
        
class BookDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=250)
    author = serializers.CharField(max_length=100)
    publisher = serializers.CharField(max_length=200)
    isbn = serializers.CharField(max_length=13)
    price = serializers.CharField(max_length=50)
    tag = serializers.ReadOnlyField()
    rating = serializers.IntegerField()
