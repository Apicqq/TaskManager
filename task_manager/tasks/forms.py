from django import forms
from django.utils import timezone

from core.constants import Errors, Literals, Values
from tasks.models import TaskModel
from tasks.utils import can_set_status_to_completed


class TaskForm(forms.ModelForm):
    """
    Форма для создания объектов модели TaskModel.

    Здесь переопределяем виджет для поля deadline, чтобы он отображал
    только дату.
    """

    def clean_status(self):
        """
        Метод для проверки валидности поля status у модели TaskModel.

        Проверяется, что задача:
        1. Может быть завершена только после её принятия в работу;
        2. Может быть поставлена на паузу только после её принятия в работу;
        3. Может быть завершена, если все её подзадачи могут быть завершены.
        """
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

    def clean_deadline(self) -> timezone:
        """
        Метод для проверки валидности поля deadline у модели TaskModel.

        Проверяем, что дедлайн у задачи не может быть установлен в прошлом.
        """
        if self.cleaned_data["deadline"] < timezone.now():
            raise forms.ValidationError(Errors.DEADLINE_CANNOT_BE_IN_THE_PAST)
        return self.cleaned_data["deadline"]

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
    TaskModel,
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


class TaskEditForm(TaskForm):
    """
    Форма для редактирования объектов модели TaskModel.

    Здесь переопределяем поля planned_intensity и actual_completion_time,
    чтобы сделать их недоступными для редактирования.
    """

    planned_intensity = forms.IntegerField(
        label=Literals.PLANNED_INTENSITY, disabled=True
    )
    actual_completion_time = forms.IntegerField(
        label=Literals.ACTUAL_COMPLETION_TIME, disabled=True
    )

    class Meta(TaskForm.Meta):
        pass


TaskUpdateFormSet = forms.inlineformset_factory(
    TaskModel,
    TaskModel,
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
    fk_name="parent_task",
)
