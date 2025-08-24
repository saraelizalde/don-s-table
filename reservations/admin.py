"""
Admin configuration for the Reservations app.

Registers the Reservation model with custom admin options including:
- List display fields
- Filters
- Search fields
- Ordering
"""

from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'end_time', 'guests', 'status', 'created_on')
    list_filter = ('status', 'date', 'guests')
    search_fields = ('user__username', 'special_requests')
    ordering = ('date', 'time')