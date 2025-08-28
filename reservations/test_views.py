from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from .models import Reservation
from .forms import ReservationForm

class TestReservationViews(TestCase):

    def setUp(self):
        # Create a normal user and a superuser
        self.user = User.objects.create_user(
            username="regular_user", password="password123")
        self.superuser = User.objects.create_superuser(
            username="admin_user", password="adminpass")

        # Client to simulate requests
        self.client = Client()

        # Example reservation for tests
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date.today() + timedelta(days=1),
            time=time(18, 0),
            guests=4,
            special_requests="Test request",
            status="pending"
        )

    # Tests for reservation_dashboard
    def test_reservation_dashboard_accessible_for_logged_in_user(self):
        self.client.login(username="regular_user", password="password123")
        response = self.client.get(reverse("reservation_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test request")

    def test_reservation_dashboard_redirect_for_anonymous_user(self):
        response = self.client.get(reverse("reservation_dashboard"))
        self.assertEqual(response.status_code, 302)

    # Tests for make_reservation view
    def test_make_reservation_get_request(self):
        self.client.login(username="regular_user", password="password123")
        response = self.client.get(reverse("make_reservation"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ReservationForm)

    def test_make_reservation_post_valid(self):
        self.client.login(username="regular_user", password="password123")
        data = {
            "date": date.today() + timedelta(days=2),
            "time": time(19, 0),
            "guests": 3,
            "special_requests": "Birthday"
        }
        response = self.client.post(reverse("make_reservation"), data)
        self.assertRedirects(response, reverse("reservation_dashboard"))
        self.assertEqual(Reservation.objects.filter(user=self.user).count(), 2)

    # Tests for edit_reservation
    def test_edit_reservation_get_request(self):
        self.client.login(username="regular_user", password="password123")
        response = self.client.get(reverse("edit_reservation", args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ReservationForm)

    def test_edit_reservation_post_updates_status(self):
        self.client.login(username="regular_user", password="password123")
        data = {
            "date": self.reservation.date,
            "time": self.reservation.time,
            "guests": self.reservation.guests,
            "special_requests": "Updated request"
        }
        response = self.client.post(reverse("edit_reservation", args=[self.reservation.id]), data)
        updated = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(updated.status, "pending")
        self.assertEqual(updated.special_requests, "Updated request")
        self.assertRedirects(response, reverse("reservation_dashboard"))

    # Tests for cancel_reservation
    def test_cancel_reservation_post(self):
        self.client.login(username="regular_user", password="password123")
        response = self.client.post(reverse("cancel_reservation", args=[self.reservation.id]))
        self.assertRedirects(response, reverse("reservation_dashboard"))
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    # Tests for superuser_reservations
    def test_superuser_reservations_accessible_for_superuser(self):
        self.client.login(username="admin_user", password="adminpass")
        response = self.client.get(reverse("superuser_reservations"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test request")

    def test_superuser_can_update_status(self):
        self.client.login(username="admin_user", password="adminpass")
        response = self.client.post(reverse("superuser_reservations"), {
            "reservation_id": self.reservation.id,
            "status": "confirmed"
        })
        updated = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(updated.status, "confirmed")
        self.assertRedirects(response, reverse("superuser_reservations"))
