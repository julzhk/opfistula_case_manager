from django.db import models
import datetime
from django.forms import ModelForm


DEFAULT_LONG_CHARFIELD_LENGTH = 90
DEFAULT_SHORT_CHARFIELD_LENGTH = 30

MARITAL_STATUS_CHOICES =(
    ('MARRIED', 'Married'),
    ('DIVORCED', 'Widowed'),
    ('REMARRIED', 'Remarried (with Fistula)'),
)

SOCIAL_STATUS_CHOICES=(
    ('WITH_HUSBAND', 'Living with Husband'),
    ('WITH_FAMILY', 'Living with Family'),
    ('ALONE', 'Living Alone'),
)

BIRTH_LOCATION_CHOICES = (
    ('HOME','Home'),
    ('HOSPITAL','Hospital'),
    ('HEALTH CENTER', 'Health Center'),
)

DELIVERY_CHOICES = (
    ('VAGINAL','Vaginal'),
    ('INSTRUMENTAL','Instrumental'),
    ('CAESAREAN','Caesarean'),
    ('CAESAREAN_HYSTERECTOMY','Caesarean Hysterectomy'),
    ('DESTRUCTIVE_CRANIOTOMY','Destructive Craniotomy'),
)
DELIVERY_OUTCOME_CHOICES = (
    ('LIVEBIRTH','Live birth'),
    ('STILLBIRTH','Stillbirth'),
    ('EARLY_NEONATAL_DEATH','Early Neonatal Death')
)

CAUSE_OF_FISTALA_CHOICES = (
    ('OBSTETRIC','Obstetric'),
    ('CAESAREAN-RELATED','Caesarean related'),
    ('HYSTERECTOMY','Hysterectomy'),
    ('OTHER','Other reason'),
)

URINE_LEAK_FREQUENCY_CHOICES = (
    ('NEVER','Never'),
    ('ONCE_WEEKLY_OR_LESS','Once a week or less'),
    ('2-3_TIMES_WEEKLY','Two or three times a week'),
    ('DAILY','Once a day'),
    ('SEVERAL_TIMES_PER_DAY','Several Times per day'),
    ('CONTINUOUSLY','All the time'),
)

URINE_LEAK_AMOUNT_CHOICES= (
    ('NONE','None'),
    ('SMALL','A small amount'),
    ('MODERATE','A moderate amount'),
    ('LARGE','A large amount'),
)

URINE_LEAK_ANNOYANCE_CHOICES = [
    (0,' 0 : Not at all'),
] + [(r,str(r)) for r in range(1,10)] + [
    (10,' 10 : A great deal')]


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
    patient= models.CharField(verbose_name='Patient Name',
                              max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    age= models.IntegerField(verbose_name='Patient Age',
                             blank=True)
    ip= models.CharField(verbose_name='IP Code',
                         max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    surgeon= models.CharField(verbose_name='Surgeon',
                               max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    admission_date = models.DateField(verbose_name='Date of Admission')
    surgery_date = models.DateField(verbose_name='Date of Surgery')
    discharge_date = models.DateField(verbose_name='Date of Discharge')

    height= models.IntegerField(verbose_name='Height in cm')
    weight= models.IntegerField(verbose_name='Weight in kg')
    menache_age= models.IntegerField(verbose_name='Age at Menache',
                                     blank=True)
    main_telephone= models.CharField(verbose_name='Main Telephone number',
                                max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    other_telephone= models.TextField(verbose_name='Other Telephone numbers')
    address= models.TextField(verbose_name='Patient Address')
    regular_period= models.NullBooleanField(verbose_name="Are Patient's Periods Regular?")
    last_period= models.DateField(verbose_name="Date of last Period Date")
    marital_status = models.CharField(verbose_name='Marital Status',
                                      max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                      choices=MARITAL_STATUS_CHOICES)
    social_status =  models.CharField(verbose_name='Social Status',
                                      max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                      choices=SOCIAL_STATUS_CHOICES)
    first_pregnancy_age =  models.IntegerField(verbose_name='Age at first Pregnancy',
                                               blank=True,
                                               help_text='yrs')
    first_pregnancy_fathers_age =  models.IntegerField(verbose_name='Age of Father at first Pregnancy',
                                               blank=True,
                                               help_text='yrs')
    pregnancy_count = models.IntegerField(verbose_name='Number of Pregnancies',
                                               blank=True)
    living_children_count = models.IntegerField(verbose_name='Number of Living Children',
                                               blank=True)
    stillbirth_count = models.IntegerField(verbose_name='Number of Stillbirths',
                                               blank=True)
    early_neonatal_death_count = models.IntegerField(verbose_name='Number of Early Neonatal Deaths',
                                               blank=True)
    last_pregnancy_age =  models.IntegerField(verbose_name='Age at last Pregnancy',
                                               blank=True,
                                               help_text='yrs')
    treatment_center_travel = models.TextField(verbose_name='How did the Patient get to the treatment center?')
    treatment_center_travel_cost = models.CharField(verbose_name='How much did the journey to the treatment center cost?',
                                                    max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    age_fistula_started= models.IntegerField(verbose_name='Age when the Fistula occurred',
                                             blank=True)
    labor_duration= models.IntegerField(verbose_name='How long was the labor?',
                                     help_text='hrs')
    baby_birth_location= models.CharField(verbose_name='Where was the baby born?',
                                          max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                          choices=BIRTH_LOCATION_CHOICES)
    delivery_type= models.CharField(verbose_name='What type of Delivery?',
                                        max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                          choices=DELIVERY_CHOICES)
    delivery_outcome= models.CharField(verbose_name='Delivery Outcome?',
                                       max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                          choices=DELIVERY_OUTCOME_CHOICES)
    fistula_cause= models.CharField(verbose_name='Cause of Fistula?',
                                    max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                          choices=CAUSE_OF_FISTALA_CHOICES)
    urine_leak_frequency= models.CharField(verbose_name='How often do you leak urine?',
                                           help_text='(Ask the patient)',
                                           max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                           choices=URINE_LEAK_FREQUENCY_CHOICES)
    urine_leak_amount= models.CharField(verbose_name='How much urine do you usually leak?',
                                           help_text='(Ask the patient)',
                                           max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,
                                           choices=URINE_LEAK_AMOUNT_CHOICES)
    urine_leak_interference= models.IntegerField(verbose_name='How much does the urine leaking interfere with your daily life?',
                                           help_text='(Ask the patient)',
                                           blank=True,
                                           choices=URINE_LEAK_ANNOYANCE_CHOICES)




    # wardnurse = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH)
    # anasthetic = models.CharField(max_length=DEFAULT_LONG_CHARFIELD_LENGTH,choices=ANASTHETIC_TECHNIQUE_CHOICES)
    # diagnosis = models.TextField()
    # operation_performed = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH)
    # dye_test = models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,choices=DYE_TEST_CHOICES)
    # surgery_duration = models.IntegerField(blank=True)
    # blood_loss= models.IntegerField(blank=True)
    # drains= models.NullBooleanField()
    # drain_type= models.CharField(max_length=DEFAULT_SHORT_CHARFIELD_LENGTH,choices=DRAIN_CHOICES)



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




class CaseForm(ModelForm):
    class Meta:
        model = CaseForm0
        fields = '__all__'