from django.contrib import admin

from tasks.models import TaskModel


class SubTaskInline(admin.TabularInline):
    """
    Базовый инлайн для подзадач.
    """
    model = TaskModel
    can_delete = False
    extra = 0
    fk_name = "parent_task"


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    """Базовая админ-панель для задач."""
    inlines = [SubTaskInline]
