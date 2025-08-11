from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def make_reservation(request):
    return render(request, 'reservation_form.html')

def reservation_dashboard(request):
    return render(request, 'reservation_dashboard.html')