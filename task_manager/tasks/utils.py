def can_set_status_to_completed(task):
    if task.status == "Completed":
        return True
    elif task.status == "In progress":
        return all(
            can_set_status_to_completed(
                subtask
            ) for subtask in task.subtasks.all()
        )
    else:
        return False
