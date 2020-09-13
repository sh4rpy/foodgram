from django.contrib.auth import get_user_model
from django.db import models

from multiselectfield import MultiSelectField

User = get_user_model()
RECIPES_TAGS = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
)


class Ingredient(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    dimension = models.CharField(max_length=20, verbose_name='Единица измерения')

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author_recipes', verbose_name='Автор')
    title = models.CharField(max_length=250, verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='Unit', through_fields=('recipe', 'ingredient'),
        related_name='recipes_ingredient')
    tags = MultiSelectField(
        choices=RECIPES_TAGS, verbose_name='Теги', blank=True, null=True)
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время приготовления (мин.)')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title


class Unit(models.Model):
    amount = models.IntegerField(default=1)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredient_amount')


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower', verbose_name='Подписчик')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following', verbose_name='Автор')

    class Meta:
        unique_together = ('user', 'following')


class FavoritesList(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author_favorites', verbose_name='Автор')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Избранные рецепты')

    class Meta:
        unique_together = ('author', 'recipe',)


class ShoppingList(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author_shopping_list',
        verbose_name='Автор')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list',
        verbose_name='Список покупок')

    class Meta:
        unique_together = ('author', 'recipe',)
