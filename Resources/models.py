from django.db import models

# Create your models here.
class FAQs(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.title
    
# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Categories(models.Model):
    title = models.CharField(max_length=80, blank=False, null=False)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)