from django import template


register = template.Library()


@register.filter
def get_recipes_tags(tags):
    """
    Добавляет теги к рецептам
    Помогает избежать ужасных конструкций в шаблонах
    """
    recipes_tags = ''
    if 'lunch' in tags:
        recipes_tags += str('<li class="card__item"><span class="badge badge_style_green">Обед</span></li>')
    if 'breakfast' in tags:
        recipes_tags += str('<li class="card__item"><span class="badge badge_style_orange">Завтрак</span></li>')
    if 'dinner' in tags:
        recipes_tags += str('<li class="card__item"><span class="badge badge_style_purple">Ужин</span></li>')
    return recipes_tags
