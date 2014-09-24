from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from CaseEntry.models import Case


class Surgeon(models.Model):
    class Meta:
        verbose_name = 'Surgeon'

    user = models.OneToOneField(User)
    institution = models.CharField(verbose_name='Institution',
                                   max_length=settings.DEFAULT_LONG_CHARFIELD_LENGTH)
    cases = models.ForeignKey(Case)