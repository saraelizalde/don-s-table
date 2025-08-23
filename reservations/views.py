from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from .models import Reservation
from .forms import ReservationForm

# Create your views here.
@login_required
def reservation_dashboard(request):
    today = localdate()  # today’s date
    user_reservations = Reservation.objects.filter(
        user=request.user,
        date__gte=today
    ).order_by('date', 'time')
    return render(request, 'reservation_dashboard.html', {'reservations': user_reservations})

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('reservation_dashboard')
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            if form.has_changed():  # Only reset status if something actually changed
                updated = form.save(commit=False)
                updated.status = "pending"
                updated.save()
            else:
                form.save()  # No changes -> just save without resetting status
            return redirect("reservation_dashboard")
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        reservation.delete()
        return redirect('reservation_dashboard')
    return redirect('reservation_dashboard')