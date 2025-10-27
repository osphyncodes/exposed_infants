from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('password-reset/request/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', views.reset_password, name='reset_password'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]