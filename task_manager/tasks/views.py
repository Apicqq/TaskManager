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
    SubTaskForm,
    TaskEditForm,
    SubTaskEditForm,
    TaskUpdateFormSet,
)
from tasks.mixins import TaskMixin, SubTaskMixin
from tasks.models import SubTask, TaskModel
from tasks.utils import calculate_task_values


class TaskListView(TaskMixin, ListView):
    template_name = "tasks/tasks_list.html"


class TaskDetailView(TaskMixin, DetailView):
    template_name = "tasks/detail.html"


class TaskCreateView(TaskMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("task_list")

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(
            **context,
            formset=TaskCreateFormSet(queryset=SubTask.objects.none()),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = TaskCreateFormSet(
            request.POST, form_kwargs={"empty_permitted": False}
        )
        if form.is_valid():
            instance = form.save(commit=False)
            if formset.is_valid():
                instance.save()
                for subtask_form in formset:
                    subtask = subtask_form.save(commit=False)
                    subtask.task = instance
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
    success_url = reverse_lazy("task_list")


class TaskUpdateView(TaskMixin, UpdateView):
    template_name = "tasks/update.html"
    form_class = TaskEditForm

    def get_object(self, queryset=None):
        return get_object_or_404(TaskModel, pk=self.kwargs["task_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(
            **context,
            formset=TaskUpdateFormSet(
                instance=self.get_object(),
            ),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = TaskUpdateFormSet(
            request.POST,
            instance=self.object,
            form_kwargs={"empty_permitted": False},
        )
        if form.is_valid():
            task = form.save(commit=False)
            if formset.is_valid():
                task.save()
                formset.save()
                calculate_task_values(self.object)
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    dict(form=form, formset=formset)
                )
        else:
            return self.render_to_response(dict(form=form, formset=formset))

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})


class SubTaskCreateView(SubTaskMixin, CreateView):
    form_class = TaskCreateFormSet


class SubTaskDeleteView(SubTaskMixin, DeleteView):
    success_url = reverse_lazy("task_list")


class SubTaskUpdateView(SubTaskMixin, UpdateView):
    template_name = "tasks/update.html"
    form_class = SubTaskEditForm

    def get_success_url(self):
        return reverse(
            "subtask_detail",
            kwargs=dict(
                task_id=self.object.task.pk, subtask_id=self.object.pk
            ),
        )


class SubTaskDetailView(SubTaskMixin, DetailView):
    template_name = "tasks/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(
            **context,
            form=SubTaskForm,
        )


def task_detail(request, task_id):
    task = TaskModel.objects.get(task_id)
    return render(request, "tasks/detail.html", dict(task=task))
