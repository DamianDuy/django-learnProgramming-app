from django.test import TestCase
from .models import *

# Create your tests here.

class TermsAndConditionsTest(TestCase):
    def setUp(self) -> None:
        TermsAndContionsPage1 = Terms_And_Conditions.objects.create(content="test content")
        #return super().setUp()
    def test_about_content(self):
        TermsAndCondtionsPage = Terms_And_Conditions.objects.get(id=1)
        self.assertEqual(TermsAndCondtionsPage.content, "test content")
        self.assertNotEqual(TermsAndCondtionsPage.content, "test string")

class GDPRModelTest(TestCase):
    def setUp(self) -> None:
        GDPRPage1 = GDPR.objects.create(content="test content")
        #return super().setUp()
    def test_about_content(self):
        GDPRPage = GDPR.objects.get(id=1)
        self.assertEqual(GDPRPage.content, "test content")
        self.assertNotEqual(GDPRPage.content, "test string")

class AboutModelTest(TestCase):
    def setUp(self) -> None:
        aboutPage1 = About.objects.create(content="test content")
        #return super().setUp()
    def test_about_content(self):
        aboutPage = About.objects.get(id=1)
        self.assertEqual(aboutPage.content, "test content")
        self.assertNotEqual(aboutPage.content, "test string")