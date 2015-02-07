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
        logon = self.c.login(email='admin@test.com', password='pass')
        self.assertTrue(logon)
        self.assertTrue(Surgeon.objects.count() == 1)
        self.add_surgeon_path = '/surgeon/add/'
        response = self.c.get(self.add_surgeon_path)
        self.assertEquals(response.status_code, 200)

    def test_create_surgeon(self):
        """
        institution is optional
        """
        response = self.c.post(self.add_surgeon_path, {'email': 'test@example.com',
                                                  'password1':'890',
                                                  'password2':'890',
                                                  'first_name':'first',
                                                  'last_name':'last',
                                                  # 'institution':'aaa centre'
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Surgeon.objects.count() == 2)

    def test_create_surgeon_fails_nofirstname(self):
        """
        institution is optional
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
        institution is optional
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
        institution is optional
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
