from django import template

register = template.Library()


@register.filter
def _filter(queryset, value):
    return queryset.filter(task=value)
