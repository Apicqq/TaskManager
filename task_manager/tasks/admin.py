from django.contrib import admin

from tasks.models import TaskModel, SubTask


class SubTaskInline(admin.TabularInline):
    """
    Базовый инлайн для подзадач.
    """
    model = SubTask
    extra = 0


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    """Базовая админ-панель для задач."""
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Базовая админ-панель для задач."""
    pass
