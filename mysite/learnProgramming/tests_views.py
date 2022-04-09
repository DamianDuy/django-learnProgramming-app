from django.test import TestCase
from .views import *
from user.models import Profile

# Create your tests here.

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
