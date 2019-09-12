from django.db import models

class Coop(models.Model):
    title = models.CharField(max_length=255)

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    coop = models.ForeignKey(Coop, on_delete=models.CASCADE)