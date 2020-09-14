import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from recipes.models import Recipe, User, Follow, FavoritesList, ShoppingList, Ingredient


@require_http_methods(['POST'])
@login_required
def add_favorites(request):
    """Добавляет рецепт в список избранного"""
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    FavoritesList.objects.create(author=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def delete_favorites(request, id):
    """Удаляет рецепт из списка избранного"""
    favorite_recipe = get_object_or_404(FavoritesList, author=request.user, recipe__pk=id)
    favorite_recipe.delete()
    return JsonResponse({'success': True})


@require_http_methods(['POST'])
@login_required
def add_purchases(request):
    """Добавляет рецепт в список покупок"""
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ShoppingList.objects.create(author=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def delete_purchases(request, id):
    """Удаляет рецепт из списка покупок"""
    shop_list = get_object_or_404(ShoppingList, author=request.user, recipe__pk=id)
    shop_list.delete()
    return JsonResponse({'success': True})


@require_http_methods(['POST'])
@login_required
def add_subscriptions(request):
    """Подписывает пользователя на автора"""
    following_id = json.loads(request.body)['id']
    following = get_object_or_404(User, pk=following_id)
    Follow.objects.create(user=request.user, following=following)
    return JsonResponse({'success': True})


@login_required
def delete_subscriptions(request, id):
    """Отписывает пользователя от автора"""
    subscription = get_object_or_404(Follow, user=request.user, following__pk=id)
    subscription.delete()
    return JsonResponse({'success': True})


@login_required
def get_ingredients(request):
    """Достает ингредиенты из базы по запросу"""
    query = request.GET.get('query', '')
    result = list(Ingredient.objects.filter(
        title__istartswith=query).annotate(
        t=F('title'), d=F('dimension')).values('title', 'dimension'))
    return JsonResponse(result, safe=False)
