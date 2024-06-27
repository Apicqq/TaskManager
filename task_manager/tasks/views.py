from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)

from tasks.forms import TaskForm, SubTaskFormset, SubTaskForm, TaskEditForm, \
    SubTaskEditForm, SubTaskInlineFormset
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
            formset=SubTaskFormset(queryset=SubTask.objects.none()),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = SubTaskFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            instance = form.save()
            for subtask_form in formset:
                subtask = subtask_form.save(commit=False)
                subtask.task = instance
                subtask.save()
            calculate_task_values(instance)
            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))


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
            formset=SubTaskInlineFormset(
                instance=self.get_object(),
            ),
        )

    @atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = SubTaskInlineFormset(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            calculate_task_values(self.object)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})


class SubTaskCreateView(SubTaskMixin, CreateView):
    form_class = SubTaskFormset


class SubTaskDeleteView(SubTaskMixin, DeleteView):
    success_url = reverse_lazy("task_list")


class SubTaskUpdateView(SubTaskMixin, UpdateView):
    template_name = "tasks/update.html"
    form_class = SubTaskEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse(
            "subtask_detail", kwargs=dict(
                task_id=self.object.task.pk,
                subtask_id=self.object.pk
            )
        )


class SubTaskDetailView(SubTaskMixin, DetailView):
    template_name = "tasks/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubTaskForm

        return context


def add_task(request):
    if request.method == "POST":
        formset = SubTaskFormset(request.POST,
                                 prefix=request.POST.get("prefix"))
        if formset.is_valid():
            formset.save()
            form = formset.forms
            return JsonResponse({"form": form.as_p()})
    else:
        formset = SubTaskFormset(prefix=request.GET.get('prefix'),
                                 queryset=SubTask.objects.none())
        return JsonResponse({"formset": formset})


def task_view(request, task_id, subtask_id):
    if request.is_ajax():
        task_content = f"Content for Subtask {subtask_id} of Task {task_id}"

        return JsonResponse({"content": task_content})
