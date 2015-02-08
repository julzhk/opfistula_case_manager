from Core.models import TimeStampedModel
from django.forms import ModelForm
from django.db import models
from django.conf import settings

from Core.models import TimeStampedModel
from Surgeon.models import Surgeon
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

DEFAULT_LONG_CHARFIELD_LENGTH = settings.DEFAULT_LONG_CHARFIELD_LENGTH
DEFAULT_SHORT_CHARFIELD_LENGTH = settings.DEFAULT_SHORT_CHARFIELD_LENGTH

MARITAL_STATUS_CHOICES = (
    ('MARRIED', 'Married'),
    ('DIVORCED', 'Widowed'),
    ('REMARRIED', 'Remarried (with Fistula)'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

SOCIAL_STATUS_CHOICES = (
    ('WITH_HUSBAND', 'Living with Husband'),
    ('WITH_FAMILY', 'Living with Family'),
    ('ALONE', 'Living Alone'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

BIRTH_LOCATION_CHOICES = (
    ('HOME', 'Home'),
    ('HOSPITAL', 'Hospital'),
    ('HEALTH CENTER', 'Health Center'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

DELIVERY_CHOICES = (
    ('VAGINAL', 'Vaginal'),
    ('INSTRUMENTAL', 'Instrumental'),
    ('CAESAREAN', 'Caesarean'),
    ('CAESAREAN_HYSTERECTOMY', 'Caesarean Hysterectomy'),
    ('DESTRUCTIVE_CRANIOTOMY', 'Destructive Craniotomy'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)
DELIVERY_OUTCOME_CHOICES = (
    ('LIVEBIRTH', 'Live birth'),
    ('STILLBIRTH', 'Stillbirth'),
    ('EARLY_NEONATAL_DEATH', 'Early Neonatal Death'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

CAUSE_OF_FISTALA_CHOICES = (
    ('OBSTETRIC', 'Obstetric'),
    ('CAESAREAN-RELATED', 'Caesarean related'),
    ('HYSTERECTOMY', 'Hysterectomy'),
    ('OTHER', 'Other reason'),
    ('UNKNOWN', 'Unknown'),
)

URINE_LEAK_FREQUENCY_CHOICES = (
    ('NEVER', 'Never'),
    ('ONCE_WEEKLY_OR_LESS', 'Once a week or less'),
    ('2-3_TIMES_WEEKLY', 'Two or three times a week'),
    ('DAILY', 'Once a day'),
    ('SEVERAL_TIMES_PER_DAY', 'Several Times per day'),
    ('CONTINUOUSLY', 'All the time'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

URINE_LEAK_AMOUNT_CHOICES = (
    ('NONE', 'None'),
    ('SMALL', 'A small amount'),
    ('MODERATE', 'A moderate amount'),
    ('LARGE', 'A large amount'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

URINE_LEAK_ANNOYANCE_CHOICES = [
                                   (0, ' 0 : Not at all'),
                               ] + [(r, str(r)) for r in range(1, 10)] + [
                                   (10, ' 10 : A great deal'),
                                   ('UNKNOWN/OTHER', 'Unknown/Other'),
                                   ]

CASE_STATUS_CHOICES = (
    ('NEW', 'New Case'),
    ('APPROVED', 'Case Approved'),
    ('COMPLETED', 'Operation Completed'),
    ('NOT DONE', 'Case Abandoned'),
    ('PAYMENT APPROVED', 'Payment Approved'),
    ('PAYMENT DECLINED', 'Payment Declined'),
    ('PAYMENT REVIEW', 'Payment under review'),
    ('PAYMENT SENT', 'Payment Sent'),
    ('PAYMENT RECEIVED', 'Payment received by Surgeon'),
    ('PAYMENT NOT RECEIVED', 'Payment not received by Surgeon'),
    ('PAYMENT CANCELLED', 'Payment cancelled'),
)

ANASTHETIC_TECHNIQUE_CHOICES = (
    ('GENERAL', 'General Anasthetic'),
    ('IV SEDATION', 'IV Sedation'),
    ('SPINAL', 'Spinal'),
    ('SPINAL + GENERAL', 'Spinal followed by General'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

DYE_TEST_CHOICES = (
    ('POSITIVE', 'Positive'),
    ('NEGATIVE', 'Negative'),
    ('NOT DONE', 'Not Done'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)
DRAIN_CHOICES = (
    ('PENROSE', 'Penrose'),
    ('JP', 'JP'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

LAST_PERIOD_DATE_ALTERNATIVE_CHOICES = (
    ("NOT APPLICABLE","Not Applicable"),
    ("MENOPAUSE",'Menopause'),
    ("AMENORREHEA","Amenorrhea"),
    ('NOT MENSTRUATING',"Not menstruating"),
    ('UNKNOWN/OTHER', 'Unknown/Other'),
)

# How long was the labor? - this one is usually answered in "hours"
# up to about 48 or maybe 72 hours.
# After that, the answers switch to "days".
# They go up to seven days (longest I've seen, anyway).
#  We don't have a standard unit measurement for this - neither hours nor days -
# so I always just write in the entire answer to keep the data valid.
#  Is there a way you can allocate for hours and days both?  Or standardize it and use days?


LABOR_DURATION_CHOICES = [
    (6,'less than 6 Hours'),
    (12,'6-12 Hours'),
    (18,'12-18 Hours'),
    (24,'18-24 Hours'),
    (24+12,'1-1.5 Days'),
    (24+24,'1.5-2 Days'),
    (24+24+12,'2-2.5 Days'),
    (24+24+24,'2.5-3 Days'),
    (24+24+24+12,'3-3.5 Days'),
    (24+24+24+24,'3.5-4 Days'),
    (24*5,'4-5 Days'),
    (24*6,'5-6 Days'),
    (24*7,'6-7 Days'),
    (24*8,'7-8 Days or more'),
    ('UNKNOWN/OTHER', 'Unknown/Other'),

]

class PatientRecord(TimeStampedModel):
    class Meta:
        verbose_name = 'Patient Record Form'

    patient = models.CharField(verbose_name='Patient Name',
                               max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    age = models.IntegerField(verbose_name='Patient Age',
                              null=True,
                              default=0,
                              blank=True)
    ip = models.CharField(verbose_name='IP Code',
                          blank=True,
                          max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    admission_date = models.DateField(verbose_name='Date of Admission',
                                      null=True,
                                      blank=True)
    surgery_date = models.DateField(verbose_name='Date of Surgery',
                                    blank=True,
                                    null=True)
    discharge_date = models.DateField(verbose_name='Date of Discharge',
                                      blank=True,
                                      null=True)

    height = models.IntegerField(verbose_name='Height in cm', blank=True, null=True)
    weight = models.IntegerField(verbose_name='Weight in kg', blank=True, null=True)
    menache_age = models.IntegerField(verbose_name='Age at Menache',
                                      blank=True, null=True, help_text='Leave blank if unknown')
    main_telephone = models.CharField(verbose_name='Main Telephone number',
                                      blank=True,
                                      max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    other_telephone = models.TextField(verbose_name='Other Telephone numbers',
                                       blank=True, null=True)
    address = models.TextField(verbose_name='Patient Address',
                               blank=True)
    country = models.TextField(verbose_name='Patient Country',
                               blank=True)
    regular_period = models.NullBooleanField(verbose_name="Are Patient's Periods Regular?",
                                             blank=True)
    last_period = models.DateField(verbose_name="Date of last Period Date",
                                   blank=True, null=True)
    last_period_note = models.CharField(verbose_name="If no last period date,please explain:",
                                   max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                   choices=LAST_PERIOD_DATE_ALTERNATIVE_CHOICES,
                                   blank=True, null=True,help_text="If last period date ")
    marital_status = models.CharField(verbose_name='Marital Status',
                                      max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                      choices=MARITAL_STATUS_CHOICES,
                                      blank=True)
    social_status = models.CharField(verbose_name='Social Status',
                                     max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                     blank=True,
                                     choices=SOCIAL_STATUS_CHOICES)
    first_pregnancy_age = models.IntegerField(verbose_name='Age at first Pregnancy',
                                              blank=True,
                                              null=True,
                                              help_text='yrs')
    first_pregnancy_fathers_age = models.IntegerField(verbose_name='Age of Father at first Pregnancy',
                                                      blank=True, null=True,
                                                      help_text='(in years.) Leave blank if unknown')
    pregnancy_count = models.IntegerField(verbose_name='Number of Pregnancies',
                                          null=True,
                                          blank=True)
    living_children_count = models.IntegerField(verbose_name='Number of Living Children',
                                                null=True,
                                                blank=True)
    stillbirth_count = models.IntegerField(verbose_name='Number of Stillbirths',
                                           null=True,
                                           blank=True)
    early_neonatal_death_count = models.IntegerField(verbose_name='Number of Early Neonatal Deaths',
                                                     null=True,
                                                     blank=True)
    last_pregnancy_age = models.IntegerField(verbose_name='Age at last Pregnancy',
                                             null=True,
                                             blank=True,
                                             help_text='yrs')
    treatment_center_travel = models.TextField(verbose_name='How did the Patient get to the treatment center?',
                                               null=True,
                                               blank=True, )
    treatment_center_travel_cost = models.CharField(
        verbose_name='How much did the journey to the treatment center cost?',
        blank=True,
        max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    age_fistula_started = models.IntegerField(verbose_name='Age when the Fistula occurred',
                                              null=True,
                                              blank=True)
    labor_duration = models.IntegerField(verbose_name='How long was the labor?',
                                         null=True,
                                         blank=True,
                                         choices=LABOR_DURATION_CHOICES,
                                         help_text='hrs')
    baby_birth_location = models.CharField(verbose_name='Where was the baby born?',
                                           blank=True,
                                           max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                           choices=BIRTH_LOCATION_CHOICES)
    delivery_type = models.CharField(verbose_name='What type of Delivery?',
                                     blank=True,
                                     max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                     choices=DELIVERY_CHOICES)
    delivery_outcome = models.CharField(verbose_name='Delivery Outcome?',
                                        blank=True,
                                        max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                        choices=DELIVERY_OUTCOME_CHOICES)
    fistula_cause = models.CharField(verbose_name='Cause of Fistula?',
                                     max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                     blank=True,
                                     choices=CAUSE_OF_FISTALA_CHOICES)
    urine_leak_frequency = models.CharField(verbose_name='How often do you leak urine?',
                                            help_text='(Ask the patient)',
                                            blank=True,
                                            max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                            choices=URINE_LEAK_FREQUENCY_CHOICES)
    urine_leak_amount = models.CharField(verbose_name='How much urine do you usually leak?',
                                         help_text='(Ask the patient)',
                                         blank=True,
                                         max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                         choices=URINE_LEAK_AMOUNT_CHOICES)
    urine_leak_interference = models.IntegerField(
        verbose_name='How much does the urine leaking interfere with your daily life?',
        help_text='(Ask the patient)',
        null=True,
        blank=True,
        choices=URINE_LEAK_ANNOYANCE_CHOICES)

    def __unicode__(self):
        return "%s" % self.patient

    def clean(self):
        if self.baby_birth_location =='HOME' and 'CAESAREAN' in self.delivery_type:
            raise ValidationError(
              'Cannot have %(type)s at %(location)s',
                code='invalid',
                params={'location': self.get_baby_birth_location_display(),'type':self.get_delivery_type_display()},
            )


class Case(TimeStampedModel):
    status = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                              choices=CASE_STATUS_CHOICES,
                              default=CASE_STATUS_CHOICES[0][0])
    patientrecord = models.ForeignKey(PatientRecord)
    surgeon = models.ForeignKey(Surgeon, blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.patientrecord.patient)


class PatientRecordForm(ModelForm):
    class Meta:
        model = PatientRecord
        exclude = ['published',]


class PatientRecordReadOnlyForm(ModelForm):
    class Meta:
        model = PatientRecord
        exclude = ['published', ]

    def __init__(self, *args, **kwargs):
        super(PatientRecordReadOnlyForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for fieldwidget in self.fields:
                self.fields[fieldwidget].widget.attrs['readonly'] = True
                self.fields[fieldwidget].widget.attrs['disabled'] = True
