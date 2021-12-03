from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list),
    path('orders/<int:order_id>/', views.order_detail),
]
