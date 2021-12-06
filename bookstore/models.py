from django.db import models
from category.models import Category
from cloudinary.models import CloudinaryField
# import cloudinary.uploader
# import cloudinary.api

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    price = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image', null= True, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return f'{self.title}'
    
    def tag(self):
        return self.category.name
    
    
    


