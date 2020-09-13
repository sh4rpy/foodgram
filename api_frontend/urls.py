from django.urls import path

from . import views


urlpatterns = [
    # добавлкение рецепта в избранное
    path('add_favorites/', views.add_favorites, name='add_favorites'),
    # удаление рецепта из избранного
    path('delete_favorites/<int:id>/', views.delete_favorites, name='delete_favorites'),
    # добавление рецепта в список покупок
    path('add_purchases/', views.add_purchases, name='add_purchases'),
    # удаление рецепта из списка покупок
    path('delete_purchases/<int:id>/', views.delete_purchases, name='delete_purchases'),
    # подписка на пользователя
    path('add_subscriptions/', views.add_subscriptions, name='add_subscriptions'),
    # отписка от пользователя
    path('delete_subscriptions/<int:id>/', views.delete_subscriptions, name='delete_subscriptions'),
    # список ингредиентов форме создания/редактирования
    path('ingredients/', views.get_ingredients, name='ingredients'),
]
