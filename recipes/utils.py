from django.db.models import F, Sum, Q


def get_recipes_by_tags(tag_list, recipes):
    """Отдает рецепты в соответсвии с тегами"""
    or_condition = Q()
    for i in tag_list.split('_'):
        or_condition.add(Q(tags__contains=i), Q.OR)
    return tag_list, recipes.filter(or_condition)


def create_shopping_list_content(recipes):
    """Создание списка ингредиентов"""
    shop_list_content = ''
    ingredients = recipes.annotate(
        name=F('recipe__ingredients__title'),
        dimension=F('recipe__ingredients__dimension')).values(
        'name', 'dimension').annotate(
        total=Sum('recipe__ingredient_amount__amount')).order_by('name')
    for ingredient in ingredients:
        shop_list_content += f"{ingredient['name']} ({ingredient['dimension']}) - {ingredient['total']} \n"
    return shop_list_content


def get_ingredients(request):
    """Получение ингредиентов из формы создания/редактирования рецепта"""
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value_ingredient]
    return ingredients
