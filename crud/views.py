from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Admin, Users, ActivityLog, Complaint, Category

def login_view(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(student_number=student_number)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                messages.success(request, 'Login successful!')
                return redirect('users/complaint/')  
            else:
                messages.warning(request, 'Invalid password')
                return render(request, 'layout/login.html')
        except Users.DoesNotExist:
            messages.warning(request, 'User not found')
            return render(request, 'layout/login.html')
    return render(request, 'layout/login.html')

def register_user(request):
    try:
        errors = {}
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '')
            year_level = request.POST.get('year_level', '')
            class_section = request.POST.get('class_section', '')
            email = request.POST.get('email', '')
            student_number = request.POST.get('student_number', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not full_name:
                errors['full_name'] = 'Full Name is required.'
            if not email:
                errors['email'] = 'Email is required.'
            if not year_level:
                errors['year_level'] = 'Year Level is required.'
            if not class_section:
                errors['class_section'] = 'Class Section is required.'
            if not student_number:
                errors['student_number'] = 'Student Number is required.'
            if not password:
                errors['password'] = 'Password is required.'
            if not confirm_password:
                errors['confirm_password'] = 'Confirm Password is required.'
            elif password != confirm_password:
                errors['confirm_password'] = 'Passwords do not match.'

            if not errors:
                Users.objects.create(
                    full_name=full_name,
                    year_level=year_level,
                    class_section=class_section,
                    email=email,
                    student_number=student_number,
                    password=make_password(password),
                )

                messages.success(request, 'User added successfully!')
                return redirect('/layout/register/')
            else:
                return render(request, 'users/AddUser.html', {
                    'errors': errors,
                    'full_name': full_name,
                    'year_level': year_level,
                    'class_section': class_section,
                    'email': email,
                    'student_number': student_number,
                    'password': password,
                    'confirm_password': confirm_password
                })

        return render(request, 'layout/Register.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')

# Administrator Views
@staff_member_required
def manage_users(request):
    try:
        userObj = Users.objects.all().order_by('user_id')

        data = {
            'users':  userObj
        }

        return render(request, 'administrator/ManageUsers.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

# Users Views 
@login_required_custom
def report_complaint(request):
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            course_title = request.POST.get('course_title')
            course_lecturer = request.POST.get('course_lecturer')
            complaint_details = request.POST.get('complaint_details')

            if not category_id or not course_title or not course_lecturer or not complaint_details:
                messages.error(request, "All fields are required.")
                return redirect('/users/complaint/')

            # Get the Users instance for the logged-in user
            user_id = request.session.get('user_id')
            user = Users.objects.get(user_id=user_id)

            evidence_file = request.FILES.get('file_upload')

            complaint = Complaint(
                user_id=user,  # Pass the Users instance
                category_id=category_id,
                course_title=course_title,
                course_lecturer=course_lecturer,
                complaint_details=complaint_details,
                evidence_file=evidence_file
            )
            complaint.save()

            messages.success(request, "Complaint submitted successfully.")
            return redirect('/users/complaint/')
        except Exception as e:
            print("Error:", e)
            messages.error(request, f"An error occurred: {e}")
            return redirect('/users/complaint/')
    
    categories = Category.objects.all()
    return render(request, 'users/Complaint.html', {'categories': categories})

def account_setting(request):
    return render(request, 'users/AccountSetting.html')

def complaint_history(request):
    return render(request, 'users/ComplaintHistory.html')

def dashboard(request):
    return render(request, 'users/Dashboard.html')

def logout_view(request):
    request.session.flush()  # Clear all session data
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))