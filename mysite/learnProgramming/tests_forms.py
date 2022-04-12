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

class SubjectFormTest(TestCase):
    def test_name_field(self):
        form = Subject_Form()
        self.assertTrue(form.fields['name'].required)
        self.assertEqual(form.fields['name'].max_length, 1000)
        self.assertFalse(form.is_valid())
    
    def test_form_post(self):
        form1 = Programming_Language_Form(
            data={'name': 'test_name'}
        )
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['name'], 'test_name')

class QuestionFormTest(TestCase):
    def test_required_fields(self):
        form = Question_Form()
        self.assertTrue(form.fields['question_content'].required)
        self.assertTrue(form.fields['max_points'].required)
        self.assertFalse(form.fields['multi_selection'].required)
        self.assertFalse(form.fields['answer1'].required)
        self.assertFalse(form.fields['answer2'].required)
        self.assertFalse(form.fields['answer3'].required)
        self.assertFalse(form.fields['answer4'].required)
        self.assertFalse(form.fields['answer5'].required)
        self.assertFalse(form.fields['answer6'].required)
        self.assertFalse(form.fields['answer7'].required)
        self.assertFalse(form.fields['answer8'].required)
        self.assertFalse(form.fields['answer9'].required)
        self.assertFalse(form.fields['answer10'].required)
        self.assertFalse(form.fields['answer1_correct'].required)
        self.assertFalse(form.fields['answer2_correct'].required)
        self.assertFalse(form.fields['answer3_correct'].required)
        self.assertFalse(form.fields['answer4_correct'].required)
        self.assertFalse(form.fields['answer5_correct'].required)
        self.assertFalse(form.fields['answer6_correct'].required)
        self.assertFalse(form.fields['answer7_correct'].required)
        self.assertFalse(form.fields['answer8_correct'].required)
        self.assertFalse(form.fields['answer9_correct'].required)
        self.assertFalse(form.fields['answer10_correct'].required)
        self.assertFalse(form.is_valid())
    
    def test_form_post(self):
        form1 = Question_Form(
            data={'question_content': 'test content',
                  'max_points': 5, 
                  'multi_selection': False,
                  'answer1': 'test answer',
                  'answer1_correct': True,}
        )
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['question_content'], 'test content')
        self.assertEqual(form1.cleaned_data['max_points'], 5)
        self.assertEqual(form1.cleaned_data['multi_selection'], False)
        self.assertEqual(form1.cleaned_data['answer1'], 'test answer')
        self.assertEqual(form1.cleaned_data['answer1_correct'], True)

class AnswerFormTest(TestCase):
    def test_required_fields(self):
        form = Answer_Form()
        self.assertFalse(form.fields['answer1'].required)
        self.assertFalse(form.fields['answer2'].required)
        self.assertFalse(form.fields['answer3'].required)
        self.assertFalse(form.fields['answer4'].required)
        self.assertFalse(form.fields['answer5'].required)
        self.assertFalse(form.fields['answer6'].required)
        self.assertFalse(form.fields['answer7'].required)
        self.assertFalse(form.fields['answer8'].required)
        self.assertFalse(form.fields['answer9'].required)
        self.assertFalse(form.fields['answer10'].required)
        self.assertFalse(form.is_valid())
    
    def test_form_post(self):
        form1 = Answer_Form(
            data={'answer1': True,
                  'answer2': False,
                  'answer3': True}
        )
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['answer1'], True)
        self.assertEqual(form1.cleaned_data['answer2'], False)
        self.assertEqual(form1.cleaned_data['answer3'], True)
