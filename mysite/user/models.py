from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canCreate = models.BooleanField(default=False)

    def __str__(self):
      return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
      if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

class Group(models.Model):
  name = models.CharField(max_length=1000)
  users = models.ManyToManyField(User)
  slug = models.SlugField(max_length=1000, unique=True, blank=True, default="")

  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    if self.slug == None or self.slug == "":
      self.slug = slugify(self.name)
    super(Group, self).save(*args, **kwargs)
