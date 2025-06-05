from django.contrib import admin
from .models import Admin, Users, ActivityLog, Category, Complaint, YearLevel, Sections

admin.site.register(Category)

admin.site.register(YearLevel)

admin.site.register(Sections)
