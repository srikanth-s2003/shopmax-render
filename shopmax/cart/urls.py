from django.urls import path
from . import views

urlpatterns = [
    path('', views.summary, name="cart_summary"),
    path('add/', views.cart_add, name="cart_add"),
    path('delete/', views.cart_delete, name="cart_delete"),
    path('checkout/', views.checkout, name="checkout"),
    path('thank_you/', views.thankyou, name="thankyou"),
]