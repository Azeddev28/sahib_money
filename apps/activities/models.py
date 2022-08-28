from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel

from apps.activities.choices import ActivityTypes


User = get_user_model()


class Activity(TimeStampedModel):
    action = models.IntegerField(choices=ActivityTypes.CHOICES)
    details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activities')
