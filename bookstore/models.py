from django.db import models
from category.models import Category
from cloudinary.models import CloudinaryField
import random

def generate_isbn():
    
    """This function generates ISBN for each book"""
    
    Random_num = [str(i) for i in range(10)]
    value = [random.choice(Random_num) for i in range(13)]
    ISBN = "".join(value)
    return ISBN

class Author(models.Model):
    name = models.CharField(max_length=100)
    about_author = models.TextField()
    
    class Meta:
        ordering = ['-name']
        
    def __str__(self):
        return f'{self.name}'
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    description = models.CharField(max_length=250)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    publisher = models.CharField(max_length=200, 
                                 null=True, 
                                 blank=True)
    
    isbn = models.CharField(max_length=13, 
                            default=generate_isbn(), 
                            null=True, 
                            blank=True, 
                            unique=True)
    
    price = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    image = CloudinaryField('image', 
                            null= True, 
                            blank=True)
    
    is_active = models.BooleanField(default=True)
    
    category = models.ForeignKey(Category, 
                                 on_delete=models.SET_NULL, 
                                 blank=True, 
                                 null=True)
    
    rating = models.IntegerField(blank=True, 
                                         null=True, 
                                         default=4)
    
    class Meta:
        ordering = ['-title']
        
    def __str__(self):
        return f'{self.title}'
    @property
    def tag(self):
        return self.category.name
    
    @property
    def author_name(self):
        return self.author.name
    
    
    


