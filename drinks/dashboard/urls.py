from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('delete_drink/<int:drink_id>/', views.delete_drink, name='delete_drink'),

]
