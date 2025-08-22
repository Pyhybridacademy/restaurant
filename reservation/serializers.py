from rest_framework import serializers
from .models import Reservation
from django.utils import timezone

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'phone', 'date', 'time', 'party_size', 'special_requests', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot make reservations for past dates.")
        return value
    
    def validate(self, data):
        # Check if the time slot is already booked
        if Reservation.objects.filter(
            date=data['date'], 
            time=data['time'],
            status__in=['pending', 'confirmed']
        ).exists():
            raise serializers.ValidationError("This time slot is already booked.")
        return data

class AvailableTimesSerializer(serializers.Serializer):
    date = serializers.DateField()
