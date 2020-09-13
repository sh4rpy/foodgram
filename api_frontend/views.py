import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse

from recipes.models import Recipe, User, Follow, FavoritesList, ShoppingList, Ingredient


@login_required
def add_favorites(request):
    """Добавляет рецепт в список избранного"""
    if request.method == 'POST':
        recipe_id = int(json.loads(request.body)['id'])
        recipe = Recipe.objects.prefetch_related(
            'author', 'ingredients').get(pk=recipe_id)
        FavoritesList.objects.create(author=request.user, recipe=recipe)
        return JsonResponse({'success': True})


@login_required
def delete_favorites(request, id):
    """Удаляет рецепт из списка избранного"""
    recipe = Recipe.objects.get(pk=id)
    FavoritesList.objects.select_related('author', 'recipe').get(
        author=request.user, recipe=recipe).delete()
    return JsonResponse({'success': True})


@login_required
def add_purchases(request):
    """Добавляет рецепт в список покупок"""
    if request.method == 'POST':
        recipe_id = int(json.loads(request.body)['id'])
        recipe = Recipe.objects.prefetch_related(
            'author', 'ingredients').get(pk=recipe_id)
        ShoppingList.objects.create(author=request.user, recipe=recipe)
        return JsonResponse({'success': True})


@login_required
def delete_purchases(request, id):
    """Удаляет рецепт из списка покупок"""
    recipe = Recipe.objects.prefetch_related(
        'author', 'ingredients').get(pk=id)
    ShoppingList.objects.select_related('author', 'recipe').get(
        author=request.user, recipe=recipe).delete()
    return JsonResponse({'success': True})


@login_required
def add_subscriptions(request):
    """Подписывает пользователя на автора"""
    if request.method == 'POST':
        following_id = int(json.loads(request.body)['id'])
        following = User.objects.get(pk=following_id)
        Follow.objects.create(user=request.user, following=following)
        return JsonResponse({'success': True})


@login_required
def delete_subscriptions(request, id):
    """Отписывает пользователя от автора"""
    following = User.objects.get(pk=id)
    Follow.objects.get(user=request.user, following=following).delete()
    return JsonResponse({'success': True})


@login_required
def get_ingredients(request):
    """Достает ингредиенты из базы по запросу"""
    query = request.GET.get('query', '')
    result = list(Ingredient.objects.filter(
        title__istartswith=query).annotate(
        t=F('title'), d=F('dimension')).values('title', 'dimension'))
    return JsonResponse(result, safe=False)
