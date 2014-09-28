from django.db import models
from django.utils import timezone
from django.conf import settings
from CaseEntry.models import Case
from django.contrib.auth.models import User


class Note(models.Model):
    message = models.TextField()
    case = models.ForeignKey(Case)
    commenter = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()