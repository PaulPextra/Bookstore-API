from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list),
    path('orders/<int:order_no>/', views.order_detail),
]
