from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Admin, Users, ActivityLog, Complaint, Category, YearLevel, Sections
from django.db.models import Q, Case, When, IntegerField, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.contrib.messages import error as messages_error
from django.db import models

def login_view(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(student_number=student_number)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                messages.success(request, 'Login successful!')
                return redirect('users/dashboard/')  
            else:
                messages.warning(request, 'Invalid password')
                return render(request, 'layout/login.html')
        except Users.DoesNotExist:
            messages.warning(request, 'User not found')
            return render(request, 'layout/login.html')
    return render(request, 'layout/login.html')

def register_user(request):
    YEAR_LEVELS = [
        'First Year',
        'Second Year',
        'Third Year',
        'Fourth Year'
    ]
    
    SECTIONS = [
        'BSCS-1A', 'BSCS-1B', 'BSCS-1C',
        'BSIT-1A', 'BSIT-1B', 'BSIT-1C',
        'BSIT-2A', 'BSIT-2B', 'BSIT-2C',
        'BSIT-3A', 'BSIT-3B', 'BSIT-3C',
        'BSIT-4A', 'BSIT-4B', 'BSIT-4C'
    ]

    if request.method == 'POST':
        errors = {}
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '')
            year_level_name = request.POST.get('year_level', '')
            section_name = request.POST.get('class_section', '')
            email = request.POST.get('email', '')
            student_number = request.POST.get('student_number', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not full_name:
                errors['full_name'] = 'Full Name is required.'
            if not email:
                errors['email'] = 'Email is required.'
            if not year_level_name:
                errors['year_level'] = 'Year Level is required.'
            if not section_name:
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
                try:
                    # Get or create year level
                    year_level, _ = YearLevel.objects.get_or_create(
                        name=year_level_name,
                        defaults={'name': year_level_name}
                    )
                    
                    # Get or create section
                    section, _ = Sections.objects.get_or_create(
                        name=section_name,
                        defaults={'name': section_name}
                    )

                    Users.objects.create(
                        full_name=full_name,
                        year_level=year_level,
                        class_section=section,
                        email=email,
                        student_number=student_number,
                        password=make_password(password),
                    )
                    messages.success(request, 'User added successfully!')

                    return redirect('login')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('/layout/register/')
            else:
                return render(request, 'layout/register.html', {
                    'errors': errors,
                    'full_name': full_name,
                    'year_level': year_level_name,
                    'class_section': section_name,
                    'email': email,
                    'student_number': student_number,
                    'password': password,
                    'confirm_password': confirm_password,
                    'year_levels': YEAR_LEVELS,
                    'sections': SECTIONS
                })
    else:
        return render(request, 'layout/register.html', {
            'year_levels': YEAR_LEVELS,
            'sections': SECTIONS
        })

# Administrator Views
@staff_member_required
def manage_users(request):
    try:
        search_query = request.GET.get('search', '').strip()
        userObj = Users.objects.all().order_by('user_id')
        if search_query:
            userObj = userObj.filter(
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(student_number__icontains=search_query) |
                Q(year_level__name__icontains=search_query)
            )
        paginator = Paginator(userObj, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_complaints = Complaint.objects.count()
        resolved_complaints = Complaint.objects.filter(status='Resolved').count()

        data = {
            'users': page_obj,
            'page_obj': page_obj,
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_complaints,
            'search_query': search_query,
        }

        return render(request, 'administrator/ManageUsers.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load users: {e}')

@staff_member_required
def manage_complaints(request):
    try:
        # Get all categories for the filter dropdown
        categories = Category.objects.all()
        
        # Get the selected category and status from the request
        selected_category = request.GET.get('category')
        selected_status = request.GET.get('status')
        
        # Base queryset
        complaints = Complaint.objects.select_related('user_id', 'category').all()
        
        # Apply category filter if selected
        if selected_category:
            complaints = complaints.filter(category_id=selected_category)
        # Apply status filter if selected
        if selected_status:
            complaints = complaints.filter(status=selected_status)
        
        # Order by complaint_id
        complaints = complaints.order_by('-complaint_id')
        
        # Pagination
        paginator = Paginator(complaints, 15)  # Show 15 complaints per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        total_complaints = complaints.count()
        
        context = {
            'complaints': page_obj,
            'categories': categories,
            'selected_category': selected_category,
            'selected_status': selected_status,
            'total_complaints': total_complaints,
        }
        
        return render(request, 'administrator/ManageComplaints.html', context)
    except Exception as e:
        return HttpResponse(f'Error occurred during load complaints: {e}')
    
@staff_member_required
def view_complaint(request, complaint_id):
    try:
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        return render(request, 'administrator/ViewComplaint.html', {'complaint': complaint})
    except Exception as e:
        messages.error(request, f'Error loading complaint details: {e}')
        return redirect('manage_complaints')

@staff_member_required
def update_complaint_status(request, complaint_id):
    if request.method == 'POST':
        try:
            complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
            new_status = request.POST.get('status')
            
            if new_status in ['Pending', 'On-going', 'Resolved']:
                complaint.status = new_status
                complaint.save()
                messages.success(request, f'Complaint status updated to {new_status}')
            else:
                messages.error(request, 'Invalid status value')
                
        except Exception as e:
            messages.error(request, f'Error updating complaint status: {e}')
            
    return redirect('view_complaint', complaint_id=complaint_id)

@staff_member_required
def edit_user(request, user_id):
    try:
        user = get_object_or_404(Users, user_id=user_id)
        year_levels = YearLevel.objects.all()
        sections = Sections.objects.all()

        if request.method == 'POST':
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            student_number = request.POST.get('student_number', '').strip()
            year_level_name = request.POST.get('year_level')
            section_name = request.POST.get('class_section')

            # Check if email is already taken by another user
            if Users.objects.exclude(user_id=user_id).filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
                return render(request, 'administrator/Edituser.html', {
                    'user': user,
                    'year_levels': year_levels,
                    'sections': sections
                })

            # Check if student number is already taken by another user
            if Users.objects.exclude(user_id=user_id).filter(student_number=student_number).exists():
                messages.error(request, 'Student number is already taken.')
                return render(request, 'administrator/Edituser.html', {
                    'user': user,
                    'year_levels': year_levels,
                    'sections': sections
                })

            try:
                # Get or create year level
                year_level, _ = YearLevel.objects.get_or_create(
                    name=year_level_name,
                    defaults={'name': year_level_name}
                )
                
                # Get or create section
                section, _ = Sections.objects.get_or_create(
                    name=section_name,
                    defaults={'name': section_name}
                )

                # Update user information
                user.full_name = full_name
                user.email = email
                user.student_number = student_number
                user.year_level = year_level
                user.class_section = section
                user.save()

                messages.success(request, 'User updated successfully!')
                return redirect('manage_users')
            except Exception as e:
                messages.error(request, f'Error updating user: {str(e)}')
                return render(request, 'administrator/Edituser.html', {
                    'user': user,
                    'year_levels': year_levels,
                    'sections': sections
                })

        return render(request, 'administrator/Edituser.html', {
            'user': user,
            'year_levels': year_levels,
            'sections': sections
        })
    except Exception as e:
        messages.error(request, f'Error updating user: {str(e)}')
        return redirect('manage_users')

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
                messages.error(request, "All fields except evidence are required.")
                return redirect('/users/complaint/')

            # Get the Users instance for the logged-in user
            user_id = request.session.get('user_id')
            user = Users.objects.get(user_id=user_id)

            # Get the evidence file if provided
            evidence_file = request.FILES.get('file_upload')

            # Create the complaint
            complaint = Complaint(
                user_id=user,
                category_id=category_id,
                course_title=course_title,
                course_lecturer=course_lecturer,
                complaint_details=complaint_details,
                evidence_file=evidence_file if evidence_file else None
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

@login_required_custom
def account_setting(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '').strip()
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            errors = {}

            # Name update
            if full_name:
                user.full_name = full_name

            # Password update
            if current_password or new_password or confirm_password:
                if not current_password:
                    errors['current_password'] = 'Current password is required.'
                elif not user.check_password(current_password):
                    errors['current_password'] = 'Current password is incorrect.'
                elif not new_password:
                    errors['new_password'] = 'New password is required.'
                elif new_password != confirm_password:
                    errors['confirm_password'] = 'New passwords do not match.'
                else:
                    user.set_password(new_password)
                    user.save()

            if errors:
                for k, v in errors.items():
                    messages.error(request, v)
            else:
                user.save()
                messages.success(request, 'Account updated successfully!')
            return redirect('account_setting')
        return render(request, 'users/AccountSetting.html', {'user': user})
    except Exception as e:
        messages.error(request, f'Error occurred loading account settings: {e}')
        return redirect('account_setting')

@login_required_custom
def complaint_history(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
        complaints = Complaint.objects.filter(user_id=user).annotate(
            status_priority=Case(
                When(status='Pending', then=0),
                When(status='On-going', then=1),
                When(status='Resolved', then=2),
                default=3,
                output_field=IntegerField(),
            )
        ).order_by('status_priority', '-complaint_id')
        paginator = Paginator(complaints, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'users/ComplaintHistory.html', {'complaints': page_obj, 'page_obj': page_obj, 'user': user})
    except Exception as e:
        return HttpResponse(f'Error occurred loading complaint history: {e}')

@login_required_custom
def dashboard(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
        total_complaints = Complaint.objects.filter(user_id=user).count()
        new_complaints = Complaint.objects.filter(user_id=user, status='Pending').count()
        ongoing_complaints = Complaint.objects.filter(user_id=user, status='On-going').count()
        closed_complaints = Complaint.objects.filter(user_id=user, status='Resolved').count()
        complaints = Complaint.objects.filter(user_id=user).order_by('-complaint_id')

        # Pagination: 10 per page
        paginator = Paginator(complaints, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'user': user,
            'total_complaints': total_complaints,
            'new_complaints': new_complaints,
            'ongoing_complaints': ongoing_complaints,
            'closed_complaints': closed_complaints,
            'complaints': page_obj,
            'page_obj': page_obj,
        }
        return render(request, 'users/Dashboard.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred loading dashboard: {e}')

def logout_view(request):
    # Only clear student-specific session data
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))

def delete_user(request, user_id):
    user = get_object_or_404(Users, user_id=user_id)
    # Delete associated complaints
    Complaint.objects.filter(user_id=user).delete()
    # Delete the user
    user.delete()
    return redirect('manage_users')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Changed from email to username
        password = request.POST.get('password')
        
        # First try to authenticate with the provided credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('manage_users')
            else:
                messages.warning(request, 'You do not have administrator privileges')
        else:
            messages.warning(request, 'Invalid username or password')
            
        return render(request, 'administrator/administrator.html')
    
    return render(request, 'administrator/administrator.html')

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return render(request, 'administrator/administratorsignup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'administrator/administratorsignup.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'administrator/administratorsignup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'administrator/administratorsignup.html')

        try:
            # Create a new superuser with staff privileges
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,  # This gives admin access
                is_superuser=True  # This gives full admin privileges
            )
            messages.success(request, 'Admin account created successfully!')
            return redirect('admin_login')
        except Exception as e:
            messages.error(request, f'Error creating admin account: {str(e)}')
            return render(request, 'administrator/administratorsignup.html')

    return render(request, 'administrator/administratorsignup.html')

def admin_logout(request):
    # Only clear admin-specific session data
    logout(request)  # This clears the admin authentication
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@staff_member_required
def admin_dashboard(request):
    try:
        # Get total complaints
        total_complaints = Complaint.objects.count()
        
        # Get complaints by category for pie chart
        category_data = Complaint.objects.values('category__name').annotate(count=Count('complaint_id'))
        
        # Get complaints by status for pie chart
        status_data = Complaint.objects.values('status').annotate(count=Count('complaint_id'))
        
        # Get monthly complaints for each year level
        year_levels = YearLevel.objects.all().order_by('name')
        monthly_stats = []
        
        for year_level in year_levels:
            monthly_data = Complaint.objects.filter(
                user_id__year_level=year_level
            ).annotate(
                month=ExtractMonth('created_at')
            ).values('month').annotate(
                count=Count('complaint_id')
            ).order_by('month')
            
            # Initialize all months with 0
            month_counts = [0] * 12
            
            # Update with actual data
            for data in monthly_data:
                month_counts[data['month'] - 1] = data['count']
            
            monthly_stats.append({
                'year_level': year_level.name,
                'data': month_counts
            })
        
        context = {
            'total_complaints': total_complaints,
            'category_data': list(category_data),
            'status_data': list(status_data),
            'monthly_stats': monthly_stats,
            'year_levels': year_levels,
        }
        
        return render(request, 'administrator/admin_dashboard.html', context)
    except Exception as e:
        return HttpResponse(f'Error occurred loading admin dashboard: {e}')
