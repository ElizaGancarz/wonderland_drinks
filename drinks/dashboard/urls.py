from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_drink, name='create'),
    path('edit/<int:drink_id>/', views.edit_drink, name='edit'),
    path('delete_drink/<int:drink_id>/', views.delete_drink, name='delete_drink'),
]
