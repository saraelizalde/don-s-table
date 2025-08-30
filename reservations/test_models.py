from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, time, timedelta, datetime
from .models import Reservation, STATUS_CHOICES


class TestReservationModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="testpass")

        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date.today(),
            time=time(18, 0),
            guests=4,
            special_requests="Test request"
        )

    def test_str_method(self):
        """Test the string representation of a reservation"""
        expected = (
            f"Reservation for {self.user.username} "
            f"on {self.reservation.date} at {self.reservation.time}"
        )
        self.assertEqual(str(self.reservation), expected)

    def test_end_time_auto_calculated(self):
        """Test that end_time is automatically set one hour after start time"""
        expected_end = (
            datetime.combine(self.reservation.date, self.reservation.time)
            + timedelta(hours=1)
        ).time()
        self.assertEqual(self.reservation.end_time, expected_end)

    def test_guests_limits(self):
        """Test that guests cannot exceed the allowed min/max"""
        self.reservation.guests = 14
        self.reservation.full_clean()
        self.reservation.guests = 1
        self.reservation.full_clean()

        # Invalid guest number (too low)
        self.reservation.guests = 0
        with self.assertRaises(Exception):
            self.reservation.full_clean()

        # Invalid guest number (too high)
        self.reservation.guests = 15
        with self.assertRaises(Exception):
            self.reservation.full_clean()
