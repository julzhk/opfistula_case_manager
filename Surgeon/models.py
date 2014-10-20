from Core.models import TimeStampedModel
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse


class Surgeon(TimeStampedModel):
    class Meta:
        verbose_name = 'Surgeon'

    def __unicode__(self):
        try:
            return str(self.user)
        except AttributeError:
            return 'none'

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    institution = models.CharField(verbose_name='Institution',
                                   blank=True,
                                   max_length=settings.DEFAULT_LONG_CHARFIELD_LENGTH)


    def type(self):
        if self.user.is_superuser:
            return 'Administrator'
        elif self.user.is_staff:
            return 'Surgeon'
        return 'Non-user'