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
    name = models.CharField(primary_key=True, 
                            max_length=100,
                            unique=True)
    
    about_author = models.TextField()
    
    class Meta:
        ordering = ['-name']
        
    def __str__(self):
        return f'{self.name}'
    
class Book(models.Model):
    title = models.CharField(unique=True, 
                             max_length=200,
                             primary_key=True)
    
    description = models.TextField()
    
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE, 
                               related_name='author')
    
    publisher = models.CharField(max_length=200, 
                                 null=True, 
                                 blank=True)
    
    isbn = models.CharField(max_length=13, 
                            default=generate_isbn(), 
                            null=True, 
                            blank=True, 
                            unique=True)
    
    price = models.FloatField(help_text='in Dollar ($)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    image = CloudinaryField('image', 
                            null= True, 
                            blank=True,)
    
    is_active = models.BooleanField(default=True)
    
    category = models.ManyToManyField(Category,
                                      related_name='book_category')
    
    rating = models.PositiveIntegerField(blank=True, 
                                         null=True, 
                                         default=4)
    
    class Meta:
        ordering = ['-title']
        
    def __str__(self):
        return f'{self.title}'
    