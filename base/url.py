# this file is in charge of connecting the view to the urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('products/', views.getProducts, name="products"),
    # pk stands for primary key because python has id
    path('products/<str:pk>/', views.getProduct, name="product")
]