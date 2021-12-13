from django.urls import path
from . import views
from . models import Book

urlpatterns = [
    path('books/add/', views.add_book),
    path('books/', views.book_list ),
    path('books/<int:book_id>/', views.search_by_id),
    path('books/<str:category>/', views.search_by_category),
    # path('books/<str:author>/', views.search_by_author),
]
