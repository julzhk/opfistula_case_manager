from django.test import TestCase
from CaseEntry.models import Case, CaseForm
from django.core.urlresolvers import resolve
from django.test import TestCase
from CaseEntry.views import case_form
import datetime

class CaseFormPageTest(TestCase):

    def test_caseform_url_resolves(self):
        # use django's 'resolve' fn to see if the path & view are the same
        found = resolve('/case/')
        self.assertEqual(found.func, case_form)


class SimpleCaseTestCase(TestCase):
    def setUp(self):
        CaseForm.objects.create(
            patient='new patient',
            age=22,
            ip= 'ipcode',
            admission_date= '2014-4-14',
            surgery_date= '2014-5-24',
            surgeon= 'first surgeon',
)
        newcaseform = CaseForm.objects.get(patient='new patient')
        Case.objects.create(
            caseform = newcaseform
        )

    def test_casefrom_creates_a_case(self):
        newcase = Case.objects.get(id=1)
        self.assertEqual(newcase.caseform.patient, 'new patient')

    def test_casefrom_creates_with_default_status(self):
        newcase = Case.objects.get(id=1)
        self.assertEqual(newcase.status, 'NEW')


