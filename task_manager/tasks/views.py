from django.db.models import Sum
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)

from tasks.forms import TaskForm, SubTaskFormset, SubTaskForm, TaskEditForm, \
    SubTaskEditForm
from tasks.mixins import TaskMixin, SubTaskMixin
from tasks.models import SubTask


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
            if instance.subtasks.exists():
                subtask_sums = instance.subtasks.aggregate(
                    planned_intensity=Sum("planned_intensity"),
                    actual_completion_time=Sum("actual_completion_time"),
                )
                instance.planned_intensity = (
                        subtask_sums['planned_intensity']
                        + instance.planned_intensity
                )
                instance.actual_completion_time = (
                        subtask_sums['actual_completion_time']
                        + instance.actual_completion_time
                )
                instance.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))


class TaskDeleteView(TaskMixin, DeleteView):
    pass


class TaskUpdateView(TaskMixin, UpdateView):
    template_name = "tasks/update.html"
    form_class = TaskEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse("task_detail", kwargs={"task_id": self.object.pk})


class SubTaskCreateView(SubTaskMixin, CreateView):
    form_class = SubTaskFormset


class SubTaskDeleteView(SubTaskMixin, DeleteView):
    pass


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
