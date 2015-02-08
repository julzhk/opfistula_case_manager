from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase, RequestFactory
from CaseEntry.models import Case, PatientRecord
from Surgeon.models import Surgeon
from CaseEntry.views import case_form

def create_a_surgeon_record(name,
                            is_staff=True,
                            is_superuser=False,
                            institution='abc clinic'):
    user = Surgeon.objects.create_user('%s@test.com' % name, 'pass')
    return user


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
            published=True,
            ip='ipcode',
            admission_date='2014-4-14',
            surgery_date='2014-5-24',
        )
        self.adminuser = Surgeon.objects.create_superuser('admin@test.com', 'pass')
        self.case = Case(patientrecord=self.patientrecord, surgeon=self.adminuser)
        self.case.save()
        self.surgeon = self.adminuser
        self.c = Client()


class SimpleCaseNotes(TestFixture):
    def test_make_comment(self):
        c = self.c
        c.login(email='admin@test.com', password='pass')
        response = c.get('/case/1/')
        self.assertEquals(response.status_code, 200)
        response = c.post('/case/1/', {'message': 'testmsg'})
        self.assertEquals(response.status_code, 200)
        response = c.get('/case/1/')
        note1 = response.context['case'].note_set.all()[0]
        self.assertEquals(note1.message, 'testmsg')
        self.assertEquals(note1.commenter, self.adminuser)


class AddCase(TestFixture):
    def test_create_case(self):
        c = self.c
        loginsuccess = c.login(email='admin@test.com', password='pass')
        self.assertTrue(loginsuccess)
        response = c.get('/caselist/')
        case0 = response.context['cases'][0]
        self.assertEquals(response.status_code, 200)
        self.assertEquals(case0, self.case)
        response = c.get('/submitcase/')
        self.assertEquals(response.status_code, 200)
        response = c.post('/submitcase/', {'patient': 'test_patient2'})
        self.assertEquals(response.status_code, 302)
        response = c.get('/caselist/')
        cases = response.context['cases']
        self.assertEquals(cases[0], self.case)
        self.assertEquals(cases[1], Case.objects.get(pk=2))
        self.assertEquals(len(cases), 2)


    def test_cannot_have_caesarean_at_home(self):
        self.patientrecord2 = PatientRecord.objects.create(
            patient='my_new_test_caesarean_home_patient2',
            baby_birth_location='HOME',
            delivery_type='CAESAREAN',
            age=22,
            ip='ipcode2',
            admission_date='2014-4-14',
            surgery_date='2014-5-24',
        )
        self.case2 = Case(patientrecord=self.patientrecord2, surgeon=self.surgeon)
        self.case2.save()
        # this should fail, so we only still have one case extant
        c = self.c
        loginsuccess= c.login(email='admin@test.com', password='pass')
        self.assertTrue(loginsuccess)
        response = c.get('/caselist/')
        cases = response.context['cases']
        self.assertEquals(len(cases), 1)
        self.assertEquals(response.status_code, 200)


class ViewPatientRecord(TestFixture):
    def test_view(self):
        self.c.login(email='admin@test.com', password='pass')
        response = self.c.get('/viewcase/1/')
        self.assertFalse(response.context['form_editable'])
        self.assertTrue('my_new_test_patient' in response.content, response.content)

    def test_cannot_see_unpublished_patients(self):
        self.c.login(email='admin@test.com', password='pass')
        response = self.c.get('/caselist/')
        self.assertEquals(response.status_code, 200)
        cases = response.context['cases']
        self.assertTrue(len(cases) == 1)
        self.case.published = False
        self.case.save()
        response = self.c.get('/caselist/')
        self.assertEquals(response.status_code, 200)
        cases = response.context['cases']
        self.assertTrue(len(cases) == 0, [c.__dict__ for c in cases])


class AdminViews(TestFixture):
    # we have a record & an admin. Lets add another surgeon & give them a patient
    def test_add_two_surgeons_and_patients(self):
        surgeon2 = Surgeon.objects.create_user('user2@test.com', 'pass')
        patientrecord2 = PatientRecord.objects.create(
            patient='my_new_test_patient2',
            age=23,
            published=True,
            ip='ipcode2',
            admission_date='2014-6-14',
            surgery_date='2014-8-24',
        )
        case2 = Case(patientrecord=patientrecord2, surgeon=surgeon2)
        case2.save()
        # now user2 should see just one record, but adminuser should see two
        self.c.login(email='user2@test.com', password='pass')
        response = self.c.get('/caselist/')
        cases = response.context['cases']
        self.assertEquals(len(cases), 1)
        # admin user
        loginsuccess = self.c.login(email='admin@test.com', password='pass')
        self.assertTrue(loginsuccess)
        response = self.c.get('/caselist/')
        cases = response.context['cases']
        print [c.published for c in cases]
        self.assertEquals(len(cases), 2)

    def test_change_status_admin(self):
        """only admins can change a status."""
        self.c.login(email='admin@test.com', password='pass')
        case1 = Case.objects.get(pk=1)
        self.assertEquals(case1.status, 'NEW')
        response = self.c.post('/case/1/', {'status': 'APPROVED'})
        self.assertEquals(response.status_code, 200)
        case1 = Case.objects.get(pk=1)
        self.assertEquals(case1.status, 'APPROVED')

    def test_change_status_non_admin(self):
        """CURRENTLY only admins can change a status.
        # todo : surgeons can change to some statuses, but not others
        """
        self.c.login(email='admin@test.com', password='pass')
        case1 = Case.objects.get(pk=1)
        self.assertEquals(case1.status, 'NEW')
        response = self.c.post('/case/1/', {'status': 'APPROVED'})
        self.assertEquals(response.status_code, 200)
        case1 = Case.objects.get(pk=1)
        self.assertEquals(case1.status, 'APPROVED')

        surgeon2= Surgeon.objects.create_user('user2@test.com', 'pass')
        case1.surgeon = surgeon2
        case1.save()
        # assign the case to surgeon2
        self.assertEquals(case1.surgeon, surgeon2)
        # surgeon2 shouldnt be able to update the status
        self.c.login(email='user2@test.com', password='pass')
        response = self.c.post('/case/1/', {'status': 'COMPLETED'})
        case1 = Case.objects.get(pk=1)
        self.assertNotEqual(case1.status, 'COMPLETED')
        # should still be..
        self.assertEquals(case1.status, 'APPROVED')

    def test_show_all_surgeons_page(self):
        """
        http://127.0.0.1:8000/surgeons/
        """
        self.c.login(email='admin@test.com', password='pass')
        response = self.c.get('/surgeons/')
        self.assertEquals(response.status_code, 200)
        surgeons = response.context['surgeon_list']
        self.assertEquals(len(surgeons), 1)
        create_a_surgeon_record(name='surgeon2')
        response = self.c.get('/surgeons/')
        surgeons = response.context['surgeon_list']
        self.assertEquals(len(surgeons), 2)
        #         page not visible to surgeons, only super admins
        self.c.login(email='surgeon2@test.com', password='pass')
        response = self.c.get('/surgeons/')
        self.assertNotEquals(response.status_code, 200, response.status_code)


class SurgeonView(TestFixture):
    def test_add_new_case_from_surgeon_details_page(self):
        surgeon2 = create_a_surgeon_record('surgeon2')
        c = self.c
        c.login(email='admin@test.com', password='pass')
        response = c.get('/surgeondetails/2/')
        contextsurgeon = response.context['surgeon']
        self.assertEquals(response.status_code, 200)
        self.assertEquals(contextsurgeon, surgeon2)
        addnewcaseresponse = c.get('/submitcase/2/')
        # todo : not implemented yet!
        # contextsurgeon = addnewcaseresponse.context['surgeon']
        # self.assertEquals(contextsurgeon,surgeon2)


class TestLoggedInOnly(TestFixture):
    def test_anonuser_barred(self):
        for endpoint in ['submitcase', 'caselist', 'surgeons', 'caselist', ]:
            response = self.c.get('/%s/' % endpoint)
            print endpoint, ',', response.status_code
            self.assertEqual(response.status_code, 302, '%s, %s' % (endpoint, response.status_code))

    def test_only_admin_can_create_a_surgeon(self):
        c = self.c
        c.login(username='admin', password='pass')
        response = c.post('/surgeon/add/', data={
            'institution': 'new clinic',
            'email': 'new_user@test.com',
            'password1': 'pass',
            'password2': 'pass'
                         ''})
        print response.status_code
        print response.content


class PaginationTests(TestFixture):
    def setUp(self):
        # create admin & a case
        super(PaginationTests, self).setUp()
        for i in range(0, 60):
            p = PatientRecord.objects.create(
                patient='test_patient_%s' % i,
                age=22 + i,
                ip='ipcode',
                admission_date='2014-4-14',
                surgery_date='2014-5-24',
            )
            c = Case(patientrecord=p, surgeon=self.surgeon)
            c.save()

    def test_setup(self):
        cases = Case.objects.all()
        print len(cases)
        self.assertTrue(len(cases) == 61, len(cases))

    def test_pages_cases_list(self):
        c = self.c
        loginok = c.login(email='admin@test.com', password='pass')
        self.assertTrue(loginok)
        response = c.get('/caselist/')
        cases = response.context['cases']

        self.assertTrue(len(cases) < 25)
        self.assertFalse(len(cases) == 61)

    def test_surgeon_paged_list(self):
        for i in range(0, 40):
            u = Surgeon.objects.create_user(
                'admin%s@test.com' % str(i),
                'pass')
        c = self.c
        c.login(email='admin@test.com', password='pass')
        response = c.get('/surgeons/')
        surgeons = response.context['surgeon_list']
        self.assertTrue(len(surgeons) < 25)
        self.assertFalse(len(surgeons) == 39)


class SearchCasesTests(TestFixture):
    def setUp(self):
        # create admin & a case
        super(SearchCasesTests, self).setUp()
        for i in range(0, 60):
            p = PatientRecord.objects.create(
                patient='test_patient_%s' % i,
                age=22 + i,
                ip='ipcode',
                admission_date='2014-4-14',
                surgery_date='2014-5-24',
            )
            c = Case(patientrecord=p, surgeon=self.surgeon)
            c.save()

    def test_adminsearch(self):
        c = self.c
        c.login(email='admin@test.com', password='pass')
        response = c.get('/caselist/?q=1')
        cases = response.context['cases']
        for i in cases:
            self.assertTrue('1' in i.patientrecord.patient, i.patientrecord.patient)

