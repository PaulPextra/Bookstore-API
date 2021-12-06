from django.db import models
from bookstore.models import Book
from category.models import Category
from accounts.models import CustomUser


class Order(models.Model):
    PENDING = 'PE'
    REJECTED = 'RE'
    COMPLETED = 'CO'
    
    STATUSES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=150, default=0)
    unit_price = models.PositiveIntegerField()
    status = models.CharField(max_length=2, choices=STATUSES, default=PENDING)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book}"

    def customer(self):
        return f'{self.user.first_name} {self.user.last_name}'