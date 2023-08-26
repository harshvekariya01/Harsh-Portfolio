from django.db import models

# Create your models here.
class visitorquery(models.Model):
    name = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=150,default="")
    subject = models.CharField(max_length=100,default="")
    message = models.TextField(default="")
    dateandtime = models.DateField(auto_now_add=True)