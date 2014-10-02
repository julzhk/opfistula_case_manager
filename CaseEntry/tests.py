from django.test import TestCase
from CaseEntry.models import Case, PatientRecord
from Surgeon.models import Surgeon
from django.core.urlresolvers import resolve
from django.test import TestCase
from CaseEntry.views import case_form
from django.contrib.auth.models import User
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import Client

class PatientrecordPageTest(TestCase):
    def test_patientrecord_url_resolves(self):
        # use django's 'resolve' fn to see if the path & view are the same
        found = resolve('/submitcase/')
        self.assertEqual(found.func, case_form)


class SimpleCaseTestCase(TestCase):
    def setUp(self):
        PatientRecord.objects.create(
            patient='my_new_test_patient',
            age=22,
            ip='ipcode',
            admission_date='2014-4-14',
            surgery_date='2014-5-24',
        )
        newpatientrecord = PatientRecord.objects.get(patient='my_new_test_patient')
        Case.objects.create(
            patientrecord=newpatientrecord
        )

    def test_casefrom_creates_a_case(self):
        newcase = Case.objects.get(id=1)
        self.assertEqual(newcase.patientrecord.patient, 'my_new_test_patient')

    def test_casefrom_creates_with_default_status(self):
        newcase = Case.objects.get(id=1)
        self.assertEqual(newcase.status, 'NEW')


class TestFixture(TestCase):

    def setUp(self):
        self.patientrecord = PatientRecord.objects.create(
            patient='my_new_test_patient',
            age=22,
            ip='ipcode',
            admission_date='2014-4-14',
            surgery_date='2014-5-24',
        )

        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()
        self.surgeon = Surgeon.objects.create(
            institution = 'abc',
            user= self.adminuser)
        self.case = Case(patientrecord=self.patientrecord,surgeon=self.surgeon)
        self.case.save()
        self.c = Client()

class SimpleCaseNotes(TestFixture):
    def test_make_comment(self):

        c = self.c
        c.login(username='admin', password='pass')
        response = c.get('/case/1/')
        self.assertEquals(response.status_code,200)
        response = c.post('/case/1/',{'message':'testmsg'})
        self.assertEquals(response.status_code,200)
        response = c.get('/case/1/')
        note1 = response.context['case'].note_set.all()[0]
        self.assertEquals(note1.message,'testmsg')
        self.assertEquals(note1.commenter,self.adminuser)

class AddCase(TestFixture):
    def test_create_case(self):
        c = self.c
        c.login(username='admin', password='pass')
        response = c.get('/caselist/')
        case0 = response.context['cases'][0]
        self.assertEquals(response.status_code,200)
        self.assertEquals(case0,self.case)
        response = c.get('/submitcase/')
        self.assertEquals(response.status_code,200)
        response = c.post('/submitcase/',{'patient':'test_patient2'})
        self.assertEquals(response.status_code,302)
        response = c.get('/caselist/')
        cases = response.context['cases']
        self.assertEquals(cases[0],self.case)
        self.assertEquals(cases[1],Case.objects.get(pk=2))
        self.assertEquals(len(cases), 2)

class ViewPatientRecord(TestFixture):

    def test_view(self):
        self.c.login(username='admin', password='pass')
        response = self.c.get('/viewcase/1/')
        self.assertFalse(response.context['form_editable'])
        self.assertTrue('my_new_test_patient' in response.content,response.content)