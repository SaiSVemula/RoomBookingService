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

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)

#     # Date and time combined
#     start_datetime = models.DateTimeField()  
#     end_datetime = models.DateTimeField()

#     # New DateField to track when the booking was made
#     booking_date = models.DateField(default="2024-10-23")  

#     booking_time = models.TimeField(default="13:00")  # Time of booking creation
    
#     status = models.CharField(
#         max_length=20, 
#         choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
#         default='Pending'
#     )

#     def __str__(self):
#         return f"{self.user.name} booked {self.room.name} from {self.start_datetime} to {self.end_datetime}"



def default_start_hour():
    """Calculate the default start hour as the beginning of the current hour."""
    now = datetime.now()
    return time(hour=now.hour)  # Set minutes and seconds to zero

def default_end_hour():
    """Calculate the default end hour as one hour after the start hour."""
    now = datetime.now()
    return (datetime.combine(datetime.today(), time(hour=now.hour)) + timedelta(hours=1)).time()

class Booking(models.Model):
    """Model representing a booking with start and end times restricted to full-hour values."""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    
    # Start and end hours with default values
    start_hour = models.TimeField(default=default_start_hour)
    end_hour = models.TimeField(default=default_end_hour)
    booking_date = models.DateField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def clean(self):
        """Ensure start_hour and end_hour are on the hour and that end_hour is one hour after start_hour."""
        if self.start_hour.minute != 0 or self.start_hour.second != 0:
            raise ValidationError("Start time must be on the hour (e.g., 11:00, 14:00).")
        if self.end_hour.minute != 0 or self.end_hour.second != 0:
            raise ValidationError("End time must be on the hour (e.g., 12:00, 15:00).")

        # Validate that end_hour is exactly one hour after start_hour
        start_dt = datetime.combine(datetime.today(), self.start_hour)
        end_dt = datetime.combine(datetime.today(), self.end_hour)
        if end_dt != start_dt + timedelta(hours=1):
            raise ValidationError("End time must be exactly one hour after start time.")

    def save(self, *args, **kwargs):
        """Override save to ensure validation is applied."""
        self.full_clean()  # Calls the clean method to validate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} booked {self.room.name} from {self.start_hour} to {self.end_hour} on {self.booking_date}"