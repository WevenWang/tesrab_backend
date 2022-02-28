# this file is in charge of connecting the view to the urls
from django.urls import path
from base.views import product_views as views

urlpatterns = [
    # path('', views.getRoutes, name="routes"),

    path('', views.getProducts, name="products"),
    # pk stands for primary key because python has id
    path('create/', views.create_product, name="product-create"),
    path('upload/', views.upload_image, name="image-upload"),
    path('<str:pk>/', views.getProduct, name="product"),
    path('update/<str:pk>/', views.update_product, name="product-update"),
    path('delete/<str:pk>/', views.delete_product, name="product-delete"),

]
