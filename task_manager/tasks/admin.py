from django.contrib import admin

# Register your models here.
from tasks.models import TaskModel, SubTask


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    pass