from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.reservation_page, name='reservation'),
    path('api/create/', views.create_reservation, name='create_reservation'),
    path('api/available-times/', views.available_times, name='available_times'),
    path('api/my-reservations/', views.user_reservations, name='user_reservations'),
]
