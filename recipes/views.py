from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeForm
from .models import Recipe, User, ShoppingList, Ingredient, Unit
from .utils import get_recipes_by_tags, create_shopping_list_content, get_ingredients


def index(request):
    """Главная страница"""
    tags = []
    recipes = Recipe.objects.prefetch_related('author', 'ingredients')
    # если запрос с фильтрацией, переопределяем tags и recipes
    if 'tags' in request.GET:
        tag_list = request.GET.get('tags')
        tags, recipes = get_recipes_by_tags(tag_list, recipes)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator, 'tags': tags})


def profile(request, username):
    """Профиль пользователя"""
    tags = []
    profile = get_object_or_404(User, username=username)
    profile_recipes = profile.author_recipes.all()
    # если запрос с фильтрацией, переопределяем tags и profile_recipes
    if 'tags' in request.GET:
        tag_list = request.GET.get('tags')
        tags, profile_recipes = get_recipes_by_tags(tag_list, profile_recipes)
    paginator = Paginator(profile_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'page': page, 'paginator': paginator, 'profile': profile, 'tags': tags})


def recipe_detail(request, recipe_id):
    """Просмотр рецепта"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def follow_index(request):
    """Просмотр подписок"""
    users = request.user.follower.all()
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/follow_index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    """Просмотр избранных рецептов"""
    tags = []
    favorites_recipes = Recipe.objects.prefetch_related('author', 'ingredients').filter(
        favorites__author=request.user)
    # если запрос с фильтрацией, переопределяем tags и favorites_recipes
    if 'tags' in request.GET:
        tag_list = request.GET.get('tags')
        tags, favorites_recipes = get_recipes_by_tags(tag_list, favorites_recipes)
    paginator = Paginator(favorites_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorites.html', {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def shopping_list(request):
    """Просмотр списка покупок"""
    recipes = Recipe.objects.prefetch_related('author', 'ingredients').filter(
        shopping_list__author=request.user)
    return render(request, 'recipes/shopping_list.html', {'recipes': recipes})


@login_required
def shopping_list_delete_recipe(request, recipe_id):
    """Удаление рецепта из списка покупок"""
    recipe = get_object_or_404(ShoppingList, author=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('shopping_list')


@login_required
def download_shopping_list(request):
    """Скачивание списка покупок"""
    shop_list = ShoppingList.objects.select_related(
        'author', 'recipe').filter(author=request.user)
    # создаем переменную с ингредиентами для покупки
    shop_list_content = create_shopping_list_content(shop_list)
    response = HttpResponse(shop_list_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
    return response


@login_required
def create_recipe(request):
    """Создание рецепта"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            # получаем ингредиенты из формы
            ingredients = get_ingredients(request)
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                unit = Unit(amount=amount, ingredient=ingredient, recipe=recipe)
                unit.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})


@login_required
def change_recipe(request, recipe_id):
    """Редактирование рецепта"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_detail', recipe_id=recipe.pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            ingredients = get_ingredients(request)
            # если новые игредиенты переданы, очищаем прошлые
            # if ingredients:
            recipe.ingredient_amount.all().delete()
            # и сохраняем новые ингредиенты
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                unit = Unit(amount=amount, ingredient=ingredient, recipe=recipe)
                unit.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/change_recipe.html', {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, recipe_id):
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_detail', recipe_id=recipe.pk)
    recipe.delete()
    return redirect('profile', username=recipe.author)


def page_not_found(request, exception):
    """Страница 404"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )
