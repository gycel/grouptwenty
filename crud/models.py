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

class YearLevel(models.Model):
    YEAR_LEVEL_CHOICES = [
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
    ]
    
    name = models.CharField(
        max_length=55, 
        unique=True, 
        blank=False,
        choices=YEAR_LEVEL_CHOICES
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Sections(models.Model):
    SECTION_CHOICES = [
        ('BSCS-1A', 'BSCS-1A'), ('BSCS-1B', 'BSCS-1B'), ('BSCS-1C', 'BSCS-1C'),
        ('BSIT-1A', 'BSIT-1A'), ('BSIT-1B', 'BSIT-1B'), ('BSIT-1C', 'BSIT-1C'),
        ('BSIT-2A', 'BSIT-2A'), ('BSIT-2B', 'BSIT-2B'), ('BSIT-2C', 'BSIT-2C'),
        ('BSIT-3A', 'BSIT-3A'), ('BSIT-3B', 'BSIT-3B'), ('BSIT-3C', 'BSIT-3C'),
        ('BSIT-4A', 'BSIT-4A'), ('BSIT-4B', 'BSIT-4B'), ('BSIT-4C', 'BSIT-4C'),
    ]
    
    name = models.CharField(
        max_length=55, 
        unique=True, 
        blank=False,
        choices=SECTION_CHOICES
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return self.name

# Users model 
class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True, blank=False)
    full_name = models.CharField(max_length=55, blank=False)
    year_level = models.ForeignKey(
        YearLevel, 
        on_delete=models.CASCADE,
        related_name='users'
    )
    class_section = models.ForeignKey(
        Sections, 
        on_delete=models.CASCADE,
        related_name='users'
    ) 
    email = models.EmailField(max_length=55, blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    student_number = models.CharField(max_length=55, blank=False, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} - {self.student_number}"

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
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE) 
    complaint_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=55, blank=False)
    course_lecturer = models.CharField(max_length=55, blank=False)
    complaint_details = models.TextField(blank=False)
    evidence_file = models.FileField(upload_to='complaint_evidence/', null=True, blank=True)    
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint by {self.user_id.full_name} - {self.status}"
    
    