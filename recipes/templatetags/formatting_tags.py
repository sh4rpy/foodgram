from django import template


register = template.Library()


@register.filter
def formatting_tags(request, tag):
    """Форматирование GET-параметра tags в понятный вид"""
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
        tags = tags.split('_')
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
        if '' in tags:
            tags.remove('')
        result = '_'.join(tags)
        return result
    return tag
