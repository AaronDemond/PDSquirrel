import unittest
# Create your tests here.
from pds_v3.my_functions import foo
from pds_v3.models import AppUser,LawSociety
from django.test import Client
from django.contrib.auth.models import User



class BrowseTest(unittest.TestCase):
    def testQuery(self):
        c = Client()
        response = c.get('/browse/',{'subject' : 2})
        self.assertEqual(response.status_code, 200)
