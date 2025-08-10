from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import FileResponse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.db import IntegrityError

from .models import student as Student, Clerk, Town, buspass
from .forms import StudentRegistrationForm, LoginForm
from .utils import generate_pdf_pass
from .decorators import student_required, clerk_required

# -------------------------
# REGISTER VIEW
# -------------------------
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return render(request, 'register.html', {'form': form})

            try:
                user = User.objects.create_user(
                    username=username,
                    password=form.cleaned_data['password']
                )
                Student.objects.create(
                    user=user,
                    full_name=form.cleaned_data['full_name'],
                    course=form.cleaned_data['course'],
                    academic_year=form.cleaned_data['academic_year'],
                    photo=form.cleaned_data['photo'],
                    town=form.cleaned_data['town']
                )
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
            except IntegrityError:
                messages.error(request, "There was an error creating your account. Please try again.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


# -------------------------
# LOGIN VIEW WITH ROLE REDIRECT
# -------------------------
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'clerk'):
                    return redirect('clerk_dashboard')
                elif hasattr(user, 'student'):
                    return redirect('home')
                else:
                    messages.error(request, 'User has no role assigned.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# -------------------------
# STUDENT VIEWS
# -------------------------
@never_cache
@login_required(login_url='login')
@student_required
def home(request):
    student_obj = Student.objects.filter(user=request.user).first()
    return render(request, 'home.html', {'student': student_obj})


@never_cache
@login_required(login_url='login')
@student_required
def payment(request):
    student_obj = Student.objects.filter(user=request.user).first()
    if not student_obj:
        messages.error(request, "Student profile not found.")
        return redirect('home')

    town_obj = Town.objects.filter(name=student_obj.town).first()
    if not town_obj:
        messages.error(request, "Associated town not found.")
        return redirect('home')

    current_month = timezone.now().strftime("%B")
    current_year = timezone.now().year

    if request.method == 'POST':
        pdf_path = generate_pdf_pass(student_obj, current_month, current_year)
        return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f"{student_obj.user}_bus_pass.pdf")

    context = {
        'student': student_obj,
        'current_month': current_month,
        'current_year': current_year,
        'price': town_obj.price,
        'qr_code_url': '/static/qr.svg'
    }
    return render(request, 'payment.html', context)


@never_cache
@login_required(login_url='login')
@student_required
def find_bus(request):
    student_obj = Student.objects.filter(user=request.user).first()
    towns = Town.objects.all().order_by('name')
    return render(request, 'find_bus.html', {'student': student_obj, 'towns': towns})


@never_cache
@login_required(login_url='login')
@student_required
def bus_payment(request, town_id):
    student = Student.objects.filter(user=request.user).first()
    town = get_object_or_404(Town, id=town_id)

    current_month = timezone.now().strftime('%B')
    current_year = timezone.now().year

    context = {
        'student': student,
        'town': town,
        'price': town.price,
        'qr_code_url': '/static/qr.svg',
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'bus_payment.html', context)


@never_cache
@login_required(login_url='login')
@student_required
def confirm_payment(request, town_id):
    if request.method == 'POST':
        student_obj = Student.objects.filter(user=request.user).first()
        selected_town = get_object_or_404(Town, id=town_id)

        current_month = timezone.now().strftime("%B")
        current_year = timezone.now().year

        if not buspass.objects.filter(student=student_obj, month=current_month, year=current_year).exists():
            buspass.objects.create(
                student=student_obj,
                month=current_month,
                year=current_year,
                is_renewed=True
            )
            pdf_path = generate_pdf_pass(student_obj, current_month, current_year, selected_town)
            return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f"{student_obj.user}_bus_pass.pdf")
        else:
            messages.warning(request, "You have already renewed your pass for this month.")
    
    return redirect('home')


# -------------------------
# CLERK DASHBOARD
# -------------------------
@never_cache
@login_required(login_url='login')
@clerk_required
def clerk_dashboard(request):
    query = request.GET.get('query')
    student = None
    renewed_this_month = False

    if query:
        student = Student.objects.filter(user__username=query).first()
        if student:
            current_month = timezone.now().strftime("%B")
            current_year = timezone.now().year
            renewed_this_month = buspass.objects.filter(
                student=student,
                month=current_month,
                year=current_year,
                is_renewed=True
            ).exists()

    return render(request, 'clerk_dashboard.html', {
        'student': student,
        'query': query,
        'renewed_this_month': renewed_this_month
    })


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def after_login_redirect(request):
    if hasattr(request.user, 'clerk'):
        return redirect('clerk_dashboard')
    elif hasattr(request.user, 'student'):
        return redirect('home')
    else:
        return redirect('login')


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, StudentUpdateForm
from .models import student

@login_required
def profile(request):
    # get the student's profile for the logged-in user
    stu = student.objects.get(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        s_form = StudentUpdateForm(request.POST, request.FILES, instance=stu)

        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')  # reload page
    else:
        u_form = UserUpdateForm(instance=request.user)
        s_form = StudentUpdateForm(instance=stu)

    context = {
        'u_form': u_form,
        's_form': s_form
    }
    return render(request, 'profile.html', context)
