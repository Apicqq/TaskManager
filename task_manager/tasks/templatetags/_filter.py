from django import template

register = template.Library()


@register.filter
def _filter(queryset, value):
    """Темплейттэг, фильтрующий поступающий кверисет по полю parent_task.

    Используется в главном шаблоне для корректного отображения всех подзадач
    у каждой задачи.
    """
    return queryset.filter(parent_task=value)
