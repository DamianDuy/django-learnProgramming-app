from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.
class GDPR(models.Model):
    content = MarkdownxField(default="", null=True)

    def __str__(self):
        return self.content
  
    def get_absolute_path(self):
        return "/info/gdpr"

class Terms_And_Conditions(models.Model):
    content = MarkdownxField(default="", null=True)

    def __str__(self):
        return self.content
  
    def get_absolute_path(self):
        return "/info/terms_and_conditions"

class About(models.Model):
    content = MarkdownxField(default="", null=True)

    def __str__(self):
        return self.content
  
    def get_absolute_path(self):
        return "/info/about"