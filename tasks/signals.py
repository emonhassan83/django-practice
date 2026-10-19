from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task, TaskDetails

from django.conf import settings

# signal function
@receiver(m2m_changed, sender=Task.assign_to.through)
def notify_employee_task_created(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assign_to.all() if emp.email]
        if assigned_emails:
            send_mail(
                f"Task: {instance.title}",
                f"New task has been assigned to you. Due date: {instance.due_date}",
                settings.DEFAULT_FROM_EMAIL,
                assigned_emails,
                fail_silently=False,
            )


@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if hasattr(instance, 'task_details') and instance.task_details:
        instance.task_details.delete()
        print("Task details deleted.")