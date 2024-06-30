from django.db.models import Sum


def can_set_status_to_completed(task):
    if task.status == "Completed":
        return True
    elif task.status == "In progress":
        return all(
            can_set_status_to_completed(subtask)
            for subtask in task.subtasks.all()
        )
    else:
        return False


def calculate_task_values(instance):
    # instance = form.save()
    # for subtask_form in formset:
    #     subtask = subtask_form.save(commit=False)
    #     subtask.task = instance
    #     subtask.save()
    if instance.subtasks.exists():
        subtask_sums = instance.subtasks.aggregate(
            planned_intensity=Sum("planned_intensity"),
            actual_completion_time=Sum("actual_completion_time"),
        )
        instance.planned_intensity = (
            subtask_sums["planned_intensity"] + instance.planned_intensity
        )
        instance.actual_completion_time = (
            subtask_sums["actual_completion_time"]
            + instance.actual_completion_time
        )
        instance.save()
    else:
        instance.planned_intensity = 0
        instance.actual_completion_time = 0
        instance.save()
