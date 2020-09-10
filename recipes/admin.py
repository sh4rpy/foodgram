from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Unit, Follow, FavoritesList, ShoppingList


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)


admin.site.register(Ingredient, IngredientAdmin)


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    list_filter = ('author', 'title', 'tags')
    inlines = (UnitInline,)
    #TODO: На странице рецепта вывести число добавлений этого рецепта в избранное


admin.site.register(Recipe, RecipeAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('amount', 'ingredient', 'recipe',)


admin.site.register(Unit, UnitAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following', )


admin.site.register(Follow, FollowAdmin)


class FavoritesListAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe')


admin.site.register(FavoritesList, FavoritesListAdmin)
admin.site.register(ShoppingList, FavoritesListAdmin)
