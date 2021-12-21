from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.add_book),
    path('book/<str:book_title>/', views.update_book),
    path('books/', views.fetch_books),
    path('books/search/<str:title>/', views.search_by_title),
    path('books/search/<str:category>/', views.search_by_category),
    path('books/search/<str:book_author>/', views.search_by_author),
]
