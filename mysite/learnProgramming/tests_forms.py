from django.test import TestCase
from .forms import *

# Create your tests here.

class ProgrammingLanguageFormTest(TestCase):
    def test_icon_field(self):
        form = Programming_Language_Form()
        self.assertFalse(form.fields['icon'].required)
        self.assertEqual(form.fields['icon'].max_length, 1000)
        self.assertFalse(form.is_valid())

    def test_name_field(self):
        form = Programming_Language_Form()
        self.assertTrue(form.fields['name'].required)
        self.assertEqual(form.fields['name'].max_length, 1000)
        self.assertFalse(form.is_valid())
    
    def test_form_post(self):
        form1 = Programming_Language_Form(
            data={'name': 'test_name'}
        )
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['name'], 'test_name')

        form2 = Programming_Language_Form(
            data={'name': 'test_name',
                  'icon': 'test/path'}
        )
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['icon'], 'test/path')

        form3 = Programming_Language_Form(
            data={'icon': 'test/path'}
        )
        self.assertFalse(form3.is_valid())
