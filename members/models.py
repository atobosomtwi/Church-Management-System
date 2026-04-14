from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class UserProfiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profile_pictures', null=True)
    
gender = (
    ("Male", "Male"),
    ("Female", "Female"),
          )

marital_status= (
    ("single", "Single"), 
    ("married", "Married"), 
    ("divorced", "Divorced"), 

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
    marital_status = models.CharField(max_length=100, choices=marital_status, null=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'members'
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

# # Attendance Model 
# class Attendance(models.Model):
#     members = models.ForeignKey(Members, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         if self.status:
#             return f"{self.members} - Present"
#         return f"{self.members} - Absent"
        
    
# Committee Model 
class Committee(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    members = models.ManyToManyField(Members, blank=True)

    def __str__(self):
        return self.name
    
expense_choices = (
    ("Giving", "Giving"),
    ("Tithe", "Tithe"),
    ("Donation", "Donation"),
    ("Benevolence", "Benevolence"),
    ("Miscellaneous", "Miscellaneous"),
)

expense_type = (
   ("Income", "Income"),
    ("Expense", "Expense"),
   
)

class Finance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(decimal_places=2, max_digits=1000)
    category = models.CharField(max_length=50, choices=expense_choices, null=True)
    type = models.CharField(max_length=25, choices=expense_type, null=True)
    purpose = models.TextField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f"{self.category} -- {self.type}"
    
    class Meta:
        db_table = 'Finance'
        managed = True
        verbose_name = 'Finance'
        verbose_name_plural = 'Finances'

service_choices = (
    ("sunday", "Sunday Service"),
    ("midweek", "Mid Week Service")
)


class Attendance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE, blank=True, null=True)
    non_registered = models.CharField(max_length=100, null=True, blank=True)
    service_type = models.CharField(max_length=100, choices=service_choices, null=True)
    recorded_by = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date}"
    
    class Meta:
        db_table = 'Attendance'
        managed = True
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'

class Visitors(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    full_name = models.CharField( max_length=50)
    gender = models.CharField(max_length=20, choices=gender)
    phone_number = models.CharField(null=True, blank=True, default='N/A')
    location = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100, choices=service_choices, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'visitors'
        managed = True
        verbose_name = 'Visitor'
        verbose_name_plural = 'visitors'