from django import forms

from tasks.models import SubTask, TaskModel
from tasks.utils import can_set_status_to_completed


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = [
            "name",
            "description",
            "performers",
            "deadline",
            "status",
            "planned_intensity",
            "actual_completion_time",
        ]
        widgets = dict(
            deadline=forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        )


class TaskForm(forms.ModelForm):

    def clean_status(self):
        if self.initial.get("status") is not None:
            initial_status, new_status = (
                self.initial["status"],
                self.cleaned_data["status"],
            )
            if initial_status != "In progress" and new_status == "Completed":
                raise forms.ValidationError(
                    'Задача может быть переведена в статус "Завершена" '
                    "только после её принятия в работу"
                )
            elif new_status == "Paused" and initial_status != "In progress":
                raise forms.ValidationError(
                    'Задача может быть переведена в статус "Приостановлена" '
                    "только после её принятия в работу"
                )
            elif new_status == "Completed" and not can_set_status_to_completed(
                self.instance
            ):
                raise forms.ValidationError(
                    'Задача может быть переведена в статус "Завершена" '
                    "только после того, как все подзадачи будут выполнены."
                )
        return self.cleaned_data["status"]

    class Meta:
        model = TaskModel
        fields = [
            "name",
            "description",
            "performers",
            "deadline",
            "status",
            "planned_intensity",
            "actual_completion_time",
        ]
        widgets = dict(
            deadline=forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        )


TaskCreateFormSet = forms.modelformset_factory(
    SubTask,
    fields=[
        "name",
        "description",
        "performers",
        "deadline",
        "status",
        "planned_intensity",
        "actual_completion_time",
    ],
    extra=1,
    can_delete=False,
    form=TaskForm,
)

TaskUpdateFormSet = forms.inlineformset_factory(
    TaskModel,
    SubTask,
    fields=[
        "name",
        "description",
        "performers",
        "deadline",
        "status",
        "planned_intensity",
        "actual_completion_time",
    ],
    extra=1,
    form=SubTaskForm,
    can_delete=True,
)


class TaskEditForm(TaskForm):
    planned_intensity = forms.IntegerField(
        label="Планируемая интенсивность задачи", disabled=True
    )
    actual_completion_time = forms.IntegerField(
        label="Фактическое время выполнения", disabled=True
    )

    class Meta(TaskForm.Meta):
        pass


class SubTaskEditForm(TaskEditForm):
    pass
