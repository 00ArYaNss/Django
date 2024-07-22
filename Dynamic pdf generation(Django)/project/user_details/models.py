from django.db import models

class UserDetails(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
