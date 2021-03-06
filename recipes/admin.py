from django.contrib import admin

from .models import Ingredient, Recipe, Unit, Follow, FavoritesList, ShoppingList


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = 'Число добавлений в "Избранное"'
    list_display = ('title', 'author', 'get_favorites_count')
    list_filter = ('author', 'title', 'tags')
    inlines = (UnitInline,)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('amount', 'ingredient', 'recipe',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following',)


class FavoritesListAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(FavoritesList, FavoritesListAdmin)
admin.site.register(ShoppingList, FavoritesListAdmin)
