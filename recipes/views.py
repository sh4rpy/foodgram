from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeCreateForm
from .models import Recipe, User, ShoppingList
from .utils import create_shopping_list_file


def index(request):
    tags = request.GET.getlist('tag', '')
    if tags:
        recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').order_by('-pub_date').filter(
            tags__slug__in=tags).order_by('-pub_date').distinct()
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
            author=profile.id, tags__slug__in=tags).order_by('-pub_date').distinct()
    else:
        profile_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            author=profile.id).order_by('-pub_date')
    paginator = Paginator(profile_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'page': page, 'paginator': paginator, 'profile': profile, 'tags': tags})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def follow_index(request):
    users = User.objects.filter(following__user=request.user)
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/follow_index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    tags = request.GET.getlist('tag', '')
    if tags:
        favorites_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            favorites__author=request.user, tags__slug__in=tags).order_by('-pub_date').distinct()
    else:
        favorites_recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
            favorites__author=request.user).order_by('-pub_date')
    paginator = Paginator(favorites_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorites.html', {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def shopping_list(request):
    recipes = Recipe.objects.prefetch_related('author', 'ingredients', 'tags').filter(
        shopping_list__author=request.user)
    return render(request, 'recipes/shopping_list.html', {'recipes': recipes})


@login_required
def shopping_list_delete_recipe(request, recipe_id):
    recipe = get_object_or_404(ShoppingList, author=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('shopping_list')


@login_required
def create_recipe(request):
    # TODO:
    form = RecipeCreateForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})


@login_required
def change_recipe(request, recipe_id):
    # TODO
    form = RecipeCreateForm()
    return render(request, 'recipes/change_recipe.html', {'form': form})


@login_required
def download_shopping_list(request):
    shop_list = ShoppingList.objects.select_related(
        'author', 'recipe').filter(author=request.user)
    create_shopping_list_file(shop_list)
    with open('recipes/download/shopping_list.txt') as file:
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )
