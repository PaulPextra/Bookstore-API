from django.urls import path
from . import views
from . models import Book

urlpatterns = [
    path('books/', views.book_list ),
    path('books/<int:book_id>/', views.search_by_id),
    path('books/<int:author>/', views.search_by_author),
]
