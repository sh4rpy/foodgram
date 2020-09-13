from django.db.models import F, Sum, Q


def get_recipes_by_tags(request, recipes):
    """Отдает рецепты в соответсвии с тегами"""
    tags = request.GET.getlist('tag')
    or_condition = Q()
    for i in tags:
        or_condition.add(Q(tags__contains=i), Q.OR)

    return tags, recipes.filter(or_condition)


def create_shopping_list_file(recipes):
    """Создание файла со списком ингредиентов"""
    ingredients = recipes.annotate(
        name=F('recipe__ingredients__title'),
        dimension=F('recipe__ingredients__dimension')).values(
        'name', 'dimension').annotate(
        total=Sum('recipe__ingredient_amount__amount')).order_by('name')
    with open('recipes/download/shopping_list.txt', 'w') as file:
        for ingredient in ingredients:
            file.write(f"{ingredient['name']} ({ingredient['dimension']}) - {ingredient['total']} \n")


def get_ingredients(request):
    """Получение ингредиентов из формы создания/редактирования рецепта"""
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value_ingredient]
    return ingredients
