from django.db.models import Count, Q
from django.shortcuts import render, redirect
from tasks.forms import TaskDetailModelForm, TaskModelForm
from tasks.models import Task, TaskDetails

def home(request):
    return render(request, "home.html")

def manager_dashboard(request, status=None):
    valid_statuses = {choice[0] for choice in Task.STATUS_CHOICES}
    if status and status not in valid_statuses:
        status = None

    tasks = (
        Task.objects.select_related("project", "task_details")
        .prefetch_related("assign_to")
        .order_by("-created_at")
    )
    if status:
        tasks = tasks.filter(status=status)
    stats = Task.objects.aggregate(
        total_tasks=Count("id"),
        in_progress=Count("id", filter=Q(status=Task.IN_PROGRESS)),
        completed=Count("id", filter=Q(status=Task.COMPLETED)),
        pending=Count("id", filter=Q(status=Task.PENDING)),
        high_priority_in_progress=Count(
            "id",
            filter=Q(
                status=Task.IN_PROGRESS,
                task_details__priority__in=[TaskDetails.HIGH, TaskDetails.URGENT],
            ),
        ),
    )
    total_tasks = stats["total_tasks"]
    completed = stats["completed"]
    success_rate = round((completed / total_tasks) * 100) if total_tasks else 0

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "in_progress": stats["in_progress"],
        "completed": completed,
        "pending": stats["pending"],
        "high_priority_in_progress": stats["high_priority_in_progress"],
        "success_rate": success_rate,
        "current_status": status,
    }
    return render(request, "dashboard/manager_dashboard.html", context)

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def task_form(request):
    form = TaskModelForm()
    detail_form = TaskDetailModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        detail_form = TaskDetailModelForm(request.POST)

        if form.is_valid() and detail_form.is_valid():
            task = form.save()
            task_details = detail_form.save(commit=False) # Create Obj but not save to db

            task_details.task = task
            assigned = task.assign_to.first()
            task_details.assign_to = assigned.name if assigned else ""
            task_details.save()

            return redirect("manager_dashboard")

    return render(
        request,
        "task_form.html",
        {"form": form, "detail_form": detail_form},
    )