from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    artist = models.CharField(max_length=50, blank=True, null=True)
    album = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
