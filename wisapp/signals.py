from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import *


@receiver(post_save, sender=Teacher)
def post_save_user(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f'Пользователь {instance.name} создан')
    else:
        print(f'Баланс пользователя {instance.name} обновлен. Баланс: {instance.acc}')
