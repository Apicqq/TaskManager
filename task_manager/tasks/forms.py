from django import forms

from core.constants import Errors, Literals, Values
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
            if (
                    initial_status != Literals.IN_PROGRESS_INTERNAL
                    and new_status == Literals.COMPLETED_INTERNAL
            ):
                raise forms.ValidationError(
                    Errors.TASK_CANNOT_BE_COMPLETED_UNTIL_IN_PROGRESS
                )
            elif (
                    new_status == Literals.PAUSED_INTERNAL
                    and initial_status != Literals.IN_PROGRESS_INTERNAL
            ):
                raise forms.ValidationError(
                    Errors.TASK_CANNOT_BE_PAUSED_UNTIL_IN_PROGRESS
                )
            elif (
                    new_status == Literals.COMPLETED_INTERNAL
                    and not can_set_status_to_completed(self.instance)
            ):
                raise forms.ValidationError(
                    Errors.TASK_CANNOT_BE_COMPLETED_UNTIL_ALL_SUBTASKS_ARE_DONE
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
    extra=Values.FORMSETS_EXTRA_FORMS,
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
    extra=Values.FORMSETS_EXTRA_FORMS,
    form=TaskForm,
    can_delete=True,
)


class TaskEditForm(TaskForm):
    planned_intensity = forms.IntegerField(
        label=Literals.PLANNED_INTENSITY, disabled=True
    )
    actual_completion_time = forms.IntegerField(
        label=Literals.ACTUAL_COMPLETION_TIME, disabled=True
    )

    class Meta(TaskForm.Meta):
        pass


class SubTaskEditForm(TaskEditForm):
    pass
