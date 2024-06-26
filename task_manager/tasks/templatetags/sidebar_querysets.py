from django import template

from tasks.models import TaskModel, SubTask

register = template.Library()


@register.simple_tag()
def sidebar_querysets():
    return dict(
        tasks=TaskModel.objects.all(),
        subtasks=SubTask.objects.all()
    )