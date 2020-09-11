from django import forms

from .models import Recipe, Tag


class RecipeCreateForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), to_field_name='name')

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image',)

    # def __init__(self, data=None, *args, **kwargs):
    #     if data is not None:
    #         data = data.copy()
    #         for k in ('breakfast', 'lunch', 'dinner'):
    #             if k in data:
    #                 data.update({'tags': k})
    #     super().__init__(data=data, *args, **kwargs)
