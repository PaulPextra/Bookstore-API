from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from bookstore.models import Book

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return  '{0} unit(s) of {1}'.format(self.quantity, self.book)