from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer, AvailableTimesSerializer
from django.utils import timezone

def reservation_page(request):
    return render(request, 'reservation/reservation.html')

@csrf_exempt
@api_view(['POST'])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        reservation = serializer.save()
        if request.user.is_authenticated:
            reservation.user = request.user
            reservation.save()
        return Response({
            'success': True,
            'message': 'Reservation created successfully!',
            'reservation': ReservationSerializer(reservation).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def available_times(request):
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'Date parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
    if date < timezone.now().date():
        return Response({'available_times': []})
    
    # Get booked times for the date
    booked_times = Reservation.objects.filter(
        date=date,
        status__in=['pending', 'confirmed']
    ).values_list('time', flat=True)
    
    # Get all available times
    all_times = [time[0] for time in Reservation.TIME_SLOTS]
    available_times = [time for time in all_times if time not in booked_times]
    
    return Response({'available_times': available_times})

@csrf_exempt
@api_view(['GET'])
def user_reservations(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user=request.user)
    else:
        # For anonymous users, we could use session or email lookup
        email = request.GET.get('email')
        if email:
            reservations = Reservation.objects.filter(email=email)
        else:
            return Response({'reservations': []})
    
    serializer = ReservationSerializer(reservations, many=True)
    return Response({'reservations': serializer.data})
