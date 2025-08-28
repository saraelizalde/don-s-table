from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
from .forms import ReservationForm
from .models import Reservation
from django.db.models import Sum

class TestReservationForm(TestCase):
    """
    Tests for ReservationForm validation and logic.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        
        # Create an existing reservation for capacity testing
        self.existing_reservation = Reservation.objects.create(
            user=self.user,
            date=date.today() + timedelta(days=1),
            time=time(19, 0),
            guests=30
        )

    def test_form_valid_data(self):
        """
        The form should be valid with all required fields correctly filled.
        """
        form_data = {
            'date': date.today() + timedelta(days=1),
            'time': time(18, 0),
            'guests': 4,
            'special_requests': 'Window seat'
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="Form should be valid with correct data")

    def test_form_invalid_past_date(self):
        """
        The form should be invalid if the reservation date/time is in the past.
        """
        past_date = date.today() - timedelta(days=1)
        form_data = {
            'date': past_date,
            'time': time(12, 0),
            'guests': 2,
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid with past date")

    def test_form_invalid_over_capacity(self):
        """
        The form should be invalid if adding guests exceeds TOTAL_CAPACITY_PER_SLOT.
        """
        form_data = {
            'date': self.existing_reservation.date,
            'time': self.existing_reservation.time,
            'guests': 25,
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid even though it exceeds capacity")

    def test_form_invalid_missing_time(self):
        """
        The form should be invalid if the time is missing.
        """
        form_data = {
            'date': date.today() + timedelta(days=1),
            'guests': 4,
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid even though time is missing")

    def test_form_invalid_missing_guests(self):
        """
        The form should be invalid if the number of guests is missing.
        """
        form_data = {
            'date': date.today() + timedelta(days=1),
            'time': time(19, 0),
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid even though guests number is missing")

    def test_form_invalid_too_many_guests(self):
        """
        The form should be invalid if the number of guests exceeds 14.
        """
        form_data = {
            'date': date.today() + timedelta(days=1),
            'time': time(18, 0),
            'guests': 15,
            'special_requests': 'Extra chairs'
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid even though guests exceed 14")
