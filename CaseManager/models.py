from django.db import models
import datetime
DEFAULT_LONG_CHARFIELD_LENGTH = 90
DEFAULT_SHORT_CHARFIELD_LENGTH = 30

CASE_STATUS_CHOICES = (
    ('NEW', 'New Case'),
    ('APPROVED', 'Case Approved'),
    ('COMPLETED', 'Operation Completed'),
    ('NOT DONE', 'Case Abandoned'),
    ('PAYMENT APPROVED', 'Payment Approved'),
    ('PAYMENT DECLINED', 'Payment Declined'),
    ('PAYMENT REVIEW', 'Payment under review'),
    ('PAYMENT SENT', 'Payment Sent'),
    ('PAYMENT RECEIVED', 'Payment received by surgeon'),
    ('PAYMENT NOT RECEIVED', 'Payment not recieved by surgeon'),
    ('PAYMENT CANCELLED', 'Payment cancelled'),
)

ANASTHETIC_TECHNIQUE_CHOICES = (
    ('GENERAL', 'General Anasthetic'),
    ('IV SEDATION', 'IV Sedation'),
    ('SPINAL', 'Spinal'),
    ('SPINAL + GENERAL', 'Spinal followed by General')
)

DYE_TEST_CHOICES = (
    ('POSITIVE', 'Positive'),
    ('NEGATIVE', 'Negative'),
    ('NOT DONE', 'Not Done'),
)
DRAIN_CHOICES = (
    ('PENROSE', 'Penrose'),
    ('JP', 'JP'),
)


class CaseForm0(models.Model):
    patient= models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    age= models.IntegerField(blank=True)
    ip= models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    surgeon1= models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    surgeon2 = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    theatrenurse = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    wardnurse = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    anasthetic = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH,choices=ANASTHETIC_TECHNIQUE_CHOICES)
    diagnosis = models.TextField()
    operation_performed = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    dye_test = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,choices=DYE_TEST_CHOICES)
    surgery_duration = models.IntegerField(blank=True)
    blood_loss= models.IntegerField(blank=True)
    drains= models.NullBooleanField()
    drain_type= models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,choices=DRAIN_CHOICES)



class Case(models.Model):
    status = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,choices=CASE_STATUS_CHOICES)
    caseform = models.ForeignKey(CaseForm0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.updated_at = datetime.datetime.today()
        return super(Case, self).save(*args, **kwargs)