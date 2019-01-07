from django.db import models
from taggit.managers import TaggableManager


class Reme(models.Model):
    media = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    last_downloaded = models.DateTimeField(auto_now=True)
    downloads = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

