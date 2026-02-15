from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('book/', views.book_appointment, name='book'),
    path('history/', views.appointment_history, name='history'),
    path('availability/', views.set_availability, name='availability'),
    path('logout/', views.user_logout, name='logout'),
    path('history/export/pdf/', views.export_appointments_pdf, name='export_appointments_pdf'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('export/csv/', views.export_appointments_csv, name='export_appointments_csv'),
    path('export/pdf/', views.export_appointments_pdf, name='export_appointments_pdf'),
    path('export/json/', views.export_appointments_json, name='export_appointments_json'),
    path('profile/', views.profile, name='profile'),
]
