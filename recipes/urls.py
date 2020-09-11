from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('subscriptions/', views.follow_index, name='follow_index'),
    path('favorites/', views.favorites, name='favorites'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/download/', views.download_shopping_list, name='download'),
    path('shopping_list/delete/<int:recipe_id>', views.shopping_list_delete_recipe, name='shopping_list_delete_recipe'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('change_recipe/<int:recipe_id>/', views.change_recipe, name='change_recipe'),
    path('<str:username>/', views.profile, name='profile'),
]
