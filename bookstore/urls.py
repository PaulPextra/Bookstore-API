from django.urls import path
from . import views
from . models import Book

urlpatterns = [
    path('book_list/', views.book_list ),
    path('book_detail/<int:book_id>/', views.book_detail),
]
