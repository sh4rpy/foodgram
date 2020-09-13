from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Форма создания/редактиирования рецепта"""
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input', 'id': 'id_name'}),
            'tags': forms.CheckboxSelectMultiple(),
            'cooking_time': forms.NumberInput(attrs={'class': 'form__input', 'id': 'id_time'}),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': '8', 'id': 'id_description'}),
        }
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'cooking_time': 'Время приготовления',
            'image': 'Загрузить фото',
        }
