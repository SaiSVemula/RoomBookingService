"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # rooms
    path('rooms/', views.get_rooms, name='get_rooms'),
    path('rooms/<int:room_id>/slots/', views.get_available_slots, name='get_available_slots'),
    # path('api/users/', views.get_user, name='get_all_users'),
    # users
    path('api/users/<int:user_id>/', views.get_user, name='get_user'),
    path('api/users/create/', views.create_user, name='create_user'),
    path('api/users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('api/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    # bookings
    path('bookings/', views.get_bookings, name='get_bookings'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
]
