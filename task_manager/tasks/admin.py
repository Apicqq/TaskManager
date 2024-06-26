from django.contrib import admin

# Register your models here.
from tasks.models import TaskModel, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0
    max = 3


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    pass
