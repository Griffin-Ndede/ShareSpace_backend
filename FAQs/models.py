from django.db import models

# Create your models here.
class FAQs(models.Model):
    Question = models.CharField(max_length=300)
    Answer = models.TextField()

    def __str__(self):
        return self.Question
