from datetime import datetime, time

from django.shortcuts import render, redirect
from django.utils import timezone
from tasks.forms import TaskForm
from tasks.models import Employee, Task, TaskDetails, Project

def home(request):
    return render(request, "home.html")


def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def task_form(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)

    if request.method == "POST":
        form = TaskForm(request.POST, employees=employees)
        # print(form.errors)

        if form.is_valid():
            data = form.cleaned_data
            title = data.get("title")
            description = data.get("description")
            due_date = data.get("due_date")
            assign_to = data.get("assign_to")
            priority = data.get("priority")
            
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date
            )
            TaskDetails.objects.create(task=task, priority=priority)

            # assign the task to the employees
            for emp_id in assign_to:
                employee = Employee.objects.get(id=emp_id)
                task.assign_to.add(employee)

            return redirect("manager_dashboard")
    return render(request, "task_form.html", {"form": form})