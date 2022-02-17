# this file is in charge of connecting the view to the urls
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('products/', views.getProducts, name="products"),
    # pk stands for primary key because python has id
    path('products/<str:pk>/', views.getProduct, name="product"),

    # use the customized token in views.py
    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/profile/', views.getUserProfile, name="user-profile" )
]