from django.contrib import admin
from .models import Room, User, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'capacity', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'capacity')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_hour', 'end_hour', 'status', 'booking_date')
    list_filter = ('status', 'start_hour', 'room')
    search_fields = ('user__name', 'room__name')
