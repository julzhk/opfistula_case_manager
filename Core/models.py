from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models

__author__ = 'julz'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(published=True)


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

    objects = models.Manager()
    published_objects = PublishedManager()


def paginate(qs, page):
    paginator = Paginator(qs, settings.PAGE_SIZE)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)