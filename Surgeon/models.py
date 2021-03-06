from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group


class SurgeonManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        admin = is_staff or is_superuser
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, is_admin=admin, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email=email, password=password,
                                 is_staff=False, is_superuser= False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password,
                                 is_staff=True, is_superuser= True,
                                 **extra_fields)


class Surgeon(AbstractBaseUser):
    """
    Every user is a Surgeon per default, superusers can do more stuff
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    institution = models.CharField(verbose_name='Institution',
                                   blank=True,
                                   max_length=settings.DEFAULT_LONG_CHARFIELD_LENGTH)

    partnership_type = models.CharField(max_length=50,default='',blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = SurgeonManager()

    class Meta:
        verbose_name = 'Surgeon'

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        try:
            return "%(firstinitial)s. %(lastname)s" % \
                   {'firstinitial':self.first_name[0], 'lastname':self.last_name}
        except IndexError:
            return "%s" % (self.last_name or '-')

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def type(self):
        if self.is_superuser:
            return 'Administrator'
        elif self.is_staff:
            return 'Surgeon'
        return 'Non-user'
