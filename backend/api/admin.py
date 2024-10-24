from django.contrib import admin
from .models import Room, User, Booking

# Register the Room model
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'capacity', 'is_active')  # Changed 'is_available' to 'is_active'
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'capacity')

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

# Register the Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_datetime', 'end_datetime', 'status', 'booking_date')
    list_filter = ('status', 'start_datetime', 'end_datetime', 'room')
    search_fields = ('user__name', 'room__name')
