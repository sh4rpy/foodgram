from recipes.models import Recipe


def create_shopping_list_file(shopping_list):
    recipes_pk = []
    ingredients = {}
    for recipe in shopping_list:
        recipes_pk.append(recipe.recipe.pk)
    recipes = Recipe.objects.filter(pk__in=recipes_pk)
    with open('recipes/download/shopping_list.txt', 'w') as file:
        for recipe in recipes:
            for unit in recipe.unit_set.all():
                current_ingredient = f'{unit.ingredient.title} ({unit.ingredient.dimension})'
                if current_ingredient in ingredients:
                    ingredients[current_ingredient] += unit.amount
                else:
                    ingredients[current_ingredient] = unit.amount
        for key, value in ingredients.items():
            file.write(f'{key} - {value}\n')
