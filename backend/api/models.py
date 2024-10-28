from django.db import models
from django.core.exceptions import ValidationError
from datetime import time, timedelta, datetime

# charfield 
# textfield 
# booleanfield 
# integerfield 
# datetimefield 
# datefield 
# timefield 

class Room(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()  # Changed to TextField to meet the requirement
    is_active = models.BooleanField(default=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    """Model representing a booking with start and end times."""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    
    # Use simple start and end times without complex validation
    start_hour = models.TimeField(null=True, blank=True)    # end_hour = models.TimeField()    # Expect the front end to pass in the correct time
    end_hour = models.TimeField(null=True, blank=True)
    booking_date = models.DateField(auto_now_add=True)  # Automatically add the booking date
    
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def clean(self):
        """Ensure start_hour is before end_hour."""
        if self.start_hour >= self.end_hour:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.user.name} booked {self.room.name} from {self.start_hour} to {self.end_hour} on {self.booking_date}"