from django.urls import path
from productsapi import views


urlpatterns = [
    
    path('api/signup/', views.signup_view, name='signup-api'),
    path('api/login/', views.login_view, name='login-api'),
    path('api/logout/',views.logout_api, name='logout-api'),
    path('api/medicines/add/',views.add_medicine, name='add_medicines_api'),
    path('api/medicines/<int:pk>/update/', views.update_medicine_api, name='update_medicine_api'),
     path('api/medicines/<int:pk>/delete/', views.delete_medicine_api, name='delete_medicine_api'),
]

