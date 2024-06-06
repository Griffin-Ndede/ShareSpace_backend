from django.db import models

# Create your models here.
class FAQs(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.title
