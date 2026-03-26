from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

gender = (
    ("Male", "Male"),
    ("Female", "Female"),
          
          )
class Members(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    full_name = models.CharField( max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, default='N/A')
    location = models.CharField(max_length=100)
    dob = models.CharField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gender)
    date_registered = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_baptized = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'members'
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

# Attendance Model 
class Attendance(models.Model):
    members = models.ForeignKey(Members, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        if self.status:
            return f"{self.members} - Present"
        return f"{self.members} - Absent"
        
    
# Committee Model 
class Committee(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    members = models.ManyToManyField(Members, blank=True)

    def __str__(self):
        return self.name