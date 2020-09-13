from .models import ShoppingList, Recipe, User


def get_shopping_list_count(request):
    """Добавляет переменную со счетчиком покупок"""
    if request.user.is_authenticated:
        return {'shopping_list_count': ShoppingList.objects.select_related('author', 'recipe').filter(
            author=request.user).count()}
    return []


def get_shopping_list_recipes(request):
    """Добавялет переменную со списком рецептов в списке покупок"""
    if request.user.is_authenticated:
        return {'shopping_list_recipes': Recipe.objects.prefetch_related('author', 'ingredients').filter(
            shopping_list__author=request.user)}
    return []


def get_favorites_recipes(request):
    """Добавялет переменную со списком избранных рецептов"""
    if request.user.is_authenticated:
        return {'favorites_recipes': Recipe.objects.prefetch_related('author', 'ingredients').filter(
            favorites__author=request.user)}
    return []


def get_followings(request):
    """Добавялет переменную со списком подписок"""
    if request.user.is_authenticated:
        return {'followings': User.objects.filter(following__user=request.user)}
    return []


def get_variables(request):
    """
    Добавляет переменную с GET-параметрами
    Нужно для сохранения фильтрациии при переключении страниц
    """
    variables = request.GET.copy()
    if 'page' in variables:
        del variables['page']
    return {'variables': '&{0}'.format(variables.urlencode())}
