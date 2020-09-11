from django.db.models import F, Sum


def create_shopping_list_file(recipes):
    ingredients = recipes.annotate(
        name=F('recipe__ingredients__title'),
        dimension=F('recipe__ingredients__dimension')).values(
        'name', 'dimension').annotate(
        total=Sum('recipe__ingredient_amount__amount')).order_by('name')
    with open('recipes/download/shopping_list.txt', 'w') as file:
        for ingredient in ingredients:
            file.write(f"{ingredient['name']} ({ingredient['dimension']}) - {ingredient['total']} \n")


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startwith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value_ingredient]
    return ingredients
