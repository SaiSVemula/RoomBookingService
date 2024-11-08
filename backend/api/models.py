"""Models for room booking system."""
from datetime import datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    """Custom user model with additional fields."""
    STAFF_TYPE_CHOICES = [
        ('Admin', 'Admin'),
        ('Professors', 'Professors'),
        ('Student', 'Student'),
        ('Academic Staff', 'Academic Staff'),
    ]
    
    SCHOOLS = [
        ('School of the Arts', 'School of the Arts'),
        ('School of Business and Management', 'School of Business and Management'),
        ('School of Economics and Finance', 'School of Economics and Finance'),
        ('School of Geography', 'School of Geography'),
        ('School of History', 'School of History'),
        ('School of Law', 'School of Law'),
        ('School of politics and International Relations', 'School of politics and International Relations'),
        ('School of Medicine and Dentistry', 'School of Medicine and Dentistry'),
        ('School of Biological and Behavioural Sciences', 'School of Biological and Behavioural Sciences'),
        ('School of Electronic Engineering and Computer Science', 'School of Electronic Engineering and Computer Science'),
        ('School of Engineering and Materials Science', 'School of Engineering and Materials Science'),
        ('School of Mathematical Sciences', 'School of Mathematical Sciences'),
        ('School of physical and Chemical Sciences', 'School of physical and Chemical Sciences'),
    ]
    
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    reenter_password = models.CharField(max_length=128)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES, default='Academic Staff')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    school = models.CharField(max_length=100, choices=SCHOOLS, default='School of Engineering and Materials Science')

    def __str__(self):
        """Return string representation of CustomUser."""
        return self.username



class Room(models.Model):
    """Model representing a room that can be booked."""

    name = models.CharField(max_length=1000)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        """Return string representation of Room."""
        return self.name


class Booking(models.Model):
    """Model representing a booking with start and end times."""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)
    booking_date = models.DateField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def clean(self):
        """Validate booking times."""
        if self.start_hour >= self.end_hour:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        """Return string representation of Booking."""
        return (
            f"{self.user.username} booked {self.room.name} from "
            f"{self.start_hour} to {self.end_hour} on {self.booking_date}"
        )
