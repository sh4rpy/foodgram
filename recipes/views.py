import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeCreateOrUpdateForm
from .models import Recipe, User, Follow, FavoritesList, ShoppingList, Ingredient
from .utils import create_file


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def index(request):
    tags = request.GET.getlist('tag', '')
    if tags:
        recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').order_by('-pub_date').filter(
            tags__in=tags)
    else:
        recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator, 'tags': tags})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    tags = request.GET.getlist('tag', '')
    if tags:
        profile_recipes = Recipe.objects.prefetch_related(
            'author', 'ingredients', 'tags').filter(
            author=profile.id, tags__in=tags).order_by('-pub_date')
    else:
        profile_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            author=profile.id).order_by('-pub_date')
    paginator = Paginator(profile_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'page': page, 'paginator': paginator, 'profile': profile, 'tags': tags})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').get(pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def follow_index(request):
    subscriptions = Follow.objects.select_related('user', 'following').filter(user=request.user)
    favorites_authors = [subscription.following.pk for subscription in subscriptions]
    users = User.objects.filter(pk__in=favorites_authors)
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/follow_index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    favorites = FavoritesList.objects.select_related('author', 'recipe').filter(author=request.user)
    favorites_recipes_pk = [favorite.recipe.pk for favorite in favorites]
    tags = request.GET.getlist('tag', '')
    if tags:
        favorites_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            pk__in=favorites_recipes_pk, tags__in=tags).order_by('-pub_date')
    else:
        favorites_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            pk__in=favorites_recipes_pk).order_by('-pub_date')
    paginator = Paginator(favorites_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorites.html', {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def shopping_list(request):
    shop_list = ShoppingList.objects.select_related('author', 'recipe').filter(author=request.user)
    recipes_pk = [recipe.recipe.pk for recipe in shop_list]
    recipes = Recipe.objects.filter(pk__in=recipes_pk)
    return render(request, 'recipes/shopping_list.html', {'recipes': recipes})


@login_required
def shopping_list_delete_recipe(request, recipe_id):
    recipe = get_object_or_404(ShoppingList, author=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('shopping_list')


@login_required
def create_recipe(request):
    # TODO:
    form = RecipeCreateOrUpdateForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})


@login_required
def change_recipe(request, recipe_id):
    # TODO
    form = RecipeCreateOrUpdateForm()
    return render(request, 'recipes/change_recipe.html', {'form': form})


@login_required
def download_shopping_list(request):
    shopping_list = ShoppingList.objects.select_related(
        'author', 'recipe').filter(author=request.user)
    create_file.create_shopping_list_file(shopping_list)
    with open('recipes/download/shopping_list.txt') as file:
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response


@login_required
def add_favorites(request):
    if request.method == 'POST':
        recipe_id = int(json.loads(request.body)['id'])
        recipe = Recipe.objects.prefetch_related(
            'author', 'ingredients', 'tags').get(pk=recipe_id)
        FavoritesList.objects.create(author=request.user, recipe=recipe)
        return JsonResponse({'success': True})


@login_required
def delete_favorites(request, id):
    recipe = Recipe.objects.get(pk=id)
    FavoritesList.objects.select_related('author', 'recipe').get(
        author=request.user, recipe=recipe).delete()
    return JsonResponse({'success': True})


@login_required
def add_purchases(request):
    if request.method == 'POST':
        recipe_id = int(json.loads(request.body)['id'])
        recipe = Recipe.objects.prefetch_related(
            'author', 'ingredients', 'tags').get(pk=recipe_id)
        ShoppingList.objects.create(author=request.user, recipe=recipe)
        return JsonResponse({'success': True})


@login_required
def delete_purchases(request, id):
    recipe = Recipe.objects.prefetch_related(
        'author', 'ingredients', 'tags').get(pk=id)
    ShoppingList.objects.select_related('author', 'recipe').get(
        author=request.user, recipe=recipe).delete()
    return JsonResponse({'success': True})


@login_required
def add_subscriptions(request):
    if request.method == 'POST':
        following_id = int(json.loads(request.body)['id'])
        following = User.objects.get(pk=following_id)
        Follow.objects.create(user=request.user, following=following)
        return JsonResponse({'success': True})


@login_required
def delete_subscriptions(request, id):
    following = User.objects.get(pk=id)
    Follow.objects.get(user=request.user, following=following).delete()
    return JsonResponse({'success': True})


@login_required
def get_ingredients(request):
    query = request.GET.get('query', '')
    result = []
    for ing in Ingredient.objects.filter(title__istartswith=query):
        result.append({
            'title': ing.title,
            'dimension': ing.dimension,
        })
    print(result)
    return JsonResponse({'result': result})
