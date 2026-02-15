from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Appointment, TeacherAvailability, Profile
from .forms import AppointmentForm, AvailabilityForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Profile
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Appointment, TeacherProfile
from django.utils.timezone import now
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Appointment  # your model
from django.shortcuts import render
from .models import Appointment
import csv
from django.http import HttpResponse
from .models import Appointment
from django.http import JsonResponse
from .models import Appointment

def register(request):
    if request.method == 'POST':
        role = request.POST['role']
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        Profile.objects.create(user=user, role=role)
        return redirect('login')
    return render(request, 'auth/register.html')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'auth/login.html')


def dashboard(request):
    if not request.user.is_authenticated:
        # If user not logged in, redirect to login page
        return redirect('login')  # make sure login URL exists

    # Example dashboard data
    user = request.user
    context = {
        'user': user,
        'message': 'Welcome to your dashboard!',
        # You can add more dashboard stats here, e.g., courses, tasks, notifications
    }

    return render(request, 'study/dashboard.html', context)


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'student':
        return render(request, 'student/dashboard.html')
    return render(request, 'teacher/dashboard.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.student = request.user
            appt.save()
            return redirect('history')
    else:
        form = AppointmentForm()
    return render(request, 'student/book_appointment.html', {'form': form})


@login_required
def appointment_history(request):
    appointments = Appointment.objects.filter(student=request.user)
    return render(request, 'student/history.html', {'appointments': appointments})


@login_required
def set_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.teacher = request.user
            availability.save()
            return redirect('dashboard')
    else:
        form = AvailabilityForm()
    return render(request, 'teacher/availability.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')




def home(request):
    total_students = User.objects.filter(is_staff=False).count()
    total_teachers = User.objects.filter(is_staff=True).count()
    total_appointments = Appointment.objects.count()

    upcoming_appointments = []
    if request.user.is_authenticated:
        upcoming_appointments = Appointment.objects.filter(
            student=request.user,
            date__gte=now()
        ).order_by('date')[:5]

    featured_teachers = User.objects.filter(is_staff=True)[:3]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
        'featured_teachers': featured_teachers,
    }
    return render(request, 'home.html', context)

def export_appointments_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'

    p = canvas.Canvas(response)
    y = 800

    appointments = Appointment.objects.filter(student=request.user)

    p.drawString(100, y, "Appointment History")
    y -= 30

    for appointment in appointments:
        text = f"{appointment.teacher.user.get_full_name()} - {appointment.date} - {appointment.time} - {appointment.status}"
        p.drawString(100, y, text)
        y -= 20

    p.showPage()
    p.save()

    return response



def export_appointments_pdf(request):
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'

    p = canvas.Canvas(response)

    # Example: write table headers
    p.drawString(100, 800, "Appointment History")
    appointments = Appointment.objects.filter(student=request.user)
    y = 750
    for appointment in appointments:
        text = f"{appointment.teacher.username} - {appointment.date} {appointment.time} - {appointment.status}"
        p.drawString(50, y, text)
        y -= 20

    p.showPage()
    p.save()
    return response

def appointment_history(request):
    appointments = Appointment.objects.filter(student=request.user)
    return render(request, 'student/history.html', {'appointments': appointments})

def export_appointments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Teacher', 'Date', 'Time', 'Status'])

    appointments = Appointment.objects.filter(student=request.user)

    for appointment in appointments:
        writer.writerow([
            appointment.teacher.user.get_full_name(),
            appointment.date,
            appointment.time,
            appointment.status
        ])

    return response

def export_appointments_json(request):
    appointments = Appointment.objects.filter(student=request.user)

    data = []
    for appointment in appointments:
        data.append({
            "teacher": appointment.teacher.user.get_full_name(),
            "date": str(appointment.date),
            "time": str(appointment.time),
            "status": appointment.status,
        })

    return JsonResponse(data, safe=False)
def book_appointment(request):
    return render(request, 'student/book_appointment.html')

def history(request):
    appointments = Appointment.objects.filter(student=request.user)
    return render(request, 'student/history.html', {
        'appointments': appointments
    })

def profile(request):
    # Example: show logged-in user's info
    user = request.user
    return render(request, 'profile.html', {'user': user})