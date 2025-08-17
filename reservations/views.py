from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Reservation
from .forms import ReservationForm

# Create your views here.
@login_required
def reservation_dashboard(request):
    user_reservations = Reservation.objects.filter(user=request.user, date__gte=timezone.now())
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