from django.db import models
from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title
