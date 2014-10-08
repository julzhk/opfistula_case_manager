from django.db import models

__author__ = 'julz'


class TimeStampedModel(models.Model):
    """
    Abstract Base Class Model providing self-updating
    created & modified fields
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True