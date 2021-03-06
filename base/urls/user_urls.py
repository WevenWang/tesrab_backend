# this file is in charge of connecting the view to the urls
from django.urls import path
from base.views import user_views as views


urlpatterns = [
    # use the customized token in views.py
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.resgisterUser, name='register'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.getUserProfile, name="user-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    
    # admin only path
    path('', views.getUsers, name="users"),
    path('<str:pk>/', views.getUserById, name="user"),
    path('delete/<str:pk>/', views.deleteUser, name="user-delete"),
    path('update/<str:pk>/', views.updateUser, name="user-update"),
    
]
