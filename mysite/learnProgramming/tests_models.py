from cv2 import threshold
from django.test import TestCase
from .models import *

# Create your tests here.

class ProgrammingLanguageTest(TestCase):
    def setUp(self) -> None:
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        #return super().setUp()
    def test_programming_language(self):
        ProgrammingLanguageObj = Programming_Language.objects.get(id=1)
        self.assertEqual(ProgrammingLanguageObj.name, "test name")
        self.assertNotEqual(ProgrammingLanguageObj.name, "test string")
        self.assertEqual(ProgrammingLanguageObj.slug, "test slug")
        self.assertNotEqual(ProgrammingLanguageObj.slug, "test string")
        self.assertEqual(ProgrammingLanguageObj.icon, "test icon")
        self.assertNotEqual(ProgrammingLanguageObj.icon, "test string")

class SubjectTest(TestCase):
    def setUp(self) -> None:
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        UserObj2 = User.objects.create(username='test_username2', password='test_password2', email="test_email2@test.com")
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLangObj2 = Programming_Language.objects.create(name="test name1", slug="test slug1", icon="test icon1")
        #return super().setUp()
    def test_subject(self):
        User1 = User.objects.get(id=1)
        User2 = User.objects.get(id=2)
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        ProgrammingLang2 = Programming_Language.objects.get(id=2)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)

        self.assertEqual(SubjectObj.name, "test name")
        self.assertNotEqual(SubjectObj.name, "test string")
        self.assertEqual(SubjectObj.author, User1)
        self.assertNotEqual(SubjectObj.author, User2)
        self.assertEqual(SubjectObj.programming_lang, ProgrammingLang1)
        self.assertNotEqual(SubjectObj.programming_lang, ProgrammingLang2)
        self.assertEqual(SubjectObj.slug, "test slug")
        self.assertNotEqual(SubjectObj.slug, "test string")
    
class TestTest(TestCase):
    def setUp(self) -> None:
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        ProgrammingLangObj1 = Programming_Language.objects.create(name="test name", slug="test slug", icon="test icon")
        ProgrammingLang1 = Programming_Language.objects.get(id=1)
        SubjectObj1 = Subject.objects.create(name="test name", author = User1, programming_lang = ProgrammingLang1, slug="test slug")
        SubjectObj = Subject.objects.get(id=1)
        TestObj1 = Test.objects.create(name = 'test name', subject = SubjectObj, slug = 'test slug', author = User1,
                test_description= 'test description', questions_number = 50, threshold = 50)
        #return super().setUp()
    def test_test(self):
        TestObj = Test.objects.get(id=1)
        SubjectObj = Subject.objects.get(id=1)
        User1 = User.objects.get(id=1)

        self.assertEqual(TestObj.name, 'test name')
        self.assertEqual(TestObj.subject, SubjectObj)
        self.assertEqual(TestObj.slug, 'test slug')
        self.assertEqual(TestObj.author, User1)
        self.assertEqual(TestObj.test_description, 'test description')
        self.assertEqual(TestObj.questions_number, 50)
        self.assertEqual(TestObj.threshold, 50)

class QuestionTest(TestCase):
    def setUp(self) -> None:
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
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
        #return super().setUp()
    def test_question(self):
        TestObj = Test.objects.get(id=1)
        QuestionObj = Question.objects.get(id=1)

        self.assertEqual(QuestionObj.question_number, 5)
        self.assertEqual(QuestionObj.question_content, 'test question content')
        self.assertEqual(QuestionObj.max_points, 10)
        self.assertEqual(QuestionObj.test, TestObj)
        self.assertEqual(QuestionObj.multi_selection, False)

class AnswerTest(TestCase):
    def setUp(self) -> None:
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
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
        QuestionObj = Question.objects.get(id=1)
        AnswerObj1 = Answer.objects.create(answer_content = "test answer content", question = QuestionObj, if_correct = True)
        #return super().setUp()
    def test_question(self):
        QuestionObj = Question.objects.get(id=1)
        AnswerObj = Answer.objects.get(id=1)

        self.assertEqual(AnswerObj.answer_content, "test answer content")
        self.assertEqual(AnswerObj.question, QuestionObj)
        self.assertEqual(AnswerObj.if_correct, True)
