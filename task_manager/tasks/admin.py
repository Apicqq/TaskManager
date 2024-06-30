from django.contrib import admin

from tasks.models import TaskModel, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    pass
