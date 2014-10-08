from Core.models import TimeStampedModel
from django.db import models
from django.utils import timezone
from django.conf import settings
from CaseEntry.models import Case
from django.contrib.auth.models import User


class Note(TimeStampedModel):
    message = models.TextField()
    case = models.ForeignKey(Case,null=True)
    commenter = models.ForeignKey(User, null=True, blank=True)