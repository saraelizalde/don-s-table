"""
Views for the Reservations app.

Provides functionality for users to:
- View their reservations dashboard
- Make a new reservation
- Edit an existing reservation
- Cancel a reservation

All views require the user to be logged in.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages

@login_required
def reservation_dashboard(request):
    """
    Display the reservation dashboard for the logged-in user.

    Shows all upcoming reservations for the user, ordered by date and time.

    Template:
        reservation_dashboard.html
    """
    today = localdate()
    user_reservations = Reservation.objects.filter(
        user=request.user,
        date__gte=today
    ).order_by('date', 'time')
    return render(request, 'reservation_dashboard.html', {'reservations': user_reservations})

@login_required
def make_reservation(request):
    """
    Handle the creation of a new reservation.

    If the request is POST and the form is valid:
        - Associate the reservation with the logged-in user
        - Save the reservation
        - Show a success message
        - Redirect to reservation dashboard

    If the request is GET or the form is invalid:
        - Display the reservation form

    Template:
        reservation_form.html
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Your reservation has been submitted and is pending confirmation.")
            return redirect('reservation_dashboard')
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def edit_reservation(request, reservation_id):
    """
    Edit an existing reservation for the logged-in user.

    Only the owner of the reservation can edit it. If the form changes:
        - Reset the reservation status to 'pending'
        - Show a success message

    Template:
        reservation_form.html
    """
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            if form.has_changed():  # Only reset status if something actually changed
                updated = form.save(commit=False)
                updated.status = "pending"
                updated.save()
                messages.success(request, "Your reservation has been updated and is pending confirmation.")
            else:
                form.save()  # No changes -> just save without resetting status
            return redirect("reservation_dashboard")
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def cancel_reservation(request, reservation_id):
    """
    Cancel an existing reservation for the logged-in user.

    Only the owner of the reservation can cancel it. Shows a success message
    after deletion and redirects to the dashboard.

    Note:
        This view expects a POST request for deletion.

    Redirects:
        reservation_dashboard
    """
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation cancelled successfully.")
        return redirect('reservation_dashboard')
    return redirect('reservation_dashboard')