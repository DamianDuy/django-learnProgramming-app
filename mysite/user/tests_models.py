from cv2 import threshold
from django.test import TestCase
from .models import *

# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self) -> None:
        UserObj1 = User.objects.create(username='test_username', password='test_password', email="test_email@test.com")
        User1 = User.objects.get(id=1)
        #return super().setUp()
    def test_profile(self):
        User1 = User.objects.get(id=1)
        ProfileObj = Profile.objects.get(user=User1)
        self.assertEqual(ProfileObj.user, User1)
        self.assertFalse(ProfileObj.canCreate)
        self.assertFalse(ProfileObj.email_confirmed)
        self.assertFalse(ProfileObj.rodo_confirmed)
        self.assertFalse(ProfileObj.terms_and_conditions_confirmed)
       