from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="shopHome"),
    path('about/', views.aboutus, name="aboutus"),
    path('contact/', views.contact, name="contact"),
    path('tracker/', views.tracker, name="tracker"),
    path('search/', views.search, name="search"),
    path('products/<int:myid>', views.productViews, name="productViews"),
    path('checkout/', views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name="handleRequest"),
]
