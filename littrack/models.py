from django.conf import settings
from django.db import models

class Book(models.Model):
    cover = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=400)
    isbn13 = models.CharField(max_length=13)
    rating = models.IntegerField(null=True)
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title