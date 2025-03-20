from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser, Student, Faculty

@receiver(post_save, sender=MyUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == MyUser.STUDENT:
            Student.objects.create(user=instance)
        elif instance.user_type == MyUser.FACULTY:
            Faculty.objects.create(user=instance)
