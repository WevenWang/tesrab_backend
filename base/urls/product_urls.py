# this file is in charge of connecting the view to the urls
from django.urls import path
from base.views import product_views as views

urlpatterns = [
    # path('', views.getRoutes, name="routes"),

    path('', views.getProducts, name="products"),
    # pk stands for primary key because python has id
    path('<str:pk>/', views.getProduct, name="product"),

]
