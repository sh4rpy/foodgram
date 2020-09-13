from django.urls import path

from . import views


urlpatterns = [
    # главная страниица
    path('', views.index, name='index'),
    # странициа просмотра рецепта
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    # страница с  подписками
    path('subscriptions/', views.follow_index, name='follow_index'),
    # страница с избранными рецептами
    path('favorites/', views.favorites, name='favorites'),
    # страница со списком покупок
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    # скачивание списка покупок
    path('shopping_list/download/', views.download_shopping_list, name='download'),
    # удаление рецепта из списка покупок
    path('shopping_list/delete/<int:recipe_id>',
         views.shopping_list_delete_recipe, name='shopping_list_delete_recipe'),
    # страница создания рецепта
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    # страница редактрирования рецепта
    path('change_recipe/<int:recipe_id>/', views.change_recipe, name='change_recipe'),
    # удаление рецепта
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    # страница с профилем пользователя
    path('<str:username>/', views.profile, name='profile'),
]
