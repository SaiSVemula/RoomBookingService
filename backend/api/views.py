import datetime
import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Room, User, Booking

#rooms
@csrf_exempt
def get_rooms(request):
    rooms = Room.objects.all()
    room_list = [{"id": room.id, "name": room.name, "capacity": room.capacity} for room in rooms]
    return JsonResponse(room_list, safe=False)

@csrf_exempt
def get_available_slots(request, room_id):
    if request.method == 'GET':
        try:
            # Get the room and existing bookings for that room
            room = get_object_or_404(Room, id=room_id)
            bookings = Booking.objects.filter(room=room)

            # Define the possible time slots for the room (e.g., every hour from 9 AM to 5 PM)
            slots = [time(hour, 0) for hour in range(9, 18)]  # 9:00 to 17:00

            # Collect booked slots
            booked_slots = [(booking.start_hour, booking.end_hour) for booking in bookings]

            # Filter out the slots that are already booked
            available_slots = []
            for slot in slots:
                slot_end = (datetime.combine(datetime.today(), slot) + timedelta(hours=1)).time()
                if all(not (start <= slot < end) for start, end in booked_slots):
                    available_slots.append((slot, slot_end))

            return JsonResponse({"available_slots": available_slots})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

#users
@csrf_exempt
def get_user(request, user_id=None):
    if request.method == 'GET':
        try:
            # If user_id is provided, return specific user details
            if user_id:
                user = get_object_or_404(User, id=user_id)
                user_data = {"id": user.id, "name": user.name, "email": user.email}
                return JsonResponse(user_data)
            else:
                # If no user_id is provided, return all users
                users = User.objects.all()
                user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
                return JsonResponse(user_list, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']

            # Create a new user
            user = User.objects.create(
                name=name,
                email=email
            )
            return JsonResponse({"message": "User created successfully", "user_id": user.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=user_id)

            # Update user details
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.save()

            return JsonResponse({"message": "User updated successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


#Bookings
@csrf_exempt
def get_bookings(request):
    try:
        username = request.GET.get('username', None)  # Fetch username from query parameters

        if username:
            bookings = Booking.objects.filter(user__name=username)
        else:
            bookings = Booking.objects.all()

        booking_list = [{
            "id": booking.id,
            "user": {
                "name": booking.user.name,
                "email": booking.user.email
            },
            "room": {
                "name": booking.room.name,
                "capacity": booking.room.capacity
            },
            "start_hour": str(booking.start_hour),
            "end_hour": str(booking.end_hour),
            "status": booking.status,
            "booking_date": str(booking.booking_date)
        } for booking in bookings]

        return JsonResponse(booking_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Fetch user and room based on provided IDs
            user = get_object_or_404(User, id=data['user_id'])
            room = get_object_or_404(Room, id=data['room_id'])

            # Create a new booking with start_hour and end_hour (time only)
            booking = Booking.objects.create(
                user=user,
                room=room,
                start_hour=data['start_hour'],  # Expecting start_hour in HH:MM:SS format
                end_hour=data['end_hour'],      # Expecting end_hour in HH:MM:SS format
                status=data.get('status', 'Pending')  # Default status is 'Pending'
            )

            return JsonResponse({"message": "Booking created successfully", "booking_id": booking.id})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def update_booking(request, booking_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            booking = get_object_or_404(Booking, id=booking_id)
            
            # Update start_hour and end_hour instead of start_datetime and end_datetime
            booking.start_hour = data['start_hour']  # Expecting start_hour in HH:MM:SS format
            booking.end_hour = data['end_hour']      # Expecting end_hour in HH:MM:SS format
            booking.status = data.get('status', booking.status)  # Keep status the same if not provided
            booking.save()

            return JsonResponse({"message": "Booking updated successfully"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_booking(request, booking_id):
    if request.method == 'DELETE':
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            booking.delete()
            return JsonResponse({"message": "Booking deleted successfully"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
