from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from .models import Admin, Users, ActivityLog, Complaint, Category, YearLevel, Sections

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

                    print("Redirecting to login...")
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
        userObj = Users.objects.all().order_by('user_id')
        total_complaints = Complaint.objects.count()
        resolved_complaints = Complaint.objects.filter(status='Resolved').count()

        data = {
            'users': userObj,
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_complaints
        }

        return render(request, 'administrator/ManageUsers.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

@staff_member_required
def manage_complaints(request):
    try:
        # Get all categories for the filter dropdown
        categories = Category.objects.all()
        
        # Get the selected category from the request
        selected_category = request.GET.get('category')
        
        # Base queryset
        complaints = Complaint.objects.select_related('user_id', 'category').all()
        
        # Apply category filter if selected
        if selected_category:
            complaints = complaints.filter(category_id=selected_category)
        
        # Order by complaint_id
        complaints = complaints.order_by('-complaint_id')
        
        # Pagination
        paginator = Paginator(complaints, 10)  # Show 10 complaints per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'complaints': page_obj,
            'categories': categories,
            'selected_category': selected_category,
        }
        
        return render(request, 'administrator/ManageComplaints.html', context)
    except Exception as e:
        return HttpResponse(f'Error occurred during load complaints: {e}')
    

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

@login_required_custom
def dashboard(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
        total_complaints = Complaint.objects.filter(user_id=user).count()
        resolved_complaints = Complaint.objects.filter(user_id=user, status='Resolved').count()

        data = {
            'user': user,
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_complaints
        }
        return render(request, 'users/Dashboard.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred loading dashboard: {e}')

def logout_view(request):
    request.session.flush()  # Clear all session data
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))

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
            
            if new_status in ['Pending', 'Resolved']:
                complaint.status = new_status
                complaint.save()
                messages.success(request, f'Complaint status updated to {new_status}')
            else:
                messages.error(request, 'Invalid status value')
                
        except Exception as e:
            messages.error(request, f'Error updating complaint status: {e}')
            
    return redirect('view_complaint', complaint_id=complaint_id)