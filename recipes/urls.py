from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('subscriptions/', views.follow_index, name='follow_index'),
    path('favorites', views.favorites, name='favorites'),
    path('add_favorites/', views.add_favorites, name='add_favorites'),
    path('delete_favorites/<int:id>/', views.delete_favorites, name='delete_favorites'),
    path('add_purchases/', views.add_purchases, name='add_purchases'),
    path('delete_purchases/<int:id>/', views.delete_purchases, name='delete_purchases'),
    path('add_subscriptions/', views.add_subscriptions, name='add_subscriptions'),
    path('delete_subscriptions/<int:id>/', views.delete_subscriptions, name='delete_subscriptions'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/delete/<int:recipe_id>', views.shopping_list_delete_recipe, name='shopping_list_delete_recipe'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('change_recipe/<int:recipe_id>/', views.change_recipe, name='change_recipe'),
    path('download/', views.download_shopping_list, name='download'),
    path('<str:username>/', views.profile, name='profile'),
]