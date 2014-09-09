from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MedicalUserManager(BaseUserManager):

    def create_user(self,email, organization=None,password=None):
        """
        create and save a user with the given personal details
        :param email:
        :param organization:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not organization:
            raise ValueError('Users must have an organization')
        user = self.model(
            email = MedicalUserManager.normalize_email(email),
            organization=organization,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,organization=None,password=None):

        user = self.create_user(email,password=password,organization=organization)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    karma = models.PositiveIntegerField(_("karma"),default=0,blank=True)

class MedicalUser(AbstractUser):
    organization=models.CharField(max_length=255)
    REQUIRED_FIELDS = ['organization',]
    is_admin= models.BooleanField(default=False)

    objects=MedicalUserManager()

    def get_full_name(self):
        return "%s (from %s)" %(self.email, self.organization)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email


