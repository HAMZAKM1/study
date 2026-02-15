from django import forms
from .models import Appointment, TeacherAvailability
from django.contrib.auth.models import User

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['teacher', 'date', 'time']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = TeacherAvailability
        fields = ['day', 'start_time', 'end_time']
