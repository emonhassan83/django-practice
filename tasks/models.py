from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default = 1)
    assign_to = models.ManyToManyField(Employee, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskDetails(models.Model):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    URGENT = "urgent"
    PRIORITY_OPTIONS = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (URGENT, "Urgent"),
    )
    
    assign_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_OPTIONS, default=MEDIUM)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="task_details")
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
