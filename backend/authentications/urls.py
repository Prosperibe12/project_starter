from django.urls import path 

from backend.authentications import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify_email/', views.VerifyEmail.as_view(), name='verify-email'),
]