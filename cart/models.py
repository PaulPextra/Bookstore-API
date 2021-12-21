from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from bookstore.models import Book

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             related_name='customer')
    
    book = models.ForeignKey(Book, 
                             on_delete=models.CASCADE, 
                             related_name='fav_book')
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.book