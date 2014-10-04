from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Surgeon(models.Model):
    class Meta:
        verbose_name = 'Surgeon'

    def __unicode__(self):
        return self.user

    user = models.OneToOneField(User)
    institution = models.CharField(verbose_name='Institution',
                                   blank=True,
                                   max_length=settings.DEFAULT_LONG_CHARFIELD_LENGTH)

    def get_absolute_url(self):
        return reverse('surgeon.views.SurgeonDetailView', args=[str(self.id)])