from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.auth import logout
from django.urls import reverse
from .models import Admin, Users, ActivityLog, Complaint, Category

def login_view(request):
    return render(request, 'layout/login.html')

def sidebar_view(request):
    return render(request, 'include/sidebar.html')

def add_user(request):
    try:
        errors = {}
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '')
            email = request.POST.get('email', '')
            student_number = request.POST.get('student_number', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not full_name:
                errors['full_name'] = 'Full Name is required.'
            if not email:
                errors['email'] = 'Email is required.'
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
                    email=email,
                    student_number=student_number,
                    password=make_password(password),
                )

                messages.success(request, 'User added successfully!')
                return redirect('/users/add/')
            else:
                return render(request, 'users/AddUser.html', {
                    'errors': errors,
                    'full_name': full_name,
                    'email': email,
                    'student_number': student_number,
                    'password': password,
                    'confirm_password': confirm_password
                })

        return render(request, 'users/AddUser.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')
    
def manage_users(request):
    try:
        userObj = Users.objects.all().order_by('user_id')

        data = {
            'users':  userObj
        }

        return render(request, 'admin/ManageUsers.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

def report_complaint(request):
    if request.method == 'POST':
        try:
            # Get form data
            category_id = request.POST.get('category')
            complaint_details = request.POST.get('complaint_details')
            uploaded_file = request.FILES.get('file_upload')

            # Validate required fields
            if not category_id or not complaint_details:
                messages.error(request, 'Please fill in all required fields.')
                categories = Category.objects.all()
                return render(request, 'users/Complaint.html', {'categories': categories})

            # Save the complaint
            complaint = Complaint(
                user=request.user,
                category_id=category_id,
                complaint_details=complaint_details,
                uploaded_file=uploaded_file if uploaded_file else None,
            )
            complaint.save()

            messages.success(request, 'Complaint submitted successfully!')
            return render(request, 'users/Complaint.html', {'categories': Category.objects.all()})
        except Exception as e:
            # Handle unexpected errors
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'users/Complaint.html', {'categories': Category.objects.all()})

    # Handle GET requests or other cases
    categories = Category.objects.all()
    return render(request, 'users/Complaint.html', {'categories': categories})