from django.db import models

class ContactForm(models.Model):
    name = models.CharField(max_length=255)        
    email = models.EmailField()
    phone = models.CharField(max_length=10,null=True)  
    item = models.CharField(max_length=255)
    location = models.CharField()
    startDate = models.CharField()
    endDate = models.CharField()
 
    def __str__(self):
        return self.name
