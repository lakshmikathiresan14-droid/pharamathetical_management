from django.urls import path
from . import views 

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/',views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Medicine Management URLs
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('update/<int:pk>/', views.update_medicine, name='update_medicine'),
    path('medicine/delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),

    # General Pages URLs
    #path('home/', views.home, name='home'),  # Home page
    # path('about-us/', views.about_us, name='about_us'),  # About Us page
    path('contact-us/', views.contact_us, name='contact_us'),  # Contact Us page
    path('medicines/', views.medicine_list, name='medicine_list'),  # Medicine listing page
    path('view_medicine/<int:pk>/', views.view_medicine, name='view'),  # Medicine listing page
    path('live_search/',views.live_search, name='live_search'),
]
