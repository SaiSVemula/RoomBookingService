from django.db import models

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Date and time combined
    start_datetime = models.DateTimeField()  
    end_datetime = models.DateTimeField()

    # New DateField to track when the booking was made
    booking_date = models.DateField(default="2024-10-23")  

    booking_time = models.TimeField(default="13:00")  # Time of booking creation
    
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.name} booked {self.room.name} from {self.start_datetime} to {self.end_datetime}"
