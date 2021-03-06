from django.test import TestCase
from .views import *
from user.models import Profile

# Create your tests here.

class TestLoginUser(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
    
    def test_login(self):
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
    
class CanCreateFunTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        user2 = User.objects.create(username='test_username2', password='test_password2', email="test_email2@test.com")
        
        profile2 = Profile.objects.get(user=user2)
        profile2.canCreate = True
        profile2.save()

    def test_can_created(self):
        user1 = User.objects.get(id=1)
        self.assertFalse(can_create(user1))

        user2 = User.objects.get(id=2)
        self.assertTrue(can_create(user2))

class GetNextFreeQuestionNumberFunTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)
        TestObj = Test.objects.get(id=1)
        QuestionObj1 = Question.objects.create(question_number = 1, question_content = "test question content1", max_points = 10,
                                               test = TestObj, multi_selection = False)
        QuestionObj2 = Question.objects.create(question_number = 2, question_content = "test question content2", max_points = 10,
                                               test = TestObj, multi_selection = False)
        

    def test_get_next_free_question(self):
        TestObj = Test.objects.get(id=1)
        question_number = get_next_free_question_number(TestObj)
        self.assertEqual(question_number, 3)

class GetFreeTestNumberFunTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)
        TestObj = Test.objects.get(id=1)
        

    def test_get_free_test_number(self):
        TestObj = Test.objects.get(id=1)
        User1 = User.objects.get(id=1)
        test_number = get_free_test_number(User1, TestObj)
        self.assertEqual(test_number, 1)

class IsOnlyOneAnswerCorrectFunTest(TestCase):
    def setUp(self):
        pass

    def test_is_only_one_answer_correct(self):
        form1 = Answer_Form(
            data={'answer1': True,
                  'answer2': False,
                  'answer3': True}
        )
        self.assertTrue(form1.is_valid())
        self.assertFalse(is_only_one_answer_correct([form1.cleaned_data['answer1'], form1.cleaned_data['answer2'], form1.cleaned_data['answer3']]))
        
        form2 = Answer_Form(
            data={'answer1': False,
                  'answer2': False,
                  'answer3': True}
        ) 

        self.assertTrue(form2.is_valid())
        self.assertTrue(is_only_one_answer_correct([form2.cleaned_data['answer1'], form2.cleaned_data['answer2'], form2.cleaned_data['answer3']]))

        form3 = Answer_Form(
            data={'answer1': False,
                  'answer2': False,
                  'answer3': False}
        ) 

        self.assertTrue(form3.is_valid())
        self.assertFalse(is_only_one_answer_correct([form3.cleaned_data['answer1'], form3.cleaned_data['answer2'], form3.cleaned_data['answer3']]))

        form4 = Answer_Form(
            data={'answer1': True,
                  'answer2': True,
                  'answer3': True}
        ) 

        self.assertTrue(form4.is_valid())
        self.assertFalse(is_only_one_answer_correct([form4.cleaned_data['answer1'], form4.cleaned_data['answer2'], form4.cleaned_data['answer3']]))

class IsAtLeastOneAnswerCorrectFunTest(TestCase):
    def setUp(self):
        pass

    def test_is_at_least_one_answer_correct(self):
        form1 = Answer_Form(
            data={'answer1': True,
                  'answer2': False,
                  'answer3': True}
        )
        self.assertTrue(form1.is_valid())
        self.assertTrue(is_at_least_one_answer_correct([form1.cleaned_data['answer1'], form1.cleaned_data['answer2'], form1.cleaned_data['answer3']]))
        
        form2 = Answer_Form(
            data={'answer1': False,
                  'answer2': False,
                  'answer3': True}
        ) 

        self.assertTrue(form2.is_valid())
        self.assertTrue(is_at_least_one_answer_correct([form2.cleaned_data['answer1'], form2.cleaned_data['answer2'], form2.cleaned_data['answer3']]))

        form3 = Answer_Form(
            data={'answer1': False,
                  'answer2': False,
                  'answer3': False}
        ) 

        self.assertTrue(form3.is_valid())
        self.assertFalse(is_at_least_one_answer_correct([form3.cleaned_data['answer1'], form3.cleaned_data['answer2'], form3.cleaned_data['answer3']]))

        form4 = Answer_Form(
            data={'answer1': True,
                  'answer2': True,
                  'answer3': True}
        ) 

        self.assertTrue(form4.is_valid())
        self.assertTrue(is_at_least_one_answer_correct([form4.cleaned_data['answer1'], form4.cleaned_data['answer2'], form4.cleaned_data['answer3']]))

class CheckIfTestPassedFunTest(TestCase):
    def setUp(self):
        pass

    def test_check_if_test_passed(self):
        result, user_result = check_if_test_passed(50, 100, 70)
        self.assertEqual(user_result, 50)
        self.assertFalse(result)

class AddProgrammingLanguageByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)

    def test_add_programming_language(self):
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/add_new_programming_language',{})
        self.assertRedirects(response, '/no_access')

class DeleteProgrammingLanguageByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")

    def test_delete_programming_language(self):
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        slug = ProgrammingLang1.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/delete_programming_language/' + slug,{})
        self.assertRedirects(response, '/no_access')

class AddSubjectByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")

    def test_add_subject(self):
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        slug = ProgrammingLang1.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/add_new_subject/' + slug,{})
        self.assertRedirects(response, '/no_access')

class DeleteSubjectByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")

    def test_delete_subject(self):
        SubjectObj = Subject.objects.get(id=1)
        slug = SubjectObj.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/delete_subject/' + slug,{})
        self.assertRedirects(response, '/no_access')

class AddTestByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")

    def test_add_test(self):
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj = Subject.objects.get(id=1)
        slug = SubjectObj.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/add_new_test/' + slug,{})
        self.assertRedirects(response, '/no_access')

class DeleteTestByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)

    def test_delete_test(self):
        TestObj = Test.objects.get(id=1)
        slug = TestObj.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/delete_test/' + slug,{})
        self.assertRedirects(response, '/no_access')

class EditTestInfoByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)

    def test_edit_test_info(self):
        TestObj = Test.objects.get(id=1)
        id = TestObj.id
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/edit_test_info/' + str(id),{})
        self.assertRedirects(response, '/no_access')

class EditTestByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)

    def test_edit_test(self):
        TestObj = Test.objects.get(id=1)
        slug = TestObj.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/edit_test/' + slug,{})
        self.assertRedirects(response, '/no_access')

class AddQuestionByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)

    def test_add_question(self):
        TestObj = Test.objects.get(id=1)
        slug = TestObj.slug
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/add_new_question/' + slug,{})
        self.assertRedirects(response, '/no_access')

class EditQuestionByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)
        TestObj = Test.objects.get(id=1)
        QuestionObj1 = Question.objects.create(question_number = 5, question_content = "test question content", max_points = 10,
                                               test = TestObj, multi_selection = False)

    def test_edit_question(self):
        QuestionObj = Question.objects.get(id=1)
        id = QuestionObj.id
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/edit_question/' + str(id),{})
        self.assertRedirects(response, '/no_access')

class DeleteQuestionByUserTest(TestCase):
    def setUp(self):
        UserObj1 = User.objects.create_user(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)
        TestObj = Test.objects.get(id=1)
        QuestionObj1 = Question.objects.create(question_number = 5, question_content = "test question content", max_points = 10,
                                               test = TestObj, multi_selection = False)

    def test_edit_question(self):
        QuestionObj = Question.objects.get(id=1)
        id = QuestionObj.id
        self.client.login(username='test_username', password='test_password')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post('/delete_question/' + str(id),{})
        self.assertRedirects(response, '/no_access')
