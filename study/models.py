from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.user.username


class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher.username} - {self.day}"





# ================= TEACHER PROFILE =================
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# ================= APPOINTMENT =================
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User, related_name='student_appointments',
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        User, related_name='teacher_appointments',
        on_delete=models.CASCADE
    )

    date = models.DateField()        # ✅ separate
    time = models.TimeField()        # ✅ added

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} → {self.teacher} on {self.date} at {self.time}"
