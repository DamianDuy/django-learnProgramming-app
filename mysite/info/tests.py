from django.test import TestCase
from .models import *

# Create your tests here.

class AboutModelTest(TestCase):
    def setUp(self) -> None:
        aboutPage1 = About.objects.create(content="test content")
        #return super().setUp()
    def test_about_content(self):
        aboutPage = About.objects.get(id=1)
        self.assertEqual(aboutPage.content, "test content")
        self.assertNotEqual(aboutPage.content, "test string")