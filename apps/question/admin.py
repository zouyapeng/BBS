from django.contrib import admin

# Register your models here.
from apps.question import models

admin.site.register(models.Question)