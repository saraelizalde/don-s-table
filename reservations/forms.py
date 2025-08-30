"""
Forms for the Reservations app.

Includes:
- ReservationForm: Handles validation and input for making a reservation.
- generate_time_choices: Generates half-hourly time slots for reservations.
"""

from django import forms
from django.utils import timezone
from django.db.models import Sum
import datetime
from .models import Reservation

TOTAL_CAPACITY_PER_SLOT = 50


def generate_time_choices():
    """
    Generate a list of time slots for reservations.

    Time slots are half-hourly from 11:00 AM to 10:30 PM.

    Returns:
        list of tuples: Each tuple contains (datetime.time, formatted string)
    """
    times = []
    for hour in range(11, 23):
        for minute in (0, 30):
            t = datetime.time(hour, minute)
            label = t.strftime("%I:%M %p")
            times.append((t, label))
    return times


class ReservationForm(forms.ModelForm):
    """
    Form for creating or editing a Reservation.

    Fields:
        date: Date of the reservation.
        time: Time of the reservation (half-hour slots).
        guests: Number of guests (1–14).
        special_requests: Optional text for special requests.

    Validation:
        - Ensures reservation is not in the past.
        - Checks that the total number of guests in a time slot
          does not exceed TOTAL_CAPACITY_PER_SLOT.
    """
    time = forms.TypedChoiceField(
        choices=[("", "-- : --")] + generate_time_choices(),
        coerce=lambda v: datetime.datetime.strptime(v, "%H:%M:%S").time()
        if isinstance(v, str) else v,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'special_requests']
        widgets = {
            'date': forms.DateInput
            (attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput
            (attrs={'min': 1, 'max': 14, 'class': 'form-control'}),
            'special_requests': forms.Textarea
            (attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        """
        Validate reservation data.

        Checks:
        - Reservation datetime is not in the past.
        - Total guests for the selected time slot do not exceed capacity.

        Returns:
            dict: Cleaned data
        Raises:
            forms.ValidationError: If any validation fails
        """
        cleaned = super().clean()
        d = cleaned.get('date')
        t = cleaned.get('time')
        g = cleaned.get('guests')

        if d and t:
            if isinstance(t, str):
                try:
                    t = datetime.datetime.strptime(t, "%H:%M:%S").time()
                except ValueError:
                    t = datetime.datetime.strptime(t, "%H:%M").time()

            chosen_dt = datetime.datetime.combine(d, t)
            chosen_dt = timezone.make_aware(chosen_dt,
                                            timezone.get_current_timezone())

            if chosen_dt < timezone.now():
                raise forms.ValidationError(
                    "Reservation cannot be in the past."
                    )

        # capacity check
        if d and t and g:
            existing = (Reservation.objects
                        .filter(date=d, time=t)
                        .aggregate(total=Sum('guests'))['total'] or 0)
            if existing + g > TOTAL_CAPACITY_PER_SLOT:
                raise forms.ValidationError(
                    "Not enough availability for that time slot."
                    )

        return cleaned
