from .models import ShoppingList, FavoritesList, Follow, User


def get_shopping_list_count(request):
    return {'shopping_list_count': ShoppingList.objects.filter(author=request.user.pk).count()}


def get_shopping_list_recipes_pk(request):
    if request.user.is_authenticated:
        shopping_list = ShoppingList.objects.filter(author=request.user)
        return {'shopping_list_recipes_pk': [item.recipe.pk for item in shopping_list]}
    return []


def get_favorites_recipes_pk(request):
    if request.user.is_authenticated:
        favorites = FavoritesList.objects.filter(author=request.user)
        return {'favorites_recipes_pk': [favorite.recipe.pk for favorite in favorites]}
    return []


def get_followings_pk(request):
    if request.user.is_authenticated:
        followings = Follow.objects.filter(user=request.user)
        return {'followings_pk': [following.following.pk for following in followings]}
    return []


def get_variables(request):
    variables = request.GET.copy()
    if 'page' in variables:
        del variables['page']
    return {'variables': '&{0}'.format(variables.urlencode())}
