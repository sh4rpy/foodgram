def get_shopping_list_count(request):
    """Добавляет переменную со счетчиком покупок"""
    if request.user.is_authenticated:
        return {'shopping_list_count': request.user.author_shopping_list.count()}
    return {}


def get_shopping_list_recipes(request):
    """Добавялет переменную со списком рецептов в списке покупок"""
    if request.user.is_authenticated:
        return {'shopping_list_recipes': [i.recipe for i in request.user.author_shopping_list.all()]}
    return {}


def get_favorites_recipes(request):
    """Добавялет переменную со списком избранных рецептов"""
    if request.user.is_authenticated:
        return {'favorites_recipes': [i.recipe for i in request.user.author_favorites.all()]}
    return {}


def get_followings(request):
    """Добавялет переменную со списком подписок"""
    if request.user.is_authenticated:
        return {'followings': [i.following.pk for i in request.user.follower.all()]}
    return {}


def get_variables(request):
    """
    Добавляет переменную с GET-параметрами
    Нужно для сохранения фильтрациии при переключении страниц
    """
    variables = request.GET.copy()
    if 'page' in variables:
        del variables['page']
    return {'variables': '&{0}'.format(variables.urlencode())}
