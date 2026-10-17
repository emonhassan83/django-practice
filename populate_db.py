import os
import random
from datetime import timedelta
from django.utils import timezone

# 1. Django Environment Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')

import django
django.setup()

from django.db import transaction
from faker import Faker
from tasks.models import Employee, Project, Task, TaskDetails

fake = Faker()


def populate_employees(count=15):
    """Employee মডেলের ফেক ডেটা তৈরি করে"""
    print(f"Creating {count} employees...")
    employees = []
    for _ in range(count):
        employee = Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        employees.append(employee)
    print(f"Successfully created {len(employees)} employees.")
    return employees


def populate_projects(count=5):
    """Project মডেলের ফেক ডেটা তৈরি করে"""
    print(f"Creating {count} projects...")
    projects = []
    today = timezone.now().date()
    for _ in range(count):
        # প্রোজেক্টের শুরুর তারিখ (গত ৬০ দিনের যেকোনো দিন)
        start_date = today - timedelta(days=random.randint(1, 60))
        # শেষ তারিখ শুরুর তারিখের ৩০ থেকে ১৮০ দিন পর
        end_date = start_date + timedelta(days=random.randint(30, 180))

        project = Project.objects.create(
            name=f"{fake.bs().title()} Project",
            description=fake.paragraph(nb_sentences=3),
            start_date=start_date,
            end_date=end_date
        )
        projects.append(project)
    print(f"Successfully created {len(projects)} projects.")
    return projects


def populate_tasks_and_details(projects, employees, count=25):
    """Task এবং এর সম্পর্কিত TaskDetails তৈরি করে"""
    print(f"Creating {count} tasks with TaskDetails...")
    today = timezone.now().date()
    status_choices = [Task.PENDING, Task.IN_PROGRESS, Task.COMPLETED]
    priority_choices = [
        TaskDetails.LOW,
        TaskDetails.MEDIUM,
        TaskDetails.HIGH,
        TaskDetails.URGENT
    ]

    tasks = []
    for _ in range(count):
        chosen_project = random.choice(projects)
        status = random.choice(status_choices)
        is_completed = (status == Task.COMPLETED)

        # ডিউ ডেট
        due_date = today + timedelta(days=random.randint(-15, 45))

        task = Task.objects.create(
            project=chosen_project,
            title=fake.sentence(nb_words=6).rstrip('.'),
            description=fake.text(max_nb_chars=300),
            due_date=due_date,
            status=status,
            is_completed=is_completed
        )

        # Many-to-Many: টাস্কে ১ থেকে ৩ জন Employee অ্যাসাইন করা
        assigned_employees = random.sample(employees, k=random.randint(1, min(3, len(employees))))
        task.assign_to.set(assigned_employees)

        # One-to-One: TaskDetails তৈরি করা
        primary_assignee = assigned_employees[0].name if assigned_employees else fake.name()
        TaskDetails.objects.create(
            task=task,
            assign_to=primary_assignee,
            priority=random.choice(priority_choices),
            note=fake.paragraph(nb_sentences=2) if random.choice([True, False]) else None
        )

        tasks.append(task)

    print(f"Successfully created {len(tasks)} tasks and their details.")
    return tasks


def run(num_employees=15, num_projects=5, num_tasks=25):
    """সম্পূর্ণ ডাটাবেজ পপুলেট করার প্রধান ফাংশন"""
    print("=" * 50)
    print("Starting database population...")
    print("=" * 50)

    with transaction.atomic():
        employees = populate_employees(num_employees)
        projects = populate_projects(num_projects)
        tasks = populate_tasks_and_details(projects, employees, num_tasks)

    print("=" * 50)
    print("Database population completed successfully!")
    print(f"Summary:")
    print(f" - Total Employees: {Employee.objects.count()}")
    print(f" - Total Projects:  {Project.objects.count()}")
    print(f" - Total Tasks:     {Task.objects.count()}")
    print(f" - Task Details:    {TaskDetails.objects.count()}")
    print("=" * 50)


if __name__ == '__main__':
    run()
