from django.db import models

# Create your models here.
class FAQs(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.title
    
def upload_to(instance, filename):
    # This function generates the upload path for the image
    return 'category_images/{filename}'.format(filename=filename)

class Categories(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True)
    
    def __str__(self):
        return self.title
