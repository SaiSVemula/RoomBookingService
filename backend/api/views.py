
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Room, Booking
import json
from datetime import datetime, time, timedelta

User = get_user_model()

@csrf_exempt
def get_user_bookings(request):
    """Fetch all bookings for a specific user."""
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        user = get_object_or_404(User, id=user_id)
        bookings = Booking.objects.filter(user=user)

        booking_list = [
            {
                "id": booking.id,
                "room": booking.room.name,
                "start_hour": booking.start_hour.strftime("%H:%M"),
                "end_hour": booking.end_hour.strftime("%H:%M"),
                "date": booking.booking_date.strftime("%Y-%m-%d"),
                "status": booking.status,
            }
            for booking in bookings
        ]

        if not booking_list:
            return JsonResponse({"message": "No bookings found"}, status=200)

        return JsonResponse({"bookings": booking_list}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_available_times(request):
    """Fetch available times for a room on a given date."""
    if request.method == 'POST':
        data = json.loads(request.body)
        room = get_object_or_404(Room, id=data['room_id'])
        date = data['date']

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        possible_slots = [
            (
                datetime.combine(date_obj, time(hour, 0)),
                datetime.combine(date_obj, time(hour + 1, 0))
            ) for hour in range(9, 17)
        ]

        bookings = Booking.objects.filter(room=room, booking_date=date_obj)
        booked_slots = [(booking.start_hour, booking.end_hour) for booking in bookings]

        available_slots = []
        for start, end in possible_slots:
            slot_free = True
            for b_start, b_end in booked_slots:
                b_start_dt = datetime.combine(date_obj, b_start)
                b_end_dt = datetime.combine(date_obj, b_end)
                if (b_start_dt < end and b_end_dt > start):
                    slot_free = False
                    break
            if slot_free:
                available_slots.append({
                    "start_hour": start.time().strftime("%H:%M"),
                    "end_hour": end.time().strftime("%H:%M"),
                })

        return JsonResponse({"available_slots": available_slots}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def create_booking(request):
    """Create a new booking."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            user_id = data.get('user_id')
            start_hour_str = data.get('start_hour')
            end_hour_str = data.get('end_hour')
            booking_date_str = data.get('date')

            if not all([room_id, user_id, start_hour_str, end_hour_str, booking_date_str]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            room = get_object_or_404(Room, id=room_id)
            user = get_object_or_404(User, id=user_id)
            start_hour = datetime.strptime(start_hour_str, "%H:%M").time()
            end_hour = datetime.strptime(end_hour_str, "%H:%M").time()
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()

            existing_booking = Booking.objects.filter(
                room=room,
                start_hour__lt=end_hour,
                end_hour__gt=start_hour,
                booking_date=booking_date,
            ).exists()

            if existing_booking:
                return JsonResponse({"error": "Time slot is already booked."}, status=400)

            booking = Booking.objects.create(
                user=user,
                room=room,
                start_hour=start_hour,
                end_hour=end_hour,
                booking_date=booking_date,
                status='Confirmed'
            )

            return JsonResponse({"message": "Booking created successfully", "booking_id": booking.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_booking(request, booking_id):
    """Update an existing booking."""
    if request.method == 'PUT':
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            data = json.loads(request.body)

            start_hour_str = data.get('start_hour')
            end_hour_str = data.get('end_hour')
            status = data.get('status')

            if not all([start_hour_str, end_hour_str, status]):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            start_hour = datetime.strptime(start_hour_str, "%H:%M").time()
            end_hour = datetime.strptime(end_hour_str, "%H:%M").time()

            if status not in dict(Booking.STATUS_CHOICES):
                return JsonResponse({"error": "Invalid status."}, status=400)

            booking.start_hour = start_hour
            booking.end_hour = end_hour
            booking.status = status
            booking.clean()  # Validate booking times
            booking.save()

            return JsonResponse({
                "booking": {
                    "id": booking.id,
                    "room": booking.room.name,
                    "start_hour": booking.start_hour.strftime("%H:%M"),
                    "end_hour": booking.end_hour.strftime("%H:%M"),
                    "date": booking.booking_date.strftime("%Y-%m-%d"),
                    "status": booking.status,
                }
            }, status=200)
        except ValidationError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def delete_booking(request, booking_id):
    """Delete a booking."""
    if request.method == 'DELETE':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return JsonResponse({"message": "Booking deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_users(request):
    """Fetch all users."""
    if request.method == 'GET':
        users = User.objects.all()
        user_list = [{
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "staff_type": user.staff_type,
            "school": user.school,
        } for user in users]
        return JsonResponse({"users": user_list}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def verify_user(request):
    """Verify if a user exists by their email and password."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({"error": "Email and password are required."}, status=400)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                return JsonResponse({
                    "message": "User verified successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "staff_type": user.staff_type,
                        "school": user.school,
                    }
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def create_user(request):
    """Create a new user."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            staff_type = data.get('staff_type')
            school = data.get('school')

            if not all([email, password, first_name, last_name, staff_type, school]):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email is already in use."}, status=400)

            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                staff_type=staff_type,
                school=school
            )
            return JsonResponse({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "staff_type": user.staff_type,
                    "school": user.school,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_user(request, user_id):
    """Update an existing user."""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=user_id)

            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.staff_type = data.get('staff_type', user.staff_type)
            user.school = data.get('school', user.school)

            if 'password' in data and data['password']:
                user.set_password(data['password'])

            user.save()
            return JsonResponse({
                "message": "User updated successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "staff_type": user.staff_type,
                    "school": user.school,
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_user(request, user_id):
    """Delete a user."""
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_rooms(request):
    """Fetch all rooms."""
    if request.method == 'GET':
        rooms = Room.objects.filter(is_active=True)
        room_list = [
            {
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "capacity": room.capacity,
                "is_active": room.is_active,
            }
            for room in rooms
        ]
        return JsonResponse({"rooms": room_list}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def create_room(request):
    """Create a new room."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            capacity = data.get('capacity', 0)
            is_active = data.get('is_active', True)

            if not name:
                return JsonResponse({"error": "Room name is required."}, status=400)

            room = Room.objects.create(
                name=name,
                description=description,
                capacity=capacity,
                is_active=is_active
            )
            return JsonResponse({
                "message": "Room created successfully",
                "room": {
                    "id": room.id,
                    "name": room.name,
                    "description": room.description,
                    "capacity": room.capacity,
                    "is_active": room.is_active,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_room(request, room_id):
    """Update an existing room."""
    if request.method == 'PUT':
        try:
            room = get_object_or_404(Room, id=room_id)
            data = json.loads(request.body)

            room.name = data.get('name', room.name)
            room.description = data.get('description', room.description)
            room.capacity = data.get('capacity', room.capacity)
            room.is_active = data.get('is_active', room.is_active)

            room.save()
            return JsonResponse({
                "message": "Room updated successfully",
                "room": {
                    "id": room.id,
                    "name": room.name,
                    "description": room.description,
                    "capacity": room.capacity,
                    "is_active": room.is_active,
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_room(request, room_id):
    """Delete a room."""
    if request.method == 'DELETE':
        try:
            room = get_object_or_404(Room, id=room_id)
            room.delete()
            return JsonResponse({"message": "Room deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)