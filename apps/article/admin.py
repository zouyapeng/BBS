from django.contrib import admin

# Register your models here.
from apps.article import models

admin.site.register(models.Forum)