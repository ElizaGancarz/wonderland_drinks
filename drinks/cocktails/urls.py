from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('<int:drink_id>/', views.detail_cocktail, name='detail_cocktail'),
    path('<int:drink_id>/like/', views.like_drink, name='like_drink'),
    path('<int:drink_id>/unlike/', views.unlike_drink, name='unlike_drink'),
]
