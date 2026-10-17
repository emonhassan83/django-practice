from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed")
    ]

    project = models.ForeignKey("Project", on_delete=models.CASCADE, default = 1)
    assign_to = models.ManyToManyField(Employee, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Details for task {self.task.title}"
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
