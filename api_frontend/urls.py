from django.urls import path

from . import views


urlpatterns = [
    path('add_favorites/', views.add_favorites, name='add_favorites'),
    path('delete_favorites/<int:id>/', views.delete_favorites, name='delete_favorites'),
    path('add_purchases/', views.add_purchases, name='add_purchases'),
    path('delete_purchases/<int:id>/', views.delete_purchases, name='delete_purchases'),
    path('add_subscriptions/', views.add_subscriptions, name='add_subscriptions'),
    path('delete_subscriptions/<int:id>/', views.delete_subscriptions, name='delete_subscriptions'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
]
