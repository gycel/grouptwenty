from django.db import models

# Create your models here.
from django.db import models

# Admin model
class Admin(models.Model):
    admin_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=55, unique=True, blank=False)
    password = models.CharField(max_length=55, blank=False) 
    email = models.EmailField(max_length=55, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

# Users model 
class Users(models.Model):
    YEAR_LEVEL_CHOICES = [
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
    ]
  
    user_id = models.BigAutoField(primary_key=True, blank=False)
    full_name = models.CharField(max_length=55, blank=False)
    year_level = models.CharField(
        max_length=55, 
        blank=False, 
        choices=YEAR_LEVEL_CHOICES, 
        default=''
    )
    class_section = models.CharField(max_length=55, blank=False, null=True) 
    email = models.EmailField(max_length=55, blank=False)
    password = models.CharField(max_length=55, blank=False)
    student_number = models.CharField(max_length=55, blank=False, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id

# ActivityLog model
class ActivityLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    action = models.TextField(blank=False)  
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action} at {self.timestamp}"
    
class Category(models.Model):
    name = models.CharField(max_length=55, unique=True, blank=False)

    def __str__(self):
        return self.name
    

# Complaint model
class Complaint(models.Model):
    complaint_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=55, blank=False)
    course_lecturer = models.CharField(max_length=55, blank=False)
    complaint_details = models.TextField(blank=False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint by {self.user.full_name} - {self.status}"
    
    