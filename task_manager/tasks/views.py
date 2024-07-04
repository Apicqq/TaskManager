from django.db.transaction import atomic
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from tasks.forms import (
    TaskForm,
    TaskCreateFormSet,
    TaskEditForm,
    TaskUpdateFormSet,
)
from tasks.mixins import TaskMixin
from tasks.models import TaskModel
from tasks.utils import calculate_task_values


class TaskListView(TaskMixin, ListView):
    """
    Контроллер для отображения списка задач.

    В текущей реализации выводит пустую страницу, навигация осуществляется
    через сайдбар в левой части экрана.
    """

    template_name = "tasks/tasks_list.html"


class TaskDetailView(TaskMixin, DetailView):
    """
    Контроллер для отображения информации о конкретной задаче.
    """

    template_name = "tasks/detail.html"


class TaskCreateView(TaskMixin, CreateView):
    """
    Контроллер, использующийся для создания нового объекта задачи.
    """

    form_class = TaskForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("task_list")

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})

    def get_context_data(self, **kwargs):
        """
        Метод для добавления данных в контекст веб-страницы.
        В данном случае помимо основного контекста передаём формсет,
        при помощи которого к задаче можно добавить подзадачи.
        """
        context = super().get_context_data(**kwargs)
        return dict(
            **context,
            formset=TaskCreateFormSet(queryset=TaskModel.objects.none()),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        """
        Переопределенный метод для отправки POST-запроса и создания нового
        объекта задачи.

        К стандартной реализации добавлены проверки валидности формы и
        формсета, а также реализация бизнес-логики проекта. Помимо этого,
        к методу добавлен декоратор atomic, который гарантирует что транзакция
        и создание объекта будет осуществлено либо полностью, либо не будет
        осуществлено вообще.
        """
        self.object = None
        form = self.get_form()
        formset = TaskCreateFormSet(
            request.POST, form_kwargs={"empty_permitted": False}
        )
        if form.is_valid():
            instance = form.save(commit=False)
            if formset.is_valid():
                instance.is_root_task = True
                instance.save()
                for subtask_form in formset:
                    subtask = subtask_form.save(commit=False)
                    subtask.parent_task = instance
                    subtask.save()
                calculate_task_values(instance)
                return redirect(self.success_url)
            else:
                return self.render_to_response(
                    dict(form=form, formset=formset)
                )
        else:
            return self.render_to_response(dict(form=form, formset=formset))


class TaskDeleteView(TaskMixin, DeleteView):
    """
    Эндпоинт-заглушка для удаления объекта задачи.

    Удаление задач происходит при помощи скрипта, поэтому данный эндпоинт
    нужен только для реализации его логики, в связи с этим шаблон для него
    отсутствует.
    """

    success_url = reverse_lazy("task_list")


class TaskUpdateView(TaskMixin, UpdateView):
    """
    Контроллер, использующийся для редактирования существующего объекта задачи.
    """

    template_name = "tasks/update.html"
    form_class = TaskEditForm
    success_url = reverse_lazy("task_list")

    def get_object(self, queryset=None):
        return get_object_or_404(TaskModel, pk=self.kwargs["task_id"])

    def get_context_data(self, **kwargs):
        """
        Метод для добавления данных в контекст веб-страницы.
        В данном случае помимо основного контекста передаём формсет,
        при помощи которого к задаче можно добавить и/или удалить подзадачи.
        """
        context = super().get_context_data(**kwargs)
        return dict(
            **context,
            formset=TaskUpdateFormSet(
                instance=self.get_object(),
            ),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        """
        Переопределенный метод для отправки POST-запроса и создания нового
        объекта задачи.

        К стандартной реализации добавлены проверки валидности формы и
        формсета, а также реализация бизнес-логики проекта. Помимо этого,
        к методу добавлен декоратор atomic, который гарантирует что транзакция
        и создание объекта будет осуществлено либо полностью, либо не будет
        осуществлено вообще.
        """
        self.object = self.get_object()
        form = self.get_form()
        formset = TaskUpdateFormSet(
            request.POST,
            instance=self.object,
        )
        if form.is_valid():
            instance = form.save(commit=False)
            if formset.is_valid():
                instance.is_root_task = True
                instance.save()
                for subtask_form in formset:
                    if any(
                        subtask_form.cleaned_data.get(field) is None
                        for field in subtask_form
                        if field != ["DELETE", "parent_task", "id"]
                    ):
                        # Пропускаем пустые формы, созданные формсетом,
                        # чтобы не словить ошибку
                        continue
                    subtask = subtask_form.save(commit=False)
                    if subtask_form.cleaned_data.get("DELETE"):
                        subtask.delete()
                    else:
                        subtask.parent_task = instance
                        subtask.save()
                calculate_task_values(instance)
                return redirect(self.success_url)
            else:
                return self.render_to_response(
                    dict(form=form, formset=formset)
                )
        else:
            return self.render_to_response(dict(form=form, formset=formset))

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})


def task_detail(request, task_id):
    """
    Эндпоинт, использующийся для передачи данных в AJAX-script для
    бесшовной навигации между задачами.
    """
    return render(
        request, "tasks/detail.html", dict(task=TaskModel.objects.get(task_id))
    )
