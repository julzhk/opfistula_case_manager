from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase, RequestFactory
from CaseEntry.models import Case, PatientRecord
from Surgeon.models import Surgeon
from Surgeon.views import SurgeonCreate

class RegisterNewSurgeonTest(TestCase):
    def setUp(self):
        self.adminuser = Surgeon.objects.create_superuser('admin@test.com', 'pass')
        self.surgeon = self.adminuser
        self.c = Client()
        self.add_surgeon_path = '/surgeon/add/'

    def test_admin_site_paths(self):
        logon = self.c.login(email='admin@test.com', password='pass')
        self.assertTrue(logon)
        self.assertTrue(Surgeon.objects.count() == 1)
        response = self.c.get('/admin/Surgeon/surgeon/')
        self.assertEquals(response.status_code, 200)
        response = self.c.get('/admin/Surgeon/surgeon/add/')
        self.assertEquals(response.status_code, 200)

    def test_create_surgeon(self):
        """
        institution & partnership type is optional
        """
        response = self.c.post(self.add_surgeon_path, {'email': 'test@example.com',
                                                  'password1':'890',
                                                  'password2':'890',
                                                  'first_name':'first',
                                                  'last_name':'last',
                                                  'institution':'aaa centre',
                                                  'partnership_type':'aaa centre'
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Surgeon.objects.count() == 2)

    def test_create_surgeon_fails_nofirstname(self):
        """
        institution & partnership type is optional
        """
        response = self.c.post(self.add_surgeon_path, {'email': 'test@example.com',
                                                  'password1':'890',
                                                  'password2':'890',
                                                  'first_name':'',
                                                  'last_name':'last',
        })
        self.assertTrue(Surgeon.objects.count() == 1)

    def test_create_surgeon_fails_nolastname(self):
        """
        institution & partnership type optional
        """
        response = self.c.post(self.add_surgeon_path, {'email': 'test@example.com',
                                                  'password1':'890',
                                                  'password2':'890',
                                                  'first_name':'fir',
                                                  'last_name':'',
        })
        self.assertTrue(Surgeon.objects.count() == 1)


    def test_create_surgeon_fails_no_match_password(self):
        """
        institution & partnership type is optional
        """
        response = self.c.post(self.add_surgeon_path, {'email': 'test@example.com',
                                                  'password1':'abc',
                                                  'password2':'890',
                                                  'first_name':'first',
                                                  'last_name':'last',
                                                  # 'institution':'aaa centre'
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Surgeon.objects.count() == 1)

    def test_created_surgeon_can_then_login(self):
        response = self.c.post(self.add_surgeon_path, {'email': 'test3@example.com',
                                                  'password1':'aaa',
                                                  'password2':'aaa',
                                                  'first_name':'first',
                                                  'last_name':'last',
                                                  'institution':'aaa centre'
        })
        self.c.login(email='test3@example.com', password='aaa')
        response = self.c.get('/')
        html_content= response.content
        self.assertTrue('Add new case' in html_content)
        self.assertFalse('Create a Surgeon' in html_content)

