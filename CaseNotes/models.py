from django.db import models
from django.conf import settings

from Core.models import TimeStampedModel
from CaseEntry.models import Case


class Note(TimeStampedModel):
    message = models.TextField()
    case = models.ForeignKey(Case, null=True)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)