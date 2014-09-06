from django.test import TestCase
from CaseEntry.models import Case, CaseForm0
from django.core.urlresolvers import resolve
from django.test import TestCase
from CaseEntry.views import case_form

class CaseFormPageTest(TestCase):

    def test_caseform_url_resolves(self):
        # use django's 'resolve' fn to see if the path & view are the same
        found = resolve('/case/')
        self.assertEqual(found.func, case_form)


class SimpleCaseTestCase(TestCase):
    def setUp(self):
        CaseForm0.objects.create(
            patient='new patient',
            age=22,
            ip= 'ipcode',
            surgeon1= 'first surgeon',
            surgeon2 ='second surgeon',
            theatrenurse ='the thea nurse',
            wardnurse ='ward nurse',
            # anasthetic =
            diagnosis = 'diagnosis',
            operation_performed ='op performed',
            # dye_test =
            surgery_duration =60,
            blood_loss=33,
            drains=True,
            drain_type='JP'
)
        newcaseform = CaseForm0.objects.get(patient='new patient')
        Case.objects.create(
            caseform = newcaseform
        )
    def test_case_features(self):
        """Animals that can speak are correctly identified"""
        newcase = Case.objects.get(id=1)
        self.assertEqual(newcase.caseform.patient, 'new patient')

