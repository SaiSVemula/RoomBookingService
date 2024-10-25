from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Room, User, Booking


def get_rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        room_list = [{"id": room.id, "name": room.name, "capacity": room.capacity} for room in rooms]
        return JsonResponse(room_list, safe=False)

# @csrf_exempt 
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=data['user_id'])
            room = get_object_or_404(Room, id=data['room_id'])
            
            # Create a new booking
            booking = Booking.objects.create(
                user=user,
                room=room,
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime'],
                status='Pending'
            )
            
            return JsonResponse({"message": "Booking created successfully", "booking_id": booking.id})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# @csrf_exempt
def update_booking(request, booking_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            booking = get_object_or_404(Booking, id=booking_id)
            
            booking.start_datetime = data['start_datetime']
            booking.end_datetime = data['end_datetime']
            booking.status = data.get('status', booking.status)  # Keep status the same if not provided
            booking.save()

            return JsonResponse({"message": "Booking updated successfully"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# @csrf_exempt
def delete_booking(request, booking_id):
    if request.method == 'DELETE':
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            booking.delete()
            return JsonResponse({"message": "Booking deleted successfully"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
