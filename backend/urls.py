from django.urls import path, include 

urlpatterns = [
    path('auth/', include('backend.authentications.urls'))
]