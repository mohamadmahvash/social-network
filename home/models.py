from django.db import models

class Post(models.Model):
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField()
    updated = models.DateTimeField()