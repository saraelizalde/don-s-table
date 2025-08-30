"""
Models for the Reservations app.

Defines the Reservation model which represents a table reservation
made by a user, including date, time, number of guests, and status.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]


class Reservation(models.Model):
    """
    Represents a table reservation made by a user.

    Attributes:
        user (User): The user who made the reservation.
        date (date): Date of the reservation.
        time (time): Start time of the reservation.
        end_time (time):
        Automatically calculated end time (1 hour after start).
        guests (int): Number of guests (1–14).
        special_requests (str): Optional notes or special requests.
        created_on (datetime): Timestamp when the reservation was created.
        status (str): Current status of the reservation
        (pending, confirmed, cancelled).

    Methods:
        save(*args, **kwargs):
        Overrides save to calculate end_time automatically.
        __str__(): Returns a human-readable string representation.

    Meta:
        ordering: Reservations are ordered by date, then time.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(editable=False)
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(14)]
    )
    special_requests = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        )

    def save(self, *args, **kwargs):
        """
        Override save to automatically set the end_time.

        End time is calculated as one hour after the start time.
        """
        if self.time:
            self.end_time = (
                datetime.combine(self.date, self.time) + timedelta(hours=1)
                ).time()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a string for the reservation."""
        return (
            f"Reservation for {self.user.username} "
            f"on {self.date} at {self.time}"
        )

    class Meta:
        ordering = ['date', 'time']
