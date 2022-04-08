from django.contrib import admin

from .models import GDPR, About, Terms_And_Conditions

# Register your models here.
admin.site.register(GDPR)
admin.site.register(Terms_And_Conditions)
admin.site.register(About)
