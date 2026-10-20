from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        try:
            send_mail(
                "Activate Your Account",
                f"Click the link to activate your account: {activation_url}",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending activation email: {str(e)}")