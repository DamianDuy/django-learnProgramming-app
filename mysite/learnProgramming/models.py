import random  
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Programming_Language(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, unique=True, blank=True, default="")
    icon = models.CharField(max_length=1000, blank=True, default="")

    def __str__(self):
        return self.name
  
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.name)
        super(Programming_Language, self).save(*args, **kwargs)

    def get_absolute_path(self):
        return "/programming_language/"+self.slug
    

class Subject(models.Model):
    name = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    programming_lang = models.ForeignKey(Programming_Language, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True, default="")

    def __str__(self):
        return self.name

    def display_author(self):
        if self.author != None:
            return str(self.author)
        else:
            return "Author deleted an account."

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == "":
            random_string="".join((random.choice(string.ascii_lowercase) for x in range(10)))
            self.slug = slugify(self.name)+random_string
        super(Subject, self).save(*args, **kwargs)

    def get_absolute_path(self):
        return "/subject/"+self.slug
        
class Test(models.Model):
    name = models.CharField(max_length=1000)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, unique=True, blank=True, default="")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    test_description = models.TextField(default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == "":
            random_string="".join((random.choice(string.ascii_lowercase) for x in range(10)))
            self.slug = slugify(self.name)+random_string
        super(Test, self).save(*args, **kwargs)

    def get_absolute_path(self):
        return "/test/"+self.slug

class Question(models.Model):
    question_number = models.IntegerField(default=0)
    question_content = models.TextField(null=False)
    max_points = models.IntegerField(default=0)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    multi_selection = models.BooleanField(default=False)

    def __str__(self):
        return self.question_content

class Answer(models.Model):
    answer_content = models.TextField(null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    if_correct = models.BooleanField()

    def is_correct(self):
        return self.if_correct
          
    def __str__(self):
        return self.answer_content

class User_Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return "User: " + str(self.user) + ", Question: " + str(self.question) + ", Answer: " + str(self.answer)

class Answers_Data(models.Model):
    answer_date = models.DateTimeField('answer date')
    user_answer = models.ForeignKey(User_Answer, on_delete=models.CASCADE)
    
class Subject_Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_points_received = models.IntegerField(default=0)

    def __str__(self):
        return "User: " + str(self.user) + ", Subject: " + str(self.subject) + ", Points: " + str(self.subject_points_received)
      
class Test_Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_points_received = models.IntegerField(default=0)

    def __str__(self):
        return "User: " + str(self.user) + ", Test: " + str(self.test) + ", Points: " + str(self.test_points_received)
    
class Question_Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_points_received = models.IntegerField(default=0)

    def __str__(self):
        return "User: " + str(self.user) + ", Question: " + str(self.question) + ", Points: " + str(self.question_points_received)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
